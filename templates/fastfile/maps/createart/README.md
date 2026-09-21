# `maps/createart/`

The `maps/createart/` directory holds the generated art scripts that set up
vision, sun and fog for a map.

The asset name is the path itself. A zone definition entry therefore repeats
this directory and includes the file extension.

For example, the zone definition entry:

```
rawfile,maps/createart/example.gsc
```

is built from `maps/createart/example.gsc`.

The retail zones use entries such as:

```
rawfile,maps/createart/af_caves_fog.gsc
rawfile,maps/createart/af_chase_fog.gsc
rawfile,maps/createart/airport_art.gsc
```

| | |
| --- | --- |
| Zone definition type | `rawfile` |
| Extension | `.gsc` |
| Retail occurrence | 46 of the 116 English zones |

See [the project layout](../../README.md) for how this directory fits into the
tree as a whole.
