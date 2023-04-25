from datetime import datetime

from example.v1.example_protodc import Example, ExampleWatOneof as Oneof

dc = Example(
    life_the_universe_and_everything=42,
    examples=[
        Example(life_the_universe_and_everything=43),
    ],
    time=datetime.now()
)

dc.javascript = "eval('while(true){}')"

# Round trip to JSON and back.
txt = dc.to_protojson()
dc2 = Example.from_protojson(txt)

# Round trip to a python protobuf and back.
pb = dc.to_protobuf()
dc3 = Example.from_protobuf(pb)

# Check that nothing was lost in translation...
print(dc == dc2 == dc3)

