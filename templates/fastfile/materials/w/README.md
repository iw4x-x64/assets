# `materials/w/`

The `materials/w/` directory holds materials serving a specific rendering
purpose, such as shadow casters.

The leading `materials/` component is supplied by the tooling and does not
appear in the zone definition. The remainder of the path, `w/`, forms part of
the asset name.

For example, the zone definition entry:

```
material,w/example
```

is built from `materials/w/example.json`.

The retail zones use entries such as:

```
material,w/shadowcaster
```

| | |
| --- | --- |
| Zone definition type | `material` |
| Extension | `.json` |
| Retail occurrence | 2 of the 116 English zones |

See [the project layout](../../README.md) for how this directory fits into the
tree as a whole.
