# `materials/gfx/icons/`

The `materials/gfx/icons/` directory holds materials for heads up display
icons.

The leading `materials/` component is supplied by the tooling and does not
appear in the zone definition. The remainder of the path, `gfx/icons/`, forms
part of the asset name.

For example, the zone definition entry:

```
material,gfx/icons/example
```

is built from `materials/gfx/icons/example.json`.

The retail zones use entries such as:

```
material,gfx/icons/hud@mg42.tga
```

| | |
| --- | --- |
| Zone definition type | `material` |
| Extension | `.json` |
| Retail occurrence | 14 of the 116 English zones |

See [the project layout](../../../README.md) for how this directory fits into
the tree as a whole.
