# `gfxworld/maps/mp/`

The `gfxworld/maps/mp/` directory holds compiled render geometry for a map,
comprising its surfaces, lightmaps, portals and the placement of static
models, for multiplayer maps. Both the `maps/` and `mp/` components form part
of the asset name.

The leading `gfxworld/` component is supplied by the tooling and does not
appear in the zone definition. The remainder of the path, `maps/mp/`, forms
part of the asset name.

For example, the zone definition entry:

```
gfxworld,maps/mp/mp_afghan.d3dbsp
```

is built from `gfxworld/maps/mp/mp_afghan.d3dbsp.json`.

The retail zones use entries such as:

```
gfxworld,maps/mp/mp_abandon.d3dbsp
gfxworld,maps/mp/mp_afghan.d3dbsp
gfxworld,maps/mp/mp_boneyard.d3dbsp
```

| | |
| --- | --- |
| Zone definition type | `gfxworld` |
| Extension | `.json` |
| Retail occurrence | 26 of the 116 English zones |

See [the project layout](../../../README.md) for how this directory fits into
the tree as a whole.
