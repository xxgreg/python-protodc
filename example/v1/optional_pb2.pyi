from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Wat4(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    WAT4_UNSPECIFIED: _ClassVar[Wat4]
    WAT4_WAT: _ClassVar[Wat4]
WAT4_UNSPECIFIED: Wat4
WAT4_WAT: Wat4

class OptionalMsg(_message.Message):
    __slots__ = ["opt_int", "opt_enum", "opt_thing"]
    OPT_INT_FIELD_NUMBER: _ClassVar[int]
    OPT_ENUM_FIELD_NUMBER: _ClassVar[int]
    OPT_THING_FIELD_NUMBER: _ClassVar[int]
    opt_int: int
    opt_enum: Wat4
    opt_thing: Thing4
    def __init__(self, opt_int: _Optional[int] = ..., opt_enum: _Optional[_Union[Wat4, str]] = ..., opt_thing: _Optional[_Union[Thing4, _Mapping]] = ...) -> None: ...

class Thing4(_message.Message):
    __slots__ = ["wat"]
    WAT_FIELD_NUMBER: _ClassVar[int]
    wat: int
    def __init__(self, wat: _Optional[int] = ...) -> None: ...
