# `weapons/`

The `weapons/` directory holds weapon definitions, one extensionless file per
weapon, written in the key and value info string format. A definition covers
ammunition, handling, attachments, the models the weapon uses, and the sound
aliases and effects it plays.

The directory name is supplied by the tooling and does not appear in the zone
definition, which names the asset on its own.

For example, the zone definition entry:

```
weapon,aa12
```

is built from `weapons/aa12`.

A weapon refers to a considerable number of other assets by name, including
models, materials, sound aliases and effects, all of which must resolve for
the build to succeed.

Note that the accuracy graphs a weapon refers to are written to `accuracy/`
and are not listed in the zone definition themselves.

The retail zones use entries such as:

```
weapon,aa12
weapon,aa12_eotech_fmj_mp
```

| | |
| --- | --- |
| Zone definition type | `weapon` |
| Extension | none |
| Retail occurrence | 54 of the 116 English zones |

See [the project layout](../README.md) for how this directory fits into the
tree as a whole.
