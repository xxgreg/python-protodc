package main

func getTemplate(repeat RepeatKind, kind Kind) (Template, bool) {
	for _, t := range templates {
		if t.Repeat == repeat && t.Kind == kind {
			return t, true
		}
	}
	return Template{}, false
}

type Template struct {
	Repeat             RepeatKind
	Kind               Kind
	Field              []string
	ToPB               []string
	FromPBWithPresence string
	FromPB             []string
}

type replaceOpts []string

func newReplaceOpts(f Field) replaceOpts {
	return []string{
		"~py_field~", f.PyName,
		"~pb_field~", f.PbName,
		"~py_type~", f.ValueType.PyType,
		"~py_default~", f.ValueType.PyDefault,
		"~py_core_type~", f.ValueType.CorePyType,
		"~py_key_type~", f.KeyType.PyType,
	}
}

func (t Template) WriteField(out *Output, opts replaceOpts) {
	out.Render(t.Field, opts...)
}

func (t Template) WriteToPB(out *Output, opts replaceOpts) {
	out.Render(t.ToPB, opts...)
}

func (t Template) WriteFromPB(out *Output, opts replaceOpts, hasPresence bool) {
	// TODO has presence is only used by enum template - perhaps just duplicate that template.
	hasPresence = hasPresence && t.FromPBWithPresence != ""
	if hasPresence {
		out.Render([]string{t.FromPBWithPresence}, opts...)
		out.Indent += 1
	}
	out.Render(t.FromPB, opts...)
	if hasPresence {
		out.Indent -= 1
	}
}

var templates = []Template{
	// TODO check handling of Nones in lists for each template
	{
		Repeat: RepeatedKind,
		Kind:   PrimitiveKind,
		Field: []string{
			"~py_field~: list[~py_type~] = field(default_factory=list) ",
		},
		ToPB: []string{
			"if self.~py_field~ is not None: ",
			"    pb.~pb_field~.extend(self.~py_field~) ",
		},
		FromPB: []string{
			"dc.~py_field~ = [x for x in pb.~pb_field~] ",
		},
	},
	{
		Repeat: RepeatedKind,
		Kind:   MessageKind,
		Field: []string{
			"~py_field~: list['~py_type~'] = field(default_factory=list) ",
		},
		ToPB: []string{
			"if self.~py_field~ is not None: ",
			"    for x in self.~py_field~: ",
			"        x.to_protobuf(target_pb=pb.~pb_field~.add(), depth=depth+1) ",
		},
		FromPB: []string{
			"dc.~py_field~ = [~py_type~.from_protobuf(x, depth=depth+1) for x in pb.~pb_field~]",
		},
	},
	{
		Repeat: RepeatedKind,
		Kind:   EnumKind,
		Field: []string{
			"~py_field~: list['~py_type~'] = field(default_factory=list) ",
		},
		ToPB: []string{
			"if self.~py_field~ is not None: ",
			"    pb.~pb_field~.extend([x.value for x in self.~py_field~]) ",
		},
		FromPB: []string{
			"dc.~py_field~ = [~py_type~(x) for x in pb.~pb_field~] ",
		},
	},
	{
		Repeat: RepeatedKind,
		Kind:   AnyKind,
		Field: []string{
			"~py_field~: list[Any] = field(default_factory=list)",
		},
		ToPB: []string{
			"if self.~py_field~ is not None:",
			"    for x in self.~py_field~:",
			"        protodc.pack_any(x, pb.~pb_field~.add(), depth+1) ",
		},
		FromPB: []string{
			"dc.~py_field~ = [protodc.unpack_any(x, depth=depth+1) for x in pb.~pb_field~]",
		},
	},
	{
		Repeat: RepeatedKind,
		Kind:   WrapperKind,
		Field: []string{
			"~py_field~: list[~py_type~] = field(default_factory=list)",
		},
		ToPB: []string{
			"if self.~py_field~ is not None: ",
			"    for x in self.~py_field~: ",
			"        pb.~pb_field~.add().value = x ",
		},
		FromPB: []string{
			"dc.~py_field~ = [x.value for x in pb.~pb_field~]",
		},
	},
	{
		Repeat: RepeatedKind,
		Kind:   StructKind,
		Field: []string{
			"~py_field~: list[~py_type~] = field(default_factory=list)",
		},
		ToPB: []string{
			"if self.~py_field~ is not None: ",
			"    for x in self.~py_field~: ",
			"        google.protobuf.json_format.ParseDict(x, pb.~pb_field~.add()) ",
		},
		FromPB: []string{
			"dc.~py_field~ = [google.protobuf.json_format.MessageToDict(x) for x in pb.~pb_field~]",
		},
	},
	{
		Repeat: RepeatedKind,
		Kind:   TimestampKind,
		Field: []string{
			"~py_field~: list[datetime] = field(default_factory=list)",
		},
		ToPB: []string{
			"if self.~py_field~ is not None:",
			"    for x in self.~py_field~:",
			"        pb.~pb_field~.add().FromDatetime(x)",
		},
		FromPB: []string{
			"dc.~py_field~ = [x.ToDatetime() for x in pb.~pb_field~]",
		},
	},
	{
		Repeat: MapKind,
		Kind:   PrimitiveKind,
		Field: []string{
			"~py_field~: dict[~py_key_type~, '~py_core_type~'] = field(default_factory=dict)",
		},
		ToPB: []string{
			"if self.~py_field~ is not None: ",
			"    pb.~pb_field~.update(self.~py_field~) ",
		},
		FromPB: []string{
			"dc.~py_field~ = {k: v for (k, v) in pb.~pb_field~.items()} ",
		},
	},
	{
		Repeat: MapKind,
		Kind:   EnumKind,
		Field: []string{
			"~py_field~: dict[~py_key_type~, '~py_core_type~'] = field(default_factory=dict)",
		},
		ToPB: []string{
			"if self.~py_field~ is not None:",
			"    for (k, v) in self.~py_field~.items():",
			"        pb.~pb_field~[k] = v.value",
		},
		FromPB: []string{
			"dc.~py_field~ = {k: ~py_type~(v) for (k, v) in pb.~pb_field~.items()}",
		},
	},
	{
		Repeat: MapKind,
		Kind:   MessageKind,
		Field: []string{
			"~py_field~: dict[~py_key_type~, '~py_core_type~'] = field(default_factory=dict)",
		},
		ToPB: []string{
			"if self.~py_field~ is not None: ",
			"    for (k, v) in self.~py_field~.items(): ",
			"        v.to_protobuf(target_pb=pb.~py_field~.get_or_create(k), depth=depth+1) ",
		},
		FromPB: []string{
			"dc.~py_field~ = {k: ~py_type~.from_protobuf(v, depth=depth+1) for (k, v) in pb.~pb_field~.items()}",
		},
	},
	{
		Repeat: MapKind,
		Kind:   AnyKind,
		Field: []string{
			"~py_field~: dict[~py_key_type~, '~py_core_type~'] = field(default_factory=dict)",
		},
		ToPB: []string{
			"if self.~py_field~ is not None: ",
			"    for (k, v) in self.~py_field~.items(): ",
			"        protodc.pack_any(v, pb.~py_field~.get_or_create(k), depth+1) ",
		},
		FromPB: []string{
			"dc.~py_field~ = {k: protodc.unpack_any(v, depth=depth+1) for (k, v) in pb.~pb_field~.items()}",
		},
	},
	{
		Repeat: MapKind,
		Kind:   WrapperKind,
		Field: []string{
			"~py_field~: dict[~py_key_type~, '~py_core_type~'] = field(default_factory=dict)",
		},
		ToPB: []string{
			"if self.~py_field~ is not None:",
			"    for (k, v) in self.~py_field~.items():",
			"        pb.~pb_field~[k].value = v",
		},
		FromPB: []string{
			"dc.~py_field~ = {k: ~py_core_type~(v.value) for (k, v) in pb.~pb_field~.items()}",
		},
	},
	{
		Repeat: MapKind,
		Kind:   TimestampKind,
		Field: []string{
			"~py_field~: dict[~py_key_type~, datetime] = field(default_factory=dict)",
		},
		ToPB: []string{
			"if self.~py_field~ is not None:",
			"    for (k, v) in self.~py_field~.items():",
			"        pb.~pb_field~[k].FromDatetime(v)",
		},
		FromPB: []string{
			"dc.~py_field~ = {k: v.ToDatetime() for (k, v) in pb.~pb_field~.items()}",
		},
	},
	{
		Repeat: MapKind,
		Kind:   StructKind,
		Field: []string{
			"~py_field~: dict[~py_key_type~, '~py_core_type~'] = field(default_factory=dict)",
		},
		ToPB: []string{
			"if self.~py_field~ is not None: ",
			"    for (k, v) in self.~py_field~.items():",
			"        google.protobuf.json_format.ParseDict(v, pb.~pb_field~[k])",
		},
		FromPB: []string{
			"dc.~py_field~ = {k: google.protobuf.json_format.MessageToDict(v) for (k, v) in pb.~pb_field~.items()}",
		},
	},
	{
		Repeat: SingularKind,
		Kind:   PrimitiveKind,
		Field: []string{
			"~py_field~: ~py_type~ = ~py_default~ ", // py_default: 0, "", 0.0, False
		},
		ToPB: []string{
			"if self.~py_field~ is not None: ",
			"    pb.~pb_field~ = self.~py_field~ ",
		},
		FromPBWithPresence: "if pb.HasField('~pb_field~'):",
		FromPB: []string{
			"dc.~py_field~ = pb.~pb_field~",
		},
	},
	{
		Repeat: SingularKind,
		Kind:   EnumKind,
		Field: []string{
			"~py_field~: '~py_type~' = ~py_default~ ", // py_type(0) or Optional[py_type(0)] with presence
		},
		ToPB: []string{
			"if self.~py_field~ is not None: ",
			"    pb.~pb_field~ = self.~py_field~.value ",
		},
		FromPBWithPresence: "if pb.HasField('~pb_field~'): ",
		FromPB: []string{
			"dc.~py_field~ = ~py_core_type~(pb.~pb_field~) ",
		},
	},
	{
		Repeat: SingularKind,
		Kind:   MessageKind,
		Field: []string{
			"~py_field~: Optional['~py_type~'] = None ",
		},
		ToPB: []string{
			"if self.~py_field~ is not None: ",
			"     self.~py_field~.to_protobuf(target_pb=pb.~pb_field~, depth=depth+1) ",
		},
		FromPB: []string{
			"if pb.HasField('~pb_field~'): ",
			"    dc.~py_field~ = ~py_type~.from_protobuf(pb.~pb_field~, depth=depth+1) ",
		},
	},
	{
		Repeat: SingularKind,
		Kind:   AnyKind,
		Field: []string{
			"~py_field~: Any = None ",
		},
		ToPB: []string{
			"if self.~py_field~ is not None: ",
			"    protodc.pack_any(self.~py_field~, pb.~pb_field~, depth+1) ",
		},
		FromPB: []string{
			"if pb.HasField('~pb_field~'): ",
			"    dc.~py_field~ = protodc.unpack_any(pb.~pb_field~, depth+1) ",
		},
	},
	{
		Repeat: SingularKind,
		Kind:   NullValueKind,
		Field: []string{
			"~py_field~: None = None ",
		},
		// No Output
	},
	{
		Repeat: SingularKind,
		Kind:   StructKind, // Struct/List/Value
		Field: []string{
			// TODO optional list and struct?
			// py_type: Optional[list], Union[None, int, float, list, dict], Optional[dict[str, Any]]
			"~py_field~: ~py_type~ = None ",
		},
		ToPB: []string{
			"if self.~py_field~ is not None: ",
			"    google.protobuf.json_format.ParseDict(self.~py_field~, pb.~pb_field~) ",
		},
		FromPB: []string{
			"if pb.HasField('~pb_field~'): ",
			"    dc.~py_field~ = google.protobuf.json_format.MessageToDict(pb.~pb_field~) ",
		},
	},
	{
		Repeat: SingularKind,
		Kind:   WrapperKind,
		Field: []string{
			"~py_field~: Optional[~py_type~] = None ",
		},
		ToPB: []string{
			"if self.~py_field~ is not None: ",
			"     pb.~pb_field~.value = self.~py_field~ ",
		},
		FromPB: []string{
			"if pb.HasField('~pb_field~'): ",
			"    dc.~py_field~ = pb.~pb_field~.value ",
		},
	},
	{
		Repeat: SingularKind,
		Kind:   TimestampKind,
		Field: []string{
			"~py_field~: Optional[datetime] = None ",
		},
		ToPB: []string{
			"if self.~py_field~ is not None: ",
			"    pb.~pb_field~.FromDatetime(self.~py_field~) ",
		},
		FromPB: []string{
			"if pb.HasField('~pb_field~'): ",
			"    dc.~py_field~ = pb.~pb_field~.ToDatetime() ",
		},
	},
}
