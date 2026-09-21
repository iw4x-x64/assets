# `fx/`

The `fx/` directory holds effect definitions, one file per `FxEffectDef`
asset. Effects are grouped into the category subdirectories listed below.

The directory name is supplied by the tooling and does not appear in the zone
definition, which names the asset on its own.

For example, the zone definition entry:

```
fx,breakables/exp_wall_cinderblock_96
```

is built from `fx/breakables/exp_wall_cinderblock_96.efx`.

Note that the category subdirectory forms part of the asset name while `fx/`
itself does not. Writing `fx,fx/breakables/...` will not resolve.

Effects refer to materials and models by name, so the corresponding entries
belong in the same zone definition unless a loaded zone supplies them.

The retail zones use entries such as:

```
fx,breakables/exp_wall_cinderblock_96
fx,code/glass_shatter_32x32
```

| | |
| --- | --- |
| Zone definition type | `fx` |
| Retail occurrence | 70 of the 116 English zones |

See [the project layout](../README.md) for how this directory fits into the
tree as a whole.
