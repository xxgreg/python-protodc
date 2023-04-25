package main

import (
	"strconv"
	"strings"
)

func oneofClass(out *Output, msg Message, field Field) {

	// message Example {
	//   oneof stuff {
	//    int64 with_stuff = 14;
	//    int64 and_stuff = 15;
	//   }
	// }

	// becomes:
	// class ExampleStuffOneof(enum.Enum):
	//     None = 0
	//     with_stuff = 1
	//     and_stuff = 2

	out.Render([]string{
		"class ~msg_py_name~~py_pascal_field~Oneof(enum.Enum): ",
		"    NONE = 0",
	},
		"~msg_py_name~", msg.PyName,
		"~py_pascal_field~", field.Oneof.PyPascalName)

	for i, f := range field.Oneof.Fields {
		// Using lowercase to match oneof names - python convention is uppercase,
		// but this is simpler to implement.
		out.Write("    " + f.PyName + " = " + strconv.Itoa(i+1))
	}
	out.Write("")
	out.Write("")
}

func oneofFields(out *Output, msg Message, field Field) {

	oneofClassName := msg.PyName + field.Oneof.PyPascalName + "Oneof"

	//TODO remove duplicates
	var oneofTypes []string
	for _, f := range field.Oneof.Fields {
		oneofTypes = append(oneofTypes, f.ValueType.CorePyType)
	}

	out.Render([]string{
		"which_~py_field~: ~oneof_class~ = ~oneof_class~.NONE",
		"~py_field~: Union[None, ~oneof_types~] = None",
	},
		"~py_field~", field.Oneof.PyName,
		"~oneof_class~", oneofClassName,
		"~oneof_types~", "'"+strings.Join(oneofTypes, "', '")+"'",
	)
}

func oneofPostInit(out *Output, msg Message) {
	out.Write("def __post_init__(self):")
	for _, f := range msg.Oneofs {
		out.Render([]string{
			"    if self.~oneof~ is not None and self.which_~oneof~ in (None, ~oneof_class~.NONE):",
			"        raise Exception('~msg~: which_~oneof~ not passed in constructor')",
			"",
		},
			"~msg~", msg.Fullname,
			"~oneof~", f.Oneof.PyName,
			"~oneof_class~", msg.PyName+f.Oneof.PyPascalName+"Oneof",
		)
	}
}

func oneofToPB(out *Output, msg Message, field Field) {

	out.Render([]string{
		"if self.which_~py_oneof_field~ is None or self.which_~py_oneof_field~ == ~py_oneof_class~.NONE:",
		"    pass",
	}, "~py_oneof_field~", field.Oneof.PyName,
		"~py_oneof_class~", msg.PyName+field.Oneof.PyPascalName+"Oneof")
	for _, f := range field.Oneof.Fields {
		line := ""
		switch f.ValueType.Kind {

		case PrimitiveKind:
			line = "pb.~pb_field~ = self.~py_oneof_field~"
		case MessageKind:
			line = "self.~py_oneof_field~.to_protobuf(target_pb=pb.~pb_field~, depth=depth+1)"
		case EnumKind:
			line = "pb.~pb_field~ = self.~py_oneof_field~.value"
		case AnyKind:
			line = "protodc.pack_any(self.~py_oneof_field~, pb.~pb_field~, depth+1)"
		case StructKind:
			line = "google.protobuf.json_format.ParseDict(self.~py_oneof_field~, pb.~pb_field~)"
		case WrapperKind:
			line = "pb.~pb_field~.value = self.~py_oneof_field~"
		case TimestampKind:
			line = "pb.~pb_field~.FromDatetime(self.~py_oneof_field~)"

			//TODO NullValueKind

		default:
			debug("unimplemented", field.Oneof.FullName, f.ValueType.Kind)
		}

		out.Render([]string{
			"elif self.which_~py_oneof_field~ == ~py_oneof_class~.~py_field~: ",
			"    " + line,
		},
			"~pb_field~", f.PbName,
			"~py_field~", f.PyName,
			"~py_oneof_field~", f.Oneof.PyName,
			"~py_oneof_class~", msg.PyName+field.Oneof.PyPascalName+"Oneof",
		)
	}
	out.Render([]string{
		"else:",
		"    raise Exception('to_protobuf(): unexpected value for ~full_name~')",
		"",
	},
		"~full_name~", field.Oneof.FullName)
}

func oneofFromPB(out *Output, msg Message, field Field) {

	out.Render([]string{
		"oneof_field_name = pb.WhichOneof('~pb_oneof_field~')",
		"if oneof_field_name is None:",
		"    pass",
	},
		"~pb_oneof_field~", field.Oneof.PbName)

	for _, f := range field.Oneof.Fields {
		line := ""
		switch f.ValueType.Kind {

		case PrimitiveKind:
			line = "dc.~py_oneof_field~ = pb.~pb_field~"
		case MessageKind:
			line = "dc.~py_oneof_field~ = ~py_msg_type~.from_protobuf(pb.~pb_field~, depth+1)"
		case EnumKind:
			line = "dc.~py_oneof_field~ = ~py_enum_type~(pb.~pb_field~)"
		case AnyKind:
			line = "dc.~py_oneof_field~ = protodc.unpack_any(pb.~pb_field~, depth=depth+1)"
		case StructKind:
			line = "dc.~py_oneof_field~ = google.protobuf.json_format.MessageToDict(pb.~pb_field~)"
		case WrapperKind:
			line = "dc.~py_oneof_field~ = pb.~pb_field~.value"
		case TimestampKind:
			line = "dc.~py_oneof_field~ = pb.~pb_field~.ToDatetime()"

			//TODO NullValueKind

		default:
			debug("unimplemented", field.FullName, f.ValueType.Kind)
		}
		out.Render([]string{
			"elif oneof_field_name == '~pb_field~':",
			"    dc.which_~py_oneof_field~ = ~py_oneof_class~.~py_field~",
			"    " + line,
		},
			"~py_oneof_class~", msg.PyName+field.Oneof.PyPascalName+"Oneof",
			"~py_field~", f.PyName,
			"~pb_field~", f.PbName,
			"~py_oneof_field~", field.Oneof.PyName,
			"~py_enum_type~", f.ValueType.CorePyType,
			"~py_msg_type~", f.ValueType.CorePyType,
		)
	}
	out.Render([]string{
		"else:",
		"    raise Exception('from_protobuf(): unexpected value for ~full_name~')",
		"",
	},
		"~full_name~", field.Oneof.FullName)
}

func oneofGettersAndSetters(out *Output, msg Message, oneof *Oneof, field Field) {
	out.Render([]string{
		"@property",
		"def ~py_field~(self) -> Optional['~py_field_type~']: ",
		"    if self.which_~py_oneof_field~ == ~oneof_py_class~.~py_field~: ",
		"        return self.~py_oneof_field~",
		"    else:",
		"        return None",
		"",
		"@~py_field~.setter",
		"def ~py_field~(self, value: '~py_field_type~'): ",
		"    self.which_~py_oneof_field~ = ~oneof_py_class~.~py_field~",
		"    self.~py_oneof_field~ = value",
		"",
	},
		"~py_field~", field.PyName,
		"~py_field_type~", field.ValueType.CorePyType,
		"~py_oneof_field~", oneof.PyName,
		"~oneof_py_class~", msg.PyName+oneof.PyPascalName+"Oneof",
	)
}
