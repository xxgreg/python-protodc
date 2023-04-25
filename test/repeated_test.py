from datetime import datetime
from pprint import pprint

import protodc
from example_usage.v1.repeated_protodc import Repeated, Wat, Thing
from example_usage.v1.repeated_pb2 import Repeated as PbRepeated, Thing as PbThing


def empty_test():
    dc = Repeated()
    pb = dc.to_protobuf()
    dc2 = Repeated.from_protobuf(pb)

    pprint(dc)
    pprint(dc2)
    print(dc == dc2)


def primitive_test():
    dc = Repeated(
        the_int=[1, 2, 3]
    )
    pb = dc.to_protobuf()
    dc2 = Repeated.from_protobuf(pb)

    pprint(dc)
    pprint(dc2)
    print(dc == dc2)


def enum_test():
    dc = Repeated(
        the_enums=[Wat.WAT_UNSPECIFIED, Wat.WAT_WAT, Wat.WAT_WAT]
    )
    pb = dc.to_protobuf()
    dc2 = Repeated.from_protobuf(pb)

    pprint(dc)
    pprint(dc2)
    print(dc == dc2)


def msg_test():
    dc = Repeated(
        # FIXME support Nones in the list?
        # i.e. the_msg=[Thing(wat=42), None, Thing(wat=43)]
        the_msg=[Thing(wat=42), Thing(wat=43)]
    )
    pb = dc.to_protobuf()
    dc2 = Repeated.from_protobuf(pb)

    pprint(dc)
    pprint(dc2)
    print(dc == dc2)


def timestamp_test():
    dc = Repeated(the_timestamps=[datetime.now()])
    pb = dc.to_protobuf()
    dc2 = Repeated.from_protobuf(pb)

    pprint(dc)
    pprint(dc2)
    print(dc == dc2)


def any_test():
    protodc.register("example.v1.Repeated", Repeated, PbRepeated)
    protodc.register("example.v1.Thing", Thing, PbThing)
    dc = Repeated(the_anys=[Thing(wat=12)])
    pb = dc.to_protobuf()
    dc2 = Repeated.from_protobuf(pb)

    pprint(dc)
    pprint(dc2)
    print(dc == dc2)


def wrapper_test():
    dc = Repeated(the_strs=["a", "b", "c"])
    pb = dc.to_protobuf()
    dc2 = Repeated.from_protobuf(pb)

    pprint(dc)
    pprint(dc2)
    print(dc == dc2)


def struct_test():
    dc = Repeated(the_structs=[{"a": {"b": 42.0}}])
    pb = dc.to_protobuf()
    dc2 = Repeated.from_protobuf(pb)

    pprint(dc)
    pprint(dc2)
    print(dc == dc2)


empty_test()

enum_test()

msg_test()

timestamp_test()

any_test()

wrapper_test()

struct_test()
