# `fx/treadfx/`

The `fx/treadfx/` directory holds effects raised by vehicle treads and tyres.
The category forms part of the asset name while `fx/` does not.

The leading `fx/` component is supplied by the tooling and does not appear in
the zone definition. The remainder of the path, `treadfx/`, forms part of the
asset name.

For example, the zone definition entry:

```
fx,treadfx/example
```

is built from `fx/treadfx/example.efx`.

The retail zones use entries such as:

```
fx,treadfx/bigair_snow_snowmobile_child
fx,treadfx/bigair_snow_snowmobile_emitter
fx,treadfx/bigjump_land_snow_snowmobile
```

| | |
| --- | --- |
| Zone definition type | `fx` |
| Extension | `.efx` |
| Retail occurrence | 15 of the 116 English zones |

See [the project layout](../../README.md) for how this directory fits into the
tree as a whole.
