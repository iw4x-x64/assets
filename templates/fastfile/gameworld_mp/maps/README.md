# `gameworld_mp/maps/`

The `gameworld_mp/maps/` directory holds multiplayer gameplay world data for a
map, such as path node data, for singleplayer maps. The `maps/` component
forms part of the asset name.

The leading `gameworld_mp/` component is supplied by the tooling and does not
appear in the zone definition. The remainder of the path, `maps/`, forms part
of the asset name.

For example, the zone definition entry:

```
gameworldmp,maps/af_caves.d3dbsp
```

is built from `gameworld_mp/maps/af_caves.d3dbsp.json`.

The retail zones use entries such as:

```
gameworldmp,maps/mp/mp_abandon.d3dbsp
gameworldmp,maps/mp/mp_afghan.d3dbsp
gameworldmp,maps/mp/mp_boneyard.d3dbsp
```

| | |
| --- | --- |
| Zone definition type | `gameworldmp` |
| Retail occurrence | 26 of the 116 English zones |

See [the project layout](../../README.md) for how this directory fits into the
tree as a whole.
