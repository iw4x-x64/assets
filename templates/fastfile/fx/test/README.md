# `fx/test/`

The `fx/test/` directory holds effects used during development. The category
forms part of the asset name while `fx/` does not.

The leading `fx/` component is supplied by the tooling and does not appear in
the zone definition. The remainder of the path, `test/`, forms part of the
asset name.

For example, the zone definition entry:

```
fx,test/example
```

is built from `fx/test/example.efx`.

The retail zones use entries such as:

```
fx,test/lighting_fraction
```

| | |
| --- | --- |
| Zone definition type | `fx` |
| Extension | `.efx` |
| Retail occurrence | 1 of the 116 English zones |

See [the project layout](../../README.md) for how this directory fits into the
tree as a whole.
