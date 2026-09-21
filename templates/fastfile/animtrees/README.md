# `animtrees/`

The `animtrees/` directory holds animation trees, which declare the animation
state hierarchy that script and models select animations from.

The asset name is the path itself. A zone definition entry therefore repeats
this directory and includes the file extension.

For example, the zone definition entry:

```
rawfile,animtrees/example.atr
```

is built from `animtrees/example.atr`.

The retail zones use entries such as:

```
rawfile,animtrees/ac130.atr
rawfile,animtrees/animated_props.atr
rawfile,animtrees/animation_rig_largegroup20.atr
```

| | |
| --- | --- |
| Zone definition type | `rawfile` |
| Extension | `.atr` |
| Retail occurrence | 27 of the 116 English zones |

See [the project layout](../README.md) for how this directory fits into the
tree as a whole.
