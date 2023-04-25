from datetime import datetime
from pprint import pprint

import protodc

from example_usage.v1.map_protodc import Map, Wat2, Thing2
from example_usage.v1.map_pb2 import Map as PbMap, Thing2 as PbThing2


def empty_test():
    dc = Map()
    pb = dc.to_protobuf()
    dc2 = Map.from_protobuf(pb)

    pprint(dc)
    pprint(dc2)
    print(dc == dc2)


def primitive_test():
    dc = Map(
        str_by_str={'foo': 'bar'},
        str_by_int={1: 'foo'},
    )
    pb = dc.to_protobuf()
    dc2 = Map.from_protobuf(pb)

    pprint(dc)
    pprint(dc2)
    print(dc == dc2)


def enum_test():
    dc = Map(
        enum_by_str={
            'nope': Wat2.WAT2_UNSPECIFIED,
            'a': Wat2.WAT2_WAT,
            'b': Wat2.WAT2_WAT}
    )
    pb = dc.to_protobuf()
    dc2 = Map.from_protobuf(pb)

    pprint(dc)
    pprint(dc2)
    print(dc == dc2)


def msg_test():
    dc = Map(
        # FIXME support Nones as map values?
        msg_by_str={
            'a': Thing2(wat=42),
            'b': Thing2(wat=43),
        }
    )
    pb = dc.to_protobuf()
    dc2 = Map.from_protobuf(pb)

    pprint(dc)
    pprint(dc2)
    print(dc == dc2)


def wrapper_test():
    dc = Map(
        wrapped_int_by_str={
            'a': 42
        },
    )
    pb = dc.to_protobuf()
    dc2 = Map.from_protobuf(pb)

    pprint(dc)
    pprint(dc2)
    print(dc == dc2)


def timestamp_test():
    dc = Map(
        timestamp_by_str={
            'a': datetime.now(),
        }
    )
    pb = dc.to_protobuf()
    dc2 = Map.from_protobuf(pb)

    pprint(dc)
    pprint(dc2)
    print(dc == dc2)


def struct_test():
    dc = Map(
        struct_by_str={
            'a': {'b': {'c': 42.0}},
        }
    )
    pb = dc.to_protobuf()
    dc2 = Map.from_protobuf(pb)

    pprint(dc)
    pprint(dc2)
    print(dc == dc2)


def any_test():
    protodc.register("example.v1.Map", Map, PbMap)
    protodc.register("example.v1.Thing2", Thing2, PbThing2)
    dc = Map(any_by_str={'wat': Thing2(wat=12)})
    pb = dc.to_protobuf()
    dc2 = Map.from_protobuf(pb)

    pprint(dc)
    pprint(dc2)
    print(dc == dc2)


empty_test()

primitive_test()

enum_test()

msg_test()

wrapper_test()

timestamp_test()

struct_test()

any_test()
