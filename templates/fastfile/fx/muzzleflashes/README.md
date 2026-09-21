# `fx/muzzleflashes/`

The `fx/muzzleflashes/` directory holds weapon muzzle flash effects. The
category forms part of the asset name while `fx/` does not.

The leading `fx/` component is supplied by the tooling and does not appear in
the zone definition. The remainder of the path, `muzzleflashes/`, forms part
of the asset name.

For example, the zone definition entry:

```
fx,muzzleflashes/example
```

is built from `fx/muzzleflashes/example.efx`.

The retail zones use entries such as:

```
fx,muzzleflashes/aa12_flash_view
fx,muzzleflashes/aa12_flash_wv
fx,muzzleflashes/abrams_flash_wv
```

| | |
| --- | --- |
| Zone definition type | `fx` |
| Extension | `.efx` |
| Retail occurrence | 39 of the 116 English zones |

See [the project layout](../../README.md) for how this directory fits into the
tree as a whole.
