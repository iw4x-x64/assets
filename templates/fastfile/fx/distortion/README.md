# `fx/distortion/`

The `fx/distortion/` directory holds heat haze and other distortion effects.
The category forms part of the asset name while `fx/` does not.

The leading `fx/` component is supplied by the tooling and does not appear in
the zone definition. The remainder of the path, `distortion/`, forms part of
the asset name.

For example, the zone definition entry:

```
fx,distortion/example
```

is built from `fx/distortion/example.efx`.

The retail zones use entries such as:

```
fx,distortion/abrams_exhaust
fx,distortion/armored_car_overheat
fx,distortion/cgo_ship_puddle_large
```

| | |
| --- | --- |
| Zone definition type | `fx` |
| Extension | `.efx` |
| Retail occurrence | 30 of the 116 English zones |

See [the project layout](../../README.md) for how this directory fits into the
tree as a whole.
