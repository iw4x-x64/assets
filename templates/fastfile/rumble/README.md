# `rumble/`

The `rumble/` directory holds rumble definitions, which describe controller
vibration patterns and are referred to by weapons and effects.

The asset name is the path itself. A zone definition entry therefore repeats
this directory and includes the file extension.

For example, the zone definition entry:

```
rawfile,rumble/example.rmb
```

is built from `rumble/example.rmb`.

The retail zones use entries such as:

```
rawfile,rumble/ac130_105mm_fire
rawfile,rumble/ac130_25mm_fire
rawfile,rumble/ac130_40mm_fire
```

| | |
| --- | --- |
| Zone definition type | `rawfile` |
| Extension | `.rmb`, none |
| Retail occurrence | 26 of the 116 English zones |

See [the project layout](../README.md) for how this directory fits into the
tree as a whole.
