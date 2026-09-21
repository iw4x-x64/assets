# `fx/weather/`

The `fx/weather/` directory holds weather effects. The category forms part of
the asset name while `fx/` does not.

The leading `fx/` component is supplied by the tooling and does not appear in
the zone definition. The remainder of the path, `weather/`, forms part of the
asset name.

For example, the zone definition entry:

```
fx,weather/example
```

is built from `fx/weather/example.efx`.

The retail zones use entries such as:

```
fx,weather/cloud_bank_cloud_filler_gulag
fx,weather/cloud_bank_cloud_filler_light_gulag
fx,weather/cloud_bank_cloud_filler_tight_gulag
```

| | |
| --- | --- |
| Zone definition type | `fx` |
| Extension | `.efx` |
| Retail occurrence | 12 of the 116 English zones |

See [the project layout](../../README.md) for how this directory fits into the
tree as a whole.
