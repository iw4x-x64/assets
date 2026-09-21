# `fx/animals/`

The `fx/animals/` directory holds effects associated with animals. The
category forms part of the asset name while `fx/` does not.

The leading `fx/` component is supplied by the tooling and does not appear in
the zone definition. The remainder of the path, `animals/`, forms part of the
asset name.

For example, the zone definition entry:

```
fx,animals/example
```

is built from `fx/animals/example.efx`.

The retail zones use entries such as:

```
fx,animals/fish_school01
fx,animals/fish_school_side_large
fx,animals/fish_school_side_med
```

| | |
| --- | --- |
| Zone definition type | `fx` |
| Extension | `.efx` |
| Retail occurrence | 1 of the 116 English zones |

See [the project layout](../../README.md) for how this directory fits into the
tree as a whole.
