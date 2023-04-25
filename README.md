# python-protodc

Generate idiomatic [Python dataclasses](https://docs.python.org/3/library/dataclasses.html) 
from a [protobuf schema](https://protobuf.dev/programming-guides/proto3/).

The generated Python dataclasses include `to`/`from_protobuf`, and 
`to`/`from_protojson` methods which allow converting between the dataclass and 
protobuf representations.

These methods depend on the modules generated by the official Python 
[protobuf generator](https://github.com/protocolbuffers/protobuf/tree/main/python).

This generator is intended to be used for APIs which need to instantly familiar 
to Python developers, and not forcing them to learn the quirks of the official 
Python protobuf API. If performance is a goal, I'd recommend sticking with the 
official Python protobuf API. If low friction APIs are more important, then give
this a shot.

If you're looking at this, you may also be interested in [protoplus](https://github.com/googleapis/proto-plus-python), 
[betterproto](https://github.com/danielgtaylor/python-betterproto), or [pure-protobuf](https://github.com/eigenein/protobuf/).


## Compatibility

Support for proto3 syntax. No support for proto2.

Supports well known types for wrappers, timestamp, any, and struct.

Currently no support for nested messages, nested enums, (send a PR, it should 
be easy to add), field masks or reflection types.


## Example

Schema [source](example/v1/example.proto)
```protobuf
message Example {
  int64 life_the_universe_and_everything = 1;
  repeated Example examples = 2;
  oneof wat {
    string javascript = 3;
    string golang = 4;
    Example another_example = 5;
  }
  google.protobuf.Timestamp time = 6;
}
```

Usage [source](test/example_usage.py)
```python
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
```

Generated Dataclass [source](example/v1/example_protodc.py)
```python
class ExampleWatOneof(enum.Enum):
    NONE = 0
    javascript = 1
    golang = 2
    another_example = 3

@dataclass
class Example:
    life_the_universe_and_everything: int = 0
    examples: list['Example'] = field(default_factory=list)
    which_wat: ExampleWatOneof = ExampleWatOneof.NONE
    wat: Union[None, 'str', 'str', 'Example'] = None
    time: Optional[datetime] = None

    def __post_init__(self):
        if self.wat is not None and self.which_wat in (None, ExampleWatOneof.NONE):
            raise Exception('example.v1.Example: which_wat not passed in constructor')

    def to_protojson(self):
        return google.protobuf.json_format.MessageToJson(self.to_protobuf())

    @staticmethod
    def from_protojson(json_str):
        pb = example.v1.example_pb2.Example()
        google.protobuf.json_format.Parse(json_str, pb)
        return Example.from_protobuf(pb)

    def to_protobuf(self, target_pb: google.protobuf.message.Message = None, depth: int = 0) -> 'example.v1.example_pb2.Example':
        if depth > 100:
            raise Exception('to_protobuf(): too much nesting in example.v1.Example: often caused by a circular reference.')

        if target_pb is not None:
            pb = target_pb
        else:
            pb = example.v1.example_pb2.Example()

        if self.life_the_universe_and_everything is not None:
            pb.life_the_universe_and_everything = self.life_the_universe_and_everything
        if self.examples is not None:
            for x in self.examples:
                x.to_protobuf(target_pb=pb.examples.add(), depth=depth+1)
        if self.which_wat is None or self.which_wat == ExampleWatOneof.NONE:
            pass
        elif self.which_wat == ExampleWatOneof.javascript:
            pb.javascript = self.wat
        elif self.which_wat == ExampleWatOneof.golang:
            pb.golang = self.wat
        elif self.which_wat == ExampleWatOneof.another_example:
            self.wat.to_protobuf(target_pb=pb.another_example, depth=depth+1)
        else:
            raise Exception('to_protobuf(): unexpected value for example.v1.Example.wat')

        if self.time is not None:
            pb.time.FromDatetime(self.time)

        return pb

    @staticmethod
    def from_protobuf(pb: 'example.v1.example_pb2.Example', depth: int = 0) -> 'Example':
        if depth > 100:
            raise Exception('from_protobuf(): too much nesting in example.v1.Example: often caused by a circular reference.')

        dc = Example()

        dc.life_the_universe_and_everything = pb.life_the_universe_and_everything
        dc.examples = [Example.from_protobuf(x, depth=depth+1) for x in pb.examples]
        oneof_field_name = pb.WhichOneof('wat')
        if oneof_field_name is None:
            pass
        elif oneof_field_name == 'javascript':
            dc.which_wat = ExampleWatOneof.javascript
            dc.wat = pb.javascript
        elif oneof_field_name == 'golang':
            dc.which_wat = ExampleWatOneof.golang
            dc.wat = pb.golang
        elif oneof_field_name == 'another_example':
            dc.which_wat = ExampleWatOneof.another_example
            dc.wat = Example.from_protobuf(pb.another_example, depth+1)
        else:
            raise Exception('from_protobuf(): unexpected value for example.v1.Example.wat')

        if pb.HasField('time'):
            dc.time = pb.time.ToDatetime()

        return dc

    @property
    def javascript(self) -> Optional['str']:
        if self.which_wat == ExampleWatOneof.javascript:
            return self.wat
        else:
            return None

    @javascript.setter
    def javascript(self, value: 'str'):
        self.which_wat = ExampleWatOneof.javascript
        self.wat = value

    @property
    def golang(self) -> Optional['str']:
        if self.which_wat == ExampleWatOneof.golang:
            return self.wat
        else:
            return None

    @golang.setter
    def golang(self, value: 'str'):
        self.which_wat = ExampleWatOneof.golang
        self.wat = value

    @property
    def another_example(self) -> Optional['Example']:
        if self.which_wat == ExampleWatOneof.another_example:
            return self.wat
        else:
            return None

    @another_example.setter
    def another_example(self, value: 'Example'):
        self.which_wat = ExampleWatOneof.another_example
        self.wat = value
```


## Install

Install the [Go toolchain](https://go.dev/doc/install).

Install the [buf build CLI](https://buf.build/docs/tutorials/getting-started-with-buf-cli/).

Copy `protodc/__init__.py` to the source root.

Configure your `buf.gen.yaml`. It should look like below.

This uses `go run` to download and compile the plugin from the source github.
```
version: v1
managed:
  enabled: true
  #FIXME This value isn't actually used but is the go protobuf compiler toolchain checks for it's presence.
  go_package_prefix:
    default: gen
plugins:
  - plugin: protoc-gen-python-protodc
    out: .
    # See tags for latest version in case I forget to update this - update the @v0.1.0 at the end.
    path: ["go", "run", "go run github.com/xxgreg/python-protodc/protoc-gen-python-protodc@v0.1.0"]
  - plugin: buf.build/protocolbuffers/python
    out: .
    opt: pyi_out=.
```


## Future Experiments

Experiment with generating protojson directly without the protobuf dependency.


## TODO

* actual documentation
* include doc strings in type
* generate protodc py package - perhaps a separate flag to run it in non generator mode?
* write actual python tests - automate with Makefile
* handle None in compound types - maybe ok already - check.
* Add comments for oneof fields in field list.
* Add a type check to oneof __post_init__ that the xxx value matches what's in which_xxx.
* autogenerate a register all function
* add some checks to register to catch typos
* get rid of go namespace option from plugin
* write actual python tests - automate with Makefile
* full nullkind support - weird!
* check error message quality - or at least document comment mistakes
* optional support in weird cases - what is an optional message vs standard message
* better avoidance of name collisions - start with import as __
* get rid of go namespace option from plugin
* non-root directory proto/output location
* nested enums and nested messages
* reflection types
* field masks
* what is "group kind"
* get rid of trailing spaces
