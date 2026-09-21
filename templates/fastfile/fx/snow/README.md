# `fx/snow/`

The `fx/snow/` directory holds snow effects. The category forms part of the
asset name while `fx/` does not.

The leading `fx/` component is supplied by the tooling and does not appear in
the zone definition. The remainder of the path, `snow/`, forms part of the
asset name.

For example, the zone definition entry:

```
fx,snow/example
```

is built from `fx/snow/example.efx`.

The retail zones use entries such as:

```
fx,snow/avalanche_finger_large_child
fx,snow/avalanche_loop_large
fx,snow/avalanche_start
```

| | |
| --- | --- |
| Zone definition type | `fx` |
| Extension | `.efx` |
| Retail occurrence | 30 of the 116 English zones |

See [the project layout](../../README.md) for how this directory fits into the
tree as a whole.
