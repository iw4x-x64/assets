# `xanim/`

The `xanim/` directory holds animation data, one extensionless file per
`XAnimParts` asset. Animations are referred to by name from models, from the
animation trees in `animtrees/`, and from script.

The directory name is supplied by the tooling and does not appear in the zone
definition, which names the asset on its own.

For example, the zone definition entry:

```
xanim,abrams_movement
```

is built from `xanim/abrams_movement`.

The retail zones use entries such as:

```
xanim,abrams_movement
xanim,abrams_movement_backwards
```

| | |
| --- | --- |
| Zone definition type | `xanim` |
| Extension | none |
| Retail occurrence | 70 of the 116 English zones |

See [the project layout](../README.md) for how this directory fits into the
tree as a whole.
