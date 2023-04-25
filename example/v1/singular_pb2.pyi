from google.protobuf import any_pb2 as _any_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import wrappers_pb2 as _wrappers_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Wat3(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    WAT3_UNSPECIFIED: _ClassVar[Wat3]
    WAT3_WAT: _ClassVar[Wat3]
WAT3_UNSPECIFIED: Wat3
WAT3_WAT: Wat3

class Singular(_message.Message):
    __slots__ = ["the_str", "the_int", "the_double", "the_enum", "the_msg", "the_null", "the_timestamp", "the_wrapper", "the_struct", "the_any"]
    THE_STR_FIELD_NUMBER: _ClassVar[int]
    THE_INT_FIELD_NUMBER: _ClassVar[int]
    THE_DOUBLE_FIELD_NUMBER: _ClassVar[int]
    THE_ENUM_FIELD_NUMBER: _ClassVar[int]
    THE_MSG_FIELD_NUMBER: _ClassVar[int]
    THE_NULL_FIELD_NUMBER: _ClassVar[int]
    THE_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    THE_WRAPPER_FIELD_NUMBER: _ClassVar[int]
    THE_STRUCT_FIELD_NUMBER: _ClassVar[int]
    THE_ANY_FIELD_NUMBER: _ClassVar[int]
    the_str: str
    the_int: int
    the_double: float
    the_enum: Wat3
    the_msg: Thing3
    the_null: _struct_pb2.NullValue
    the_timestamp: _timestamp_pb2.Timestamp
    the_wrapper: _wrappers_pb2.BoolValue
    the_struct: _struct_pb2.Struct
    the_any: _any_pb2.Any
    def __init__(self, the_str: _Optional[str] = ..., the_int: _Optional[int] = ..., the_double: _Optional[float] = ..., the_enum: _Optional[_Union[Wat3, str]] = ..., the_msg: _Optional[_Union[Thing3, _Mapping]] = ..., the_null: _Optional[_Union[_struct_pb2.NullValue, str]] = ..., the_timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., the_wrapper: _Optional[_Union[_wrappers_pb2.BoolValue, _Mapping]] = ..., the_struct: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., the_any: _Optional[_Union[_any_pb2.Any, _Mapping]] = ...) -> None: ...

class Thing3(_message.Message):
    __slots__ = ["wat"]
    WAT_FIELD_NUMBER: _ClassVar[int]
    wat: int
    def __init__(self, wat: _Optional[int] = ...) -> None: ...
