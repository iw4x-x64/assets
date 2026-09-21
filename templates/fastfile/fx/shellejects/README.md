# `fx/shellejects/`

The `fx/shellejects/` directory holds effects for ejected cartridge cases. The
category forms part of the asset name while `fx/` does not.

The leading `fx/` component is supplied by the tooling and does not appear in
the zone definition. The remainder of the path, `shellejects/`, forms part of
the asset name.

For example, the zone definition entry:

```
fx,shellejects/example
```

is built from `fx/shellejects/example.efx`.

The retail zones use entries such as:

```
fx,shellejects/20mm_cargoship
fx,shellejects/20mm_mp
fx,shellejects/20mm_resting
```

| | |
| --- | --- |
| Zone definition type | `fx` |
| Extension | `.efx` |
| Retail occurrence | 28 of the 116 English zones |

See [the project layout](../../README.md) for how this directory fits into the
tree as a whole.
