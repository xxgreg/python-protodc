from google.protobuf import any_pb2 as _any_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import wrappers_pb2 as _wrappers_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Wat(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    WAT_UNSPECIFIED: _ClassVar[Wat]
    WAT_WAT: _ClassVar[Wat]
WAT_UNSPECIFIED: Wat
WAT_WAT: Wat

class Repeated(_message.Message):
    __slots__ = ["the_int", "the_enums", "the_msg", "the_timestamps", "the_anys", "the_strs", "the_structs"]
    THE_INT_FIELD_NUMBER: _ClassVar[int]
    THE_ENUMS_FIELD_NUMBER: _ClassVar[int]
    THE_MSG_FIELD_NUMBER: _ClassVar[int]
    THE_TIMESTAMPS_FIELD_NUMBER: _ClassVar[int]
    THE_ANYS_FIELD_NUMBER: _ClassVar[int]
    THE_STRS_FIELD_NUMBER: _ClassVar[int]
    THE_STRUCTS_FIELD_NUMBER: _ClassVar[int]
    the_int: _containers.RepeatedScalarFieldContainer[int]
    the_enums: _containers.RepeatedScalarFieldContainer[Wat]
    the_msg: _containers.RepeatedCompositeFieldContainer[Thing]
    the_timestamps: _containers.RepeatedCompositeFieldContainer[_timestamp_pb2.Timestamp]
    the_anys: _containers.RepeatedCompositeFieldContainer[_any_pb2.Any]
    the_strs: _containers.RepeatedCompositeFieldContainer[_wrappers_pb2.StringValue]
    the_structs: _containers.RepeatedCompositeFieldContainer[_struct_pb2.Struct]
    def __init__(self, the_int: _Optional[_Iterable[int]] = ..., the_enums: _Optional[_Iterable[_Union[Wat, str]]] = ..., the_msg: _Optional[_Iterable[_Union[Thing, _Mapping]]] = ..., the_timestamps: _Optional[_Iterable[_Union[_timestamp_pb2.Timestamp, _Mapping]]] = ..., the_anys: _Optional[_Iterable[_Union[_any_pb2.Any, _Mapping]]] = ..., the_strs: _Optional[_Iterable[_Union[_wrappers_pb2.StringValue, _Mapping]]] = ..., the_structs: _Optional[_Iterable[_Union[_struct_pb2.Struct, _Mapping]]] = ...) -> None: ...

class Thing(_message.Message):
    __slots__ = ["wat"]
    WAT_FIELD_NUMBER: _ClassVar[int]
    wat: int
    def __init__(self, wat: _Optional[int] = ...) -> None: ...
