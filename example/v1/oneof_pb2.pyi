from google.protobuf import any_pb2 as _any_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import wrappers_pb2 as _wrappers_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Wat5(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    WAT5_UNSPECIFIED: _ClassVar[Wat5]
    WAT5_WAT: _ClassVar[Wat5]
WAT5_UNSPECIFIED: Wat5
WAT5_WAT: Wat5

class Oneof(_message.Message):
    __slots__ = ["int_stuff", "more_int", "and_more_int", "wat", "thing", "the_timestamp", "the_wrapper", "the_struct", "the_any"]
    INT_STUFF_FIELD_NUMBER: _ClassVar[int]
    MORE_INT_FIELD_NUMBER: _ClassVar[int]
    AND_MORE_INT_FIELD_NUMBER: _ClassVar[int]
    WAT_FIELD_NUMBER: _ClassVar[int]
    THING_FIELD_NUMBER: _ClassVar[int]
    THE_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    THE_WRAPPER_FIELD_NUMBER: _ClassVar[int]
    THE_STRUCT_FIELD_NUMBER: _ClassVar[int]
    THE_ANY_FIELD_NUMBER: _ClassVar[int]
    int_stuff: int
    more_int: int
    and_more_int: int
    wat: Wat5
    thing: Thing5
    the_timestamp: _timestamp_pb2.Timestamp
    the_wrapper: _wrappers_pb2.BoolValue
    the_struct: _struct_pb2.Struct
    the_any: _any_pb2.Any
    def __init__(self, int_stuff: _Optional[int] = ..., more_int: _Optional[int] = ..., and_more_int: _Optional[int] = ..., wat: _Optional[_Union[Wat5, str]] = ..., thing: _Optional[_Union[Thing5, _Mapping]] = ..., the_timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., the_wrapper: _Optional[_Union[_wrappers_pb2.BoolValue, _Mapping]] = ..., the_struct: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., the_any: _Optional[_Union[_any_pb2.Any, _Mapping]] = ...) -> None: ...

class Thing5(_message.Message):
    __slots__ = ["wat"]
    WAT_FIELD_NUMBER: _ClassVar[int]
    wat: int
    def __init__(self, wat: _Optional[int] = ...) -> None: ...
