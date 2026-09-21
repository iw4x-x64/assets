# `materials/mc/`

The `materials/mc/` directory holds materials applied to world geometry and
models, which make up the bulk of a zone's material set.

The leading `materials/` component is supplied by the tooling and does not
appear in the zone definition. The remainder of the path, `mc/`, forms part of
the asset name.

For example, the zone definition entry:

```
material,mc/example
```

is built from `materials/mc/example.json`.

The retail zones use entries such as:

```
material,mc/airplane_metal_01
material,mc/airport_wood_tile_black
material,mc/ap_chrome
```

| | |
| --- | --- |
| Zone definition type | `material` |
| Extension | `.json` |
| Retail occurrence | 73 of the 116 English zones |

See [the project layout](../../README.md) for how this directory fits into the
tree as a whole.
