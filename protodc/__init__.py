import enum
from dataclasses import dataclass
from typing import Any

from google.protobuf import wrappers_pb2
from google.protobuf import json_format

_wrapped_types_by_full_name = {
    'google.protobuf.StringValue': wrappers_pb2.StringValue,
    'google.protobuf.Int64Value': wrappers_pb2.Int64Value,
    'google.protobuf.Int32Value': wrappers_pb2.Int32Value,
    'google.protobuf.UInt64Value': wrappers_pb2.UInt64Value,
    'google.protobuf.UInt32Value': wrappers_pb2.UInt32Value,
    'google.protobuf.BoolValue': wrappers_pb2.BoolValue,
    'google.protobuf.DoubleValue': wrappers_pb2.DoubleValue,
    'google.protobuf.FloatValue': wrappers_pb2.FloatValue,
    'google.protobuf.BytesValue': wrappers_pb2.BytesValue,
}


_types_by_full_name: dict = {}


@dataclass
class _TypeDef:
    fullname: str
    dataclass: type
    protobuf: type


def register(fullname: str, dataclass: type, protobuf: type):
    _types_by_full_name[fullname] = _TypeDef(fullname=fullname, dataclass=dataclass, protobuf=protobuf)


def pack_any(val, any_pb, depth):
    if val is None:
        any_pb.Pack(None)

    elif hasattr(val, 'to_protobuf'):
        any_pb.Pack(val.to_protobuf(depth=depth+1))

    elif type(val) is int:
        any_pb.Pack(wrappers_pb2.Int64Value(value=val))

    elif type(val) is str:
        any_pb.Pack(wrappers_pb2.StringValue(value=val))

    elif type(val) is bool:
        any_pb.Pack(wrappers_pb2.BoolValue(value=val))

    elif type(val) is float:
        any_pb.Pack(wrappers_pb2.DoubleValue(value=val))

    elif type(val) is bytes:
        any_pb.Pack(wrappers_pb2.BytesValue(value=val))

    else:
        raise Exception("protodc: unknown message type " + any_pb.TypeName() + " : perhaps missing a call to protodc.register() or not a message type")


def unpack_any(any_pb, depth) -> Any:
    if any_pb is None:
        return None

    full_name = any_pb.TypeName()
    type_ = _wrapped_types_by_full_name.get(full_name)

    if type_ is not None:
        pb = type_()
        any_pb.Unpack(pb)
        return pb.value

    type_ = _types_by_full_name.get(full_name)

    if type_ is None:
        raise Exception("protodc: unknown type " + any_pb.TypeName() + " : perhaps missing a call to protodc.register() ")

    pb = type_.protobuf()
    any_pb.Unpack(pb)
    return type_.dataclass.from_protobuf(pb, depth=depth+1)
