import enum
from dataclasses import dataclass, field
from typing import Any, Optional, Union
import google.protobuf.message
import google.protobuf.json_format
import protodc
from datetime import datetime

import example.other.v1.other_pb2


class OtherEnum(enum.Enum):
    OTHER_ENUM_NA = 0
    OTHER_ENUM_WAT = 1



@dataclass
class Other:
    wat: int = 0

    def to_protobuf(self, target_pb: google.protobuf.message.Message = None, depth: int = 0) -> 'example.other.v1.other_pb2.Other':
        if depth > 100:
            raise Exception('to_protobuf(): too much nesting in example.other.v1.Other: often caused by a circular reference.')

        if target_pb is not None:
            pb = target_pb
        else:
            pb = example.other.v1.other_pb2.Other()

        if self.wat is not None:
            pb.wat = self.wat

        return pb

    @staticmethod
    def from_protobuf(pb: 'example.other.v1.other_pb2.Other', depth: int = 0) -> 'Other':
        if depth > 100:
            raise Exception('from_protobuf(): too much nesting in example.other.v1.Other: often caused by a circular reference.')

        dc = Other()
        dc.wat = pb.wat
        return dc

