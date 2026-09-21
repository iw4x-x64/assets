# `fxworld/maps/mp/`

The `fxworld/maps/mp/` directory holds compiled per map effects data,
including the state of the glass system, for multiplayer maps. Both the
`maps/` and `mp/` components form part of the asset name.

The leading `fxworld/` component is supplied by the tooling and does not
appear in the zone definition. The remainder of the path, `maps/mp/`, forms
part of the asset name.

For example, the zone definition entry:

```
fxworld,maps/mp/mp_afghan.d3dbsp
```

is built from `fxworld/maps/mp/mp_afghan.d3dbsp.json`.

The retail zones use entries such as:

```
fxworld,maps/mp/mp_abandon.d3dbsp
fxworld,maps/mp/mp_afghan.d3dbsp
fxworld,maps/mp/mp_boneyard.d3dbsp
```

| | |
| --- | --- |
| Zone definition type | `fxworld` |
| Extension | `.json` |
| Retail occurrence | 26 of the 116 English zones |

See [the project layout](../../../README.md) for how this directory fits into
the tree as a whole.
