from datetime import datetime
from pprint import pprint

import protodc
from example_usage.v1.singular_protodc import Singular, Wat3, Thing3
from example_usage.v1 import singular_pb2


def empty_test():
    dc = Singular()
    pb = dc.to_protobuf()
    dc2 = Singular.from_protobuf(pb)

    pprint(dc)
    pprint(dc2)
    print(dc == dc2)


def primitive_test():
    dc = Singular(
        the_str="abc",
        the_int=1,
        the_double=2.0,
    )
    pb = dc.to_protobuf()
    dc2 = Singular.from_protobuf(pb)

    pprint(dc)
    pprint(dc2)
    print(dc == dc2)


def enum_test():
    dc = Singular(
        the_enum=Wat3.WAT3_WAT
    )
    pb = dc.to_protobuf()
    dc2 = Singular.from_protobuf(pb)

    pprint(dc)
    pprint(dc2)
    print(dc == dc2)


def msg_test():
    dc = Singular(
        the_msg=Thing3(wat=12)
    )
    pb = dc.to_protobuf()
    dc2 = Singular.from_protobuf(pb)

    pprint(dc)
    pprint(dc2)
    print(dc == dc2)


def timestamp_test():
    dc = Singular(the_timestamp=datetime.now())
    pb = dc.to_protobuf()
    dc2 = Singular.from_protobuf(pb)

    pprint(dc)
    pprint(dc2)
    print(dc == dc2)


def wrapper_test():
    dc = Singular(the_wrapper=True)
    pb = dc.to_protobuf()
    dc2 = Singular.from_protobuf(pb)

    pprint(dc)
    pprint(dc2)
    print(dc == dc2)


def struct_test():
    dc = Singular(the_struct={'foo': {'bar': [42]}})
    pb = dc.to_protobuf()
    dc2 = Singular.from_protobuf(pb)

    pprint(dc)
    pprint(dc2)
    print(dc == dc2)


def any_test():
    protodc.register("example.v1.Thing3", Thing3, singular_pb2.Thing3)
    protodc.register("example.v1.Wat3", Wat3, singular_pb2.Wat3)

    dc = Singular(the_any=1)
    pb = dc.to_protobuf()
    dc2 = Singular.from_protobuf(pb)

    pprint(dc)
    pprint(dc2)
    print(dc == dc2)

    dc = Singular(the_any=Thing3(wat=42))
    pb = dc.to_protobuf()
    dc2 = Singular.from_protobuf(pb)

    pprint(dc)
    pprint(dc2)
    print(dc == dc2)

    # Assert failure
    # dc = Singular(the_any=Wat3.WAT3_WAT)
    # pb = dc.to_protobuf()
    # dc2 = Singular.from_protobuf(pb)
    #
    # pprint(dc)
    # pprint(dc2)
    # print(dc == dc2)

    # Assert failure - enum in list
    # dc = Singular(the_any=[Wat3.WAT3_WAT, Thing3(wat=42)])
    # pb = dc.to_protobuf()
    # dc2 = Singular.from_protobuf(pb)
    #
    # pprint(dc)
    # pprint(dc2)
    # print(dc == dc2)


# empty_test()
#
# primitive_test()
#
# enum_test()
#
# msg_test()
#
# timestamp_test()
#
# wrapper_test()
#
# struct_test()

any_test()
