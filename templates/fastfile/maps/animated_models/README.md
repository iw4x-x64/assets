# `maps/animated_models/`

The `maps/animated_models/` directory holds the scripts that drive animated
models placed in a map.

The asset name is the path itself. A zone definition entry therefore repeats
this directory and includes the file extension.

For example, the zone definition entry:

```
rawfile,maps/animated_models/example.gsc
```

is built from `maps/animated_models/example.gsc`.

The retail zones use entries such as:

```
rawfile,maps/animated_models/accessories_windsock_wind_medium.gsc
rawfile,maps/animated_models/com_roofvent2.gsc
rawfile,maps/animated_models/ferris_wheel.gsc
```

| | |
| --- | --- |
| Zone definition type | `rawfile` |
| Extension | `.gsc` |
| Retail occurrence | 26 of the 116 English zones |

See [the project layout](../../README.md) for how this directory fits into the
tree as a whole.
