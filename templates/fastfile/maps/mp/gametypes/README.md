# `maps/mp/gametypes/`

The `maps/mp/gametypes/` directory holds the scripts implementing each
multiplayer gametype.

The asset name is the path itself. A zone definition entry therefore repeats
this directory and includes the file extension.

For example, the zone definition entry:

```
rawfile,maps/mp/gametypes/example.gsc
```

is built from `maps/mp/gametypes/example.gsc`.

The retail zones use entries such as:

```
rawfile,maps/mp/gametypes/_battlechatter_mp.gsc
rawfile,maps/mp/gametypes/_callbacksetup.gsc
rawfile,maps/mp/gametypes/_class.gsc
```

| | |
| --- | --- |
| Zone definition type | `rawfile` |
| Extension | `.gsc`, `.txt` |
| Retail occurrence | 3 of the 116 English zones |

See [the project layout](../../../README.md) for how this directory fits into
the tree as a whole.
