# `aim_assist/`

The `aim_assist/` directory holds aim assist curves, which describe how aim
slowdown and magnetism behave with range.

The asset name is the path itself. A zone definition entry therefore repeats
this directory and includes the file extension.

For example, the zone definition entry:

```
rawfile,aim_assist/example.graph
```

is built from `aim_assist/example.graph`.

A weapon also refers to its aim assist curve by name, but the curve itself is
carried as a rawfile rather than as a sub-asset.

The retail zones use entries such as:

```
rawfile,aim_assist/view_input_0.graph
rawfile,aim_assist/view_input_1.graph
rawfile,aim_assist/view_input_2.graph
```

| | |
| --- | --- |
| Zone definition type | `rawfile` |
| Extension | `.graph` |
| Retail occurrence | 2 of the 116 English zones |

See [the project layout](../README.md) for how this directory fits into the
tree as a whole.
