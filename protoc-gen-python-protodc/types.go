package main

import (
	"strings"
	"unicode"

	"google.golang.org/protobuf/compiler/protogen"
	"google.golang.org/protobuf/reflect/protoreflect"
)

type PyPrimitive string

const (
	NotPyPrimitive PyPrimitive = "NA"
	PyInt                      = "int"
	PyFloat                    = "float"
	PyBool                     = "bool"
	PyString                   = "str"
	PyBytes                    = "bytes"
)

type Message struct {
	Fullname    string
	PyName      string
	PyPbPkgName string
	PbName      string
	Fields      []Field
	Oneofs      []*Field
}

type Field struct {
	FullName   string
	PyName     string
	PbName     string
	RepeatKind RepeatKind
	Oneof      *Oneof
	KeyType    Type
	ValueType  Type
}

type Oneof struct {
	FullName     string
	PyName       string
	PbName       string
	PyPascalName string // used for oneof classnames
	Fields       []Field
}

type Enum struct {
	Fullname string
	PyName   string
	PbName   string
	Values   []EnumValue
}

type EnumValue struct {
	Num    int
	PyName string
	PbName string
}

type Type struct {
	Kind        Kind
	HasPresence bool
	PyType      string
	CorePyType  string // not wrapped in Optional[] //rename UnwrappedType
	PyDefault   string // not used much
}

type RepeatKind int

//go:generate stringer -type=RepeatKind
const (
	SingularKind RepeatKind = iota
	RepeatedKind
	MapKind
	OneOfKind //TODO name?
)

type Kind int

//go:generate stringer -type=Kind
const (
	PrimitiveKind Kind = iota
	MessageKind
	EnumKind

	AnyKind
	TimestampKind
	WrapperKind
	StructKind
	NullValueKind
)

func newEnum(e *protogen.Enum) Enum {

	values := make([]EnumValue, 0, e.Desc.Values().Len())
	for i := 0; i < e.Desc.Values().Len(); i++ {
		v := e.Desc.Values().Get(i)
		values = append(values, EnumValue{
			Num:    int(v.Number()),
			PyName: string(v.Name()),
			PbName: string(v.Name()),
		})
	}

	return Enum{
		Fullname: string(e.Desc.FullName()),
		PyName:   string(e.Desc.Name()),
		PbName:   string(e.Desc.Name()),
		Values:   values,
	}
}

func newMessage(m *protogen.Message) Message {
	msg := Message{
		Fullname:    string(m.Desc.FullName()),
		PyName:      string(m.Desc.Name()),
		PbName:      string(m.Desc.Name()),
		PyPbPkgName: pb2TypeName(m.Desc),
		Fields:      make([]Field, 0, len(m.Fields)),
	}

	for _, f := range m.Fields {
		field := Field{
			FullName: string(f.Desc.FullName()),
			PyName:   string(f.Desc.Name()),
			PbName:   string(f.Desc.Name()),
		}

		switch {
		case f.Desc.IsList():
			field.RepeatKind = RepeatedKind
			field.ValueType = toType(f.Desc)

		case f.Desc.IsMap():
			field.RepeatKind = MapKind
			field.KeyType = Type{
				Kind:        PrimitiveKind,
				HasPresence: false,
				PyType:      string(toPyPrimitive(f.Desc.MapKey().Kind())),
			}
			field.ValueType = toType(f.Desc.MapValue())

		case f.Desc.ContainingOneof() != nil && !f.Desc.ContainingOneof().IsSynthetic():

			if f.Desc != f.Desc.ContainingOneof().Fields().Get(0) {
				// Only generate a field for the first oneof field.
				continue
			}

			field.RepeatKind = OneOfKind

			oneof := f.Desc.ContainingOneof()
			field.Oneof = &Oneof{
				FullName:     string(oneof.FullName()),
				PyName:       string(oneof.Name()),
				PbName:       string(oneof.Name()),
				PyPascalName: toPascalCase(string(oneof.Name())),
				Fields:       nil,
			}

			for i := 0; i < oneof.Fields().Len(); i++ {
				oofield := oneof.Fields().Get(i)
				field.Oneof.Fields = append(field.Oneof.Fields, Field{
					FullName:   string(oofield.FullName()),
					PyName:     string(oofield.Name()),
					PbName:     string(oofield.Name()),
					RepeatKind: OneOfKind,
					Oneof:      field.Oneof,
					ValueType:  toType(oofield),
				})
			}

			msg.Oneofs = append(msg.Oneofs, &field)

		default:
			field.RepeatKind = SingularKind
			field.ValueType = toType(f.Desc)
		}

		msg.Fields = append(msg.Fields, field)
	}

	return msg
}

func toPascalCase(s string) string {
	sb := strings.Builder{}
	for _, part := range strings.Split(s, "_") {
		for i, r := range part {
			if i == 0 {
				sb.WriteRune(unicode.ToUpper(r))
				continue
			}
			sb.WriteRune(r)
		}
	}
	return sb.String()
}

func toType(field protoreflect.FieldDescriptor) Type {
	kind := toKind(field)
	switch kind {
	case PrimitiveKind:
		pyprim := toPyPrimitive(field.Kind())
		default_ := pyDefault(pyprim)
		corePyType := string(pyprim)
		pytype := corePyType
		if field.HasPresence() {
			default_ = "None" //TODO probably handled elsewhere anyways
			pytype = "Optional[" + corePyType + "]"
		}

		return Type{
			Kind:        PrimitiveKind,
			HasPresence: field.HasPresence(),
			PyType:      pytype,
			CorePyType:  corePyType,
			PyDefault:   default_,
		}

	case MessageKind:
		switch field.Message().FullName() {
		case "google.protobuf.Any":
			return Type{
				Kind:       AnyKind,
				PyType:     "Any",
				CorePyType: "Any",
			}

		case "google.protobuf.DoubleValue", "google.protobuf.FloatValue":
			return Type{
				Kind:       WrapperKind,
				PyType:     "Optional[float]",
				CorePyType: "float",
			}

		case "google.protobuf.Int64Value", "google.protobuf.Int32Value", "google.protobuf.UInt64Value", "google.protobuf.UInt32Value":
			return Type{
				Kind:       WrapperKind,
				PyType:     "Optional[int]",
				CorePyType: "int",
			}

		case "google.protobuf.BoolValue":
			return Type{
				Kind:       WrapperKind,
				PyType:     "Optional[bool]",
				CorePyType: "bool",
			}

		case "google.protobuf.StringValue":
			return Type{
				Kind:       WrapperKind,
				PyType:     "Optional[str]",
				CorePyType: "str",
			}

		case "google.protobuf.BytesValue":
			return Type{
				Kind:       WrapperKind,
				PyType:     "Optional[bytes]",
				CorePyType: "bytes",
			}

		case "google.protobuf.Timestamp":
			return Type{
				Kind:       TimestampKind,
				PyType:     "Optional[google.protobuf.timestamp_pb2.Timestamp]",
				CorePyType: "google.protobuf.timestamp_pb2.Timestamp",
			}

		case "google.protobuf.Struct":
			return Type{
				Kind:       StructKind,
				PyType:     "Optional[dict[str,Any]]",
				CorePyType: "dict[str,Any]",
			}

		case "google.protobuf.ListValue":
			return Type{
				Kind:       StructKind,
				PyType:     "Optional[list[Any]]",
				CorePyType: "list[Any]",
			}

		case "google.protobuf.Value":
			// TODO? "Union[None, int, float, list, dict]" ?
			// Note google.protobuf.NullValue is an enum - so handled elsewhere
			return Type{
				Kind:       StructKind,
				PyType:     "Optional[Any]",
				CorePyType: "Any",
			}

		default:
			type_ := typeName(field, field.Message())
			return Type{
				Kind:       MessageKind,
				PyType:     type_,
				CorePyType: type_,
			}
		}

	case EnumKind:
		if field.Enum().FullName() == "google.protobuf.NullValue" {
			return Type{
				Kind:       NullValueKind,
				PyType:     "None",
				CorePyType: "None",
			}
		}

		type_ := typeName(field, field.Enum())
		t := Type{
			Kind:        EnumKind,
			HasPresence: field.HasPresence(),
			PyType:      type_,
			CorePyType:  type_,
			PyDefault:   type_ + "(0)",
		}
		if field.HasPresence() {
			t.PyDefault = "None"
			t.PyType = "Optional[" + type_ + "]"
		}

		return t
	}

	//TODO is this still reachable - how?
	return Type{} //TODO
}

// TODO code dupe?
func protopkg(pkg string) string {
	pkg = strings.Replace(pkg, "/", ".", -1)
	pkg = strings.TrimSuffix(pkg, ".proto")
	return pkg
}

func typeName(parent protoreflect.Descriptor, desc protoreflect.Descriptor) string {
	isImported := parent.ParentFile().Path() != desc.ParentFile().Path()
	if !isImported {
		return string(desc.Name())
	}
	return typeNameWithSuffix(desc, "_protodc")
}

func pb2TypeName(desc protoreflect.Descriptor) string {
	return typeNameWithSuffix(desc, "_pb2")
}

func typeNameWithSuffix(desc protoreflect.Descriptor, suffix string) string {

	path_ := desc.ParentFile().Path()
	path_ = strings.TrimSuffix(path_, ".proto")
	path_ = strings.ReplaceAll(path_, "/", ".")
	path_ += suffix + "." + string(desc.Name())

	return path_
}

func toKind(fd protoreflect.FieldDescriptor) Kind {
	if toPyPrimitive(fd.Kind()) != NotPyPrimitive {
		return PrimitiveKind
	}
	switch fd.Kind() {
	case protoreflect.EnumKind:
		return EnumKind
	case protoreflect.MessageKind:
		return MessageKind

	case protoreflect.GroupKind:
		debug(fd.FullName())
		panic("group kind not implemented. field: " + fd.FullName())

	default:
		debug(fd.FullName())
		panic("unexpected kind for field: " + fd.FullName())
	}
}

func pyDefault(pyprim PyPrimitive) string {
	switch pyprim {
	case PyInt:
		return "0"
	case PyFloat:
		return "0.0"
	case PyBool:
		return "False"
	case PyString:
		return `""`
	case PyBytes:
		return "bytes()"
	default:
		return "None"
	}
}

func toPyPrimitive(kind protoreflect.Kind) PyPrimitive {
	switch kind {
	case protoreflect.BoolKind:
		return PyBool

	case protoreflect.Int32Kind,
		protoreflect.Sint32Kind,
		protoreflect.Uint32Kind,
		protoreflect.Int64Kind,
		protoreflect.Sint64Kind,
		protoreflect.Uint64Kind,
		protoreflect.Sfixed32Kind,
		protoreflect.Fixed32Kind,
		protoreflect.Sfixed64Kind,
		protoreflect.Fixed64Kind:
		return PyInt

	case protoreflect.FloatKind,
		protoreflect.DoubleKind:
		return PyFloat

	case protoreflect.StringKind:
		return PyString

	case protoreflect.BytesKind:
		return PyBytes

	case protoreflect.EnumKind,
		protoreflect.MessageKind,
		protoreflect.GroupKind:
		return NotPyPrimitive

	default:
		return NotPyPrimitive
	}
}
