# `materials/gfx/`

The `materials/gfx/` directory holds materials for the heads up display and
other two dimensional interface elements.

The leading `materials/` component is supplied by the tooling and does not
appear in the zone definition. The remainder of the path, `gfx/`, forms part
of the asset name.

For example, the zone definition entry:

```
material,gfx/example
```

is built from `materials/gfx/example.json`.

The retail zones use entries such as:

```
material,gfx/icons/hud@mg42.tga
material,gfx/reticle/mg42_cross.tga
```

| | |
| --- | --- |
| Zone definition type | `material` |
| Retail occurrence | 16 of the 116 English zones |

See [the project layout](../../README.md) for how this directory fits into the
tree as a whole.
