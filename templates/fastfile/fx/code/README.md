# `fx/code/`

The `fx/code/` directory holds effects spawned directly by engine code rather
than by script. The category forms part of the asset name while `fx/` does
not.

The leading `fx/` component is supplied by the tooling and does not appear in
the zone definition. The remainder of the path, `code/`, forms part of the
asset name.

For example, the zone definition entry:

```
fx,code/example
```

is built from `fx/code/example.efx`.

The retail zones use entries such as:

```
fx,code/glass_shatter_32x32
fx,code/glass_shatter_64x64
fx,code/glass_shatter_piece
```

| | |
| --- | --- |
| Zone definition type | `fx` |
| Extension | `.efx` |
| Retail occurrence | 2 of the 116 English zones |

See [the project layout](../../README.md) for how this directory fits into the
tree as a whole.
