from datetime import datetime
from pprint import pprint

import protodc

from example_usage.v1.oneof_protodc import Oneof, Wat5, Thing5, OneofOneStuffOneof, OneofAllStuffOneof
from example_usage.v1.oneof_pb2 import Oneof as PbOneof, Thing5 as PbThing5


def empty_test():
    dc = Oneof()
    pb = dc.to_protobuf()
    dc2 = Oneof.from_protobuf(pb)

    pprint(dc)
    pprint(dc2)
    print(dc == dc2)


def one_test():
    dc = Oneof(
        which_one_stuff=OneofOneStuffOneof.int_stuff,
        one_stuff=42,
    )
    pb = dc.to_protobuf()
    dc2 = Oneof.from_protobuf(pb)

    pprint(dc)
    pprint(dc2)
    print(dc == dc2)


def more_one_test():
    dc = Oneof(
        which_all_stuff=OneofAllStuffOneof.and_more_int,
        all_stuff=12,
    )
    pb = dc.to_protobuf()
    dc2 = Oneof.from_protobuf(pb)

    pprint(dc)
    pprint(dc2)
    print(dc == dc2)

    dc.wat = Wat5.WAT5_WAT
    pb = dc.to_protobuf()
    dc2 = Oneof.from_protobuf(pb)

    pprint(dc)
    pprint(dc2)
    print(dc == dc2)

    dc.thing = Thing5(wat=12)
    pb = dc.to_protobuf()
    dc2 = Oneof.from_protobuf(pb)

    pprint(dc)
    pprint(dc2)
    print(dc == dc2)


def wrapper_test():
    dc = Oneof(
        which_all_stuff=Oneofall_stuffOneof.the_wrapper,
        all_stuff=True,
    )
    pb = dc.to_protobuf()
    dc2 = Oneof.from_protobuf(pb)

    pprint(dc)
    pprint(dc2)
    print(dc == dc2)


def struct_test():
    dc = Oneof(
        which_all_stuff=Oneofall_stuffOneof.the_struct,
        all_stuff={"foo": {"bar": 12.0}},
    )
    pb = dc.to_protobuf()
    dc2 = Oneof.from_protobuf(pb)

    pprint(dc)
    pprint(dc2)
    print(dc == dc2)


def timestamp_test():
    dc = Oneof(
        which_all_stuff=Oneofall_stuffOneof.the_timestamp,
        all_stuff=datetime.now(),
    )
    pb = dc.to_protobuf()
    dc2 = Oneof.from_protobuf(pb)

    pprint(dc)
    pprint(dc2)
    print(dc == dc2)


def any_test():
    protodc.register("example.v1.Thing5", Thing5, PbThing5)
    dc = Oneof(
        which_all_stuff=Oneofall_stuffOneof.the_any,
        all_stuff=Thing5(wat=4),
    )
    pb = dc.to_protobuf()
    dc2 = Oneof.from_protobuf(pb)

    pprint(dc)
    pprint(dc2)
    print(dc == dc2)


empty_test()

one_test()

more_one_test()

wrapper_test()

struct_test()

timestamp_test()

any_test()
