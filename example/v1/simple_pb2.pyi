from example.other.v1 import other_pb2 as _other_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Bar(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    BAR_UNSPECIFIED: _ClassVar[Bar]
    BAR_WAT: _ClassVar[Bar]
BAR_UNSPECIFIED: Bar
BAR_WAT: Bar

class Foo(_message.Message):
    __slots__ = ["this_other"]
    THIS_OTHER_FIELD_NUMBER: _ClassVar[int]
    this_other: _other_pb2.Other
    def __init__(self, this_other: _Optional[_Union[_other_pb2.Other, _Mapping]] = ...) -> None: ...
