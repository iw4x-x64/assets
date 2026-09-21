# `maps/createfx/`

The `maps/createfx/` directory holds the generated scripts that place effects
within a map.

The asset name is the path itself. A zone definition entry therefore repeats
this directory and includes the file extension.

For example, the zone definition entry:

```
rawfile,maps/createfx/example.gsc
```

is built from `maps/createfx/example.gsc`.

The retail zones use entries such as:

```
rawfile,maps/createfx/af_caves_fx.gsc
rawfile,maps/createfx/af_chase_fx.gsc
rawfile,maps/createfx/airport_audio.gsc
```

| | |
| --- | --- |
| Zone definition type | `rawfile` |
| Extension | `.gsc` |
| Retail occurrence | 50 of the 116 English zones |

See [the project layout](../../README.md) for how this directory fits into the
tree as a whole.
