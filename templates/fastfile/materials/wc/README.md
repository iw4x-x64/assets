# `materials/wc/`

The `materials/wc/` directory holds materials related to world clipping and
collision.

The leading `materials/` component is supplied by the tooling and does not
appear in the zone definition. The remainder of the path, `wc/`, forms part of
the asset name.

For example, the zone definition entry:

```
material,wc/example
```

is built from `materials/wc/example.json`.

The retail zones use entries such as:

```
material,wc/$default3d
material,wc/747_window
material,wc/_default_water
```

| | |
| --- | --- |
| Zone definition type | `material` |
| Extension | `.json` |
| Retail occurrence | 51 of the 116 English zones |

See [the project layout](../../README.md) for how this directory fits into the
tree as a whole.
