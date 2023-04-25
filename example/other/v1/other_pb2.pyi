from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class OtherEnum(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    OTHER_ENUM_NA: _ClassVar[OtherEnum]
    OTHER_ENUM_WAT: _ClassVar[OtherEnum]
OTHER_ENUM_NA: OtherEnum
OTHER_ENUM_WAT: OtherEnum

class Other(_message.Message):
    __slots__ = ["wat"]
    WAT_FIELD_NUMBER: _ClassVar[int]
    wat: int
    def __init__(self, wat: _Optional[int] = ...) -> None: ...
