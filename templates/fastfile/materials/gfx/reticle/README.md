# `materials/gfx/reticle/`

The `materials/gfx/reticle/` directory holds materials for weapon reticles.

The leading `materials/` component is supplied by the tooling and does not
appear in the zone definition. The remainder of the path, `gfx/reticle/`,
forms part of the asset name.

For example, the zone definition entry:

```
material,gfx/reticle/example
```

is built from `materials/gfx/reticle/example.json`.

The retail zones use entries such as:

```
material,gfx/reticle/mg42_cross.tga
```

| | |
| --- | --- |
| Zone definition type | `material` |
| Extension | `.json` |
| Retail occurrence | 2 of the 116 English zones |

See [the project layout](../../../README.md) for how this directory fits into
the tree as a whole.
