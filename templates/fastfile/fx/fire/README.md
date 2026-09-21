# `fx/fire/`

The `fx/fire/` directory holds fire and flame effects. The category forms part
of the asset name while `fx/` does not.

The leading `fx/` component is supplied by the tooling and does not appear in
the zone definition. The remainder of the path, `fire/`, forms part of the
asset name.

For example, the zone definition entry:

```
fx,fire/example
```

is built from `fx/fire/example.efx`.

The retail zones use entries such as:

```
fx,fire/airplane_crash_embers
fx,fire/burninng_soldier_torso
fx,fire/cigar_glow
```

| | |
| --- | --- |
| Zone definition type | `fx` |
| Extension | `.efx` |
| Retail occurrence | 47 of the 116 English zones |

See [the project layout](../../README.md) for how this directory fits into the
tree as a whole.
