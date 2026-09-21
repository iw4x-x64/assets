# `fx/dust/`

The `fx/dust/` directory holds dust and airborne particulate effects. The
category forms part of the asset name while `fx/` does not.

The leading `fx/` component is supplied by the tooling and does not appear in
the zone definition. The remainder of the path, `dust/`, forms part of the
asset name.

For example, the zone definition entry:

```
fx,dust/example
```

is built from `fx/dust/example.efx`.

The retail zones use entries such as:

```
fx,dust/abrams_desk_dust
fx,dust/abrams_muzzle_dust
fx,dust/ash_spiral01
```

| | |
| --- | --- |
| Zone definition type | `fx` |
| Extension | `.efx` |
| Retail occurrence | 34 of the 116 English zones |

See [the project layout](../../README.md) for how this directory fits into the
tree as a whole.
