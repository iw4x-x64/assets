# `comworld/maps/mp/`

The `comworld/maps/mp/` directory holds compiled lighting data for a map,
principally the light set used for static lighting, for multiplayer maps. Both
the `maps/` and `mp/` components form part of the asset name.

The leading `comworld/` component is supplied by the tooling and does not
appear in the zone definition. The remainder of the path, `maps/mp/`, forms
part of the asset name.

For example, the zone definition entry:

```
comworld,maps/mp/mp_afghan.d3dbsp
```

is built from `comworld/maps/mp/mp_afghan.d3dbsp.json`.

The retail zones use entries such as:

```
comworld,maps/mp/mp_abandon.d3dbsp
comworld,maps/mp/mp_afghan.d3dbsp
comworld,maps/mp/mp_boneyard.d3dbsp
```

| | |
| --- | --- |
| Zone definition type | `comworld` |
| Extension | `.json` |
| Retail occurrence | 26 of the 116 English zones |

See [the project layout](../../../README.md) for how this directory fits into
the tree as a whole.
