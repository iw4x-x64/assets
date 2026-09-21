# `fx/impacts/`

The `fx/impacts/` directory holds effects played where a projectile meets a
surface. The category forms part of the asset name while `fx/` does not.

The leading `fx/` component is supplied by the tooling and does not appear in
the zone definition. The remainder of the path, `impacts/`, forms part of the
asset name.

For example, the zone definition entry:

```
fx,impacts/example
```

is built from `fx/impacts/example.efx`.

The retail zones use entries such as:

```
fx,impacts/20mm_brick_impact
fx,impacts/20mm_brick_impact_exit
fx,impacts/20mm_ceramic_impact
```

| | |
| --- | --- |
| Zone definition type | `fx` |
| Extension | `.efx` |
| Retail occurrence | 34 of the 116 English zones |

See [the project layout](../../README.md) for how this directory fits into the
tree as a whole.
