# `materials/m/`

The `materials/m/` directory holds shared and miscellaneous materials.

The leading `materials/` component is supplied by the tooling and does not
appear in the zone definition. The remainder of the path, `m/`, forms part of
the asset name.

For example, the zone definition entry:

```
material,m/example
```

is built from `materials/m/example.json`.

The retail zones use entries such as:

```
material,m/ap_glass_sanded
material,m/com_glass_clear
material,m/com_glass_clear_inside
```

| | |
| --- | --- |
| Zone definition type | `material` |
| Extension | `.json` |
| Retail occurrence | 42 of the 116 English zones |

See [the project layout](../../README.md) for how this directory fits into the
tree as a whole.
