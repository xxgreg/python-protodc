from google.protobuf import any_pb2 as _any_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import wrappers_pb2 as _wrappers_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Wat2(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    WAT2_UNSPECIFIED: _ClassVar[Wat2]
    WAT2_WAT: _ClassVar[Wat2]
WAT2_UNSPECIFIED: Wat2
WAT2_WAT: Wat2

class Map(_message.Message):
    __slots__ = ["str_by_str", "str_by_int", "enum_by_str", "msg_by_str", "timestamp_by_str", "wrapped_int_by_str", "struct_by_str", "any_by_str"]
    class StrByStrEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    class StrByIntEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: str
        def __init__(self, key: _Optional[int] = ..., value: _Optional[str] = ...) -> None: ...
    class EnumByStrEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: Wat2
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[Wat2, str]] = ...) -> None: ...
    class MsgByStrEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: Thing2
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[Thing2, _Mapping]] = ...) -> None: ...
    class TimestampByStrEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _timestamp_pb2.Timestamp
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...
    class WrappedIntByStrEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _wrappers_pb2.Int64Value
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[_wrappers_pb2.Int64Value, _Mapping]] = ...) -> None: ...
    class StructByStrEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _struct_pb2.Struct
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...
    class AnyByStrEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _any_pb2.Any
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[_any_pb2.Any, _Mapping]] = ...) -> None: ...
    STR_BY_STR_FIELD_NUMBER: _ClassVar[int]
    STR_BY_INT_FIELD_NUMBER: _ClassVar[int]
    ENUM_BY_STR_FIELD_NUMBER: _ClassVar[int]
    MSG_BY_STR_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_BY_STR_FIELD_NUMBER: _ClassVar[int]
    WRAPPED_INT_BY_STR_FIELD_NUMBER: _ClassVar[int]
    STRUCT_BY_STR_FIELD_NUMBER: _ClassVar[int]
    ANY_BY_STR_FIELD_NUMBER: _ClassVar[int]
    str_by_str: _containers.ScalarMap[str, str]
    str_by_int: _containers.ScalarMap[int, str]
    enum_by_str: _containers.ScalarMap[str, Wat2]
    msg_by_str: _containers.MessageMap[str, Thing2]
    timestamp_by_str: _containers.MessageMap[str, _timestamp_pb2.Timestamp]
    wrapped_int_by_str: _containers.MessageMap[str, _wrappers_pb2.Int64Value]
    struct_by_str: _containers.MessageMap[str, _struct_pb2.Struct]
    any_by_str: _containers.MessageMap[str, _any_pb2.Any]
    def __init__(self, str_by_str: _Optional[_Mapping[str, str]] = ..., str_by_int: _Optional[_Mapping[int, str]] = ..., enum_by_str: _Optional[_Mapping[str, Wat2]] = ..., msg_by_str: _Optional[_Mapping[str, Thing2]] = ..., timestamp_by_str: _Optional[_Mapping[str, _timestamp_pb2.Timestamp]] = ..., wrapped_int_by_str: _Optional[_Mapping[str, _wrappers_pb2.Int64Value]] = ..., struct_by_str: _Optional[_Mapping[str, _struct_pb2.Struct]] = ..., any_by_str: _Optional[_Mapping[str, _any_pb2.Any]] = ...) -> None: ...

class Thing2(_message.Message):
    __slots__ = ["wat"]
    WAT_FIELD_NUMBER: _ClassVar[int]
    wat: int
    def __init__(self, wat: _Optional[int] = ...) -> None: ...
