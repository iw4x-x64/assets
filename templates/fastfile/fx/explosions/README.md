# `fx/explosions/`

The `fx/explosions/` directory holds explosion effects. The category forms
part of the asset name while `fx/` does not.

The leading `fx/` component is supplied by the tooling and does not appear in
the zone definition. The remainder of the path, `explosions/`, forms part of
the asset name.

For example, the zone definition entry:

```
fx,explosions/example
```

is built from `fx/explosions/example.efx`.

The retail zones use entries such as:

```
fx,explosions/100ton_bomb
fx,explosions/100ton_bomb_secondary
fx,explosions/100ton_bomb_shockwave
```

| | |
| --- | --- |
| Zone definition type | `fx` |
| Extension | `.efx` |
| Retail occurrence | 54 of the 116 English zones |

See [the project layout](../../README.md) for how this directory fits into the
tree as a whole.
