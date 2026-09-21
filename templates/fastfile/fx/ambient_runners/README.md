# `fx/ambient_runners/`

The `fx/ambient_runners/` directory holds ambient looping effects placed
throughout a level. The category forms part of the asset name while `fx/` does
not.

The leading `fx/` component is supplied by the tooling and does not appear in
the zone definition. The remainder of the path, `ambient_runners/`, forms part
of the asset name.

For example, the zone definition entry:

```
fx,ambient_runners/example
```

is built from `fx/ambient_runners/example.efx`.

The retail zones use entries such as:

```
fx,ambient_runners/mp_overgrown_fog_daytime01
fx,ambient_runners/mp_overgrown_insects01
fx,ambient_runners/mp_overgrown_insects02
```

| | |
| --- | --- |
| Zone definition type | `fx` |
| Extension | `.efx` |
| Retail occurrence | 1 of the 116 English zones |

See [the project layout](../../README.md) for how this directory fits into the
tree as a whole.
