# `mptype/`

The `mptype/` directory holds the scripts defining multiplayer character
types.

The asset name is the path itself. A zone definition entry therefore repeats
this directory and includes the file extension.

For example, the zone definition entry:

```
rawfile,mptype/example.gsc
```

is built from `mptype/example.gsc`.

The retail zones use entries such as:

```
rawfile,mptype/mptype_ally_ghillie_arctic.gsc
rawfile,mptype/mptype_ally_ghillie_desert.gsc
rawfile,mptype/mptype_ally_ghillie_forest.gsc
```

| | |
| --- | --- |
| Zone definition type | `rawfile` |
| Extension | `.gsc` |
| Retail occurrence | 1 of the 116 English zones |

See [the project layout](../README.md) for how this directory fits into the
tree as a whole.
