# `materials/fonts/`

The `materials/fonts/` directory holds the materials that font assets are
drawn with.

The leading `materials/` component is supplied by the tooling and does not
appear in the zone definition. The remainder of the path, `fonts/`, forms part
of the asset name.

For example, the zone definition entry:

```
material,fonts/example
```

is built from `materials/fonts/example.json`.

The retail zones use entries such as:

```
material,fonts/devfonts_pc
material,fonts/devfonts_pc_glow
material,fonts/gamefonts_pc
```

| | |
| --- | --- |
| Zone definition type | `material` |
| Extension | `.json` |
| Retail occurrence | 2 of the 116 English zones |

See [the project layout](../../README.md) for how this directory fits into the
tree as a whole.
