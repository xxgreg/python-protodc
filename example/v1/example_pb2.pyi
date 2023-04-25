from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Example(_message.Message):
    __slots__ = ["life_the_universe_and_everything", "examples", "javascript", "golang", "another_example", "time"]
    LIFE_THE_UNIVERSE_AND_EVERYTHING_FIELD_NUMBER: _ClassVar[int]
    EXAMPLES_FIELD_NUMBER: _ClassVar[int]
    JAVASCRIPT_FIELD_NUMBER: _ClassVar[int]
    GOLANG_FIELD_NUMBER: _ClassVar[int]
    ANOTHER_EXAMPLE_FIELD_NUMBER: _ClassVar[int]
    TIME_FIELD_NUMBER: _ClassVar[int]
    life_the_universe_and_everything: int
    examples: _containers.RepeatedCompositeFieldContainer[Example]
    javascript: str
    golang: str
    another_example: Example
    time: _timestamp_pb2.Timestamp
    def __init__(self, life_the_universe_and_everything: _Optional[int] = ..., examples: _Optional[_Iterable[_Union[Example, _Mapping]]] = ..., javascript: _Optional[str] = ..., golang: _Optional[str] = ..., another_example: _Optional[_Union[Example, _Mapping]] = ..., time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...
