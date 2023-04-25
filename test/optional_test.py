from pprint import pprint

from example_usage.v1.optional_protodc import OptionalMsg, Wat4, Thing4


def empty_test():
    dc = OptionalMsg()
    pb = dc.to_protobuf()
    dc2 = OptionalMsg.from_protobuf(pb)

    pprint(dc)
    pprint(dc2)
    print(dc == dc2)


def primitive_test():
    dc = OptionalMsg(
        opt_int=1,
    )
    pb = dc.to_protobuf()
    dc2 = OptionalMsg.from_protobuf(pb)

    pprint(dc)
    pprint(dc2)
    print(dc == dc2)


def enum_test():
    dc = OptionalMsg(
        opt_enum=Wat4.WAT4_WAT,
    )
    pb = dc.to_protobuf()
    dc2 = OptionalMsg.from_protobuf(pb)

    pprint(dc)
    pprint(dc2)
    print(dc == dc2)


def msg_test():
    dc = OptionalMsg(
        opt_thing=Thing4(wat=22)
    )
    pb = dc.to_protobuf()
    dc2 = OptionalMsg.from_protobuf(pb)

    pprint(dc)
    pprint(dc2)
    print(dc == dc2)


empty_test()

primitive_test()

enum_test()

msg_test()
