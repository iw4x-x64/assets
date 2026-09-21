# `maps/mp/`

The `maps/mp/` directory holds the scripts and tables belonging to multiplayer
levels.

The asset name is the path itself. A zone definition entry therefore repeats
this directory and includes the file extension.

For example, the zone definition entry:

```
rawfile,maps/mp/example.gsc
```

is built from `maps/mp/example.gsc`.

The retail zones use entries such as:

```
rawfile,maps/mp/_animatedmodels.gsc
rawfile,maps/mp/_areas.gsc
rawfile,maps/mp/_art.gsc
```

| | |
| --- | --- |
| Zone definition type | `rawfile` |
| Extension | `.gsc`, `.json`, `.ents` |
| Retail occurrence | 29 of the 116 English zones |

See [the project layout](../../README.md) for how this directory fits into the
tree as a whole.
