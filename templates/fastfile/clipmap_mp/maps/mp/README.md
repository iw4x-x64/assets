# `clipmap_mp/maps/mp/`

The `clipmap_mp/maps/mp/` directory holds compiled collision geometry for a
map, being the brushes and models the engine traces against, for multiplayer
maps. Both the `maps/` and `mp/` components form part of the asset name.

The leading `clipmap_mp/` component is supplied by the tooling and does not
appear in the zone definition. The remainder of the path, `maps/mp/`, forms
part of the asset name.

For example, the zone definition entry:

```
clipmap,maps/mp/mp_afghan.d3dbsp
```

is built from `clipmap_mp/maps/mp/mp_afghan.d3dbsp.json`.

The retail zones use entries such as:

```
clipmap,maps/mp/mp_abandon.d3dbsp
clipmap,maps/mp/mp_afghan.d3dbsp
clipmap,maps/mp/mp_boneyard.d3dbsp
```

| | |
| --- | --- |
| Zone definition type | `clipmap` |
| Extension | `.json` |
| Retail occurrence | 26 of the 116 English zones |

See [the project layout](../../../README.md) for how this directory fits into
the tree as a whole.
