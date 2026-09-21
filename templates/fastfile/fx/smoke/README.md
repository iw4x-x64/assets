# `fx/smoke/`

The `fx/smoke/` directory holds smoke effects. The category forms part of the
asset name while `fx/` does not.

The leading `fx/` component is supplied by the tooling and does not appear in
the zone definition. The remainder of the path, `smoke/`, forms part of the
asset name.

For example, the zone definition entry:

```
fx,smoke/example
```

is built from `fx/smoke/example.efx`.

The retail zones use entries such as:

```
fx,smoke/airplane_crash_smoke
fx,smoke/airplane_crash_smoke_sun_blocker
fx,smoke/airplane_damage_blacksmoke_fire
```

| | |
| --- | --- |
| Zone definition type | `fx` |
| Extension | `.efx` |
| Retail occurrence | 61 of the 116 English zones |

See [the project layout](../../README.md) for how this directory fits into the
tree as a whole.
