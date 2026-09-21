# `impactfx/`

The `impactfx/` directory holds impact effect tables in JSON form. A table
maps a surface type and weapon class to the effect played when the two meet.
Any effect named in a table must be present in `fx/`.

The directory name is supplied by the tooling and does not appear in the zone
definition, which names the asset on its own.

For example, the zone definition entry:

```
impactfx,default
```

is built from `impactfx/default.json`.

The retail zones use entries such as:

```
impactfx,""
impactfx,default
```

| | |
| --- | --- |
| Zone definition type | `impactfx` |
| Extension | `.json` |
| Retail occurrence | 37 of the 116 English zones |

See [the project layout](../README.md) for how this directory fits into the
tree as a whole.
