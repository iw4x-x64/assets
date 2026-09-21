# `fx/water/`

The `fx/water/` directory holds water effects. The category forms part of the
asset name while `fx/` does not.

The leading `fx/` component is supplied by the tooling and does not appear in
the zone definition. The remainder of the path, `water/`, forms part of the
asset name.

For example, the zone definition entry:

```
fx,water/example
```

is built from `fx/water/example.efx`.

The retail zones use entries such as:

```
fx,water/blood_spurt_underwater
fx,water/drips_player_hand
fx,water/drips_small_splash
```

| | |
| --- | --- |
| Zone definition type | `fx` |
| Extension | `.efx` |
| Retail occurrence | 20 of the 116 English zones |

See [the project layout](../../README.md) for how this directory fits into the
tree as a whole.
