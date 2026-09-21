# `vertexdecl/`

The `vertexdecl/` directory holds vertex declarations, which describe how
vertex data is laid out for a given technique. They are represented as JSON
because no original source format for them is known.

The directory name is supplied by the tooling and does not appear in the zone
definition, which names the asset on its own.

For example, the zone definition entry:

```
vertexdecl,pp
```

is built from `vertexdecl/pp.json`.

The retail zones use entries such as:

```
vertexdecl,,pp
vertexdecl,pp
```

| | |
| --- | --- |
| Zone definition type | `vertexdecl` |
| Extension | `.json` |
| Retail occurrence | 96 of the 116 English zones |

See [the project layout](../README.md) for how this directory fits into the
tree as a whole.
