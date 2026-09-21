# `gameworld_sp/maps/`

The `gameworld_sp/maps/` directory holds singleplayer gameplay world data for
a map, such as the path nodes used by AI, for singleplayer maps. The `maps/`
component forms part of the asset name.

The leading `gameworld_sp/` component is supplied by the tooling and does not
appear in the zone definition. The remainder of the path, `maps/`, forms part
of the asset name.

For example, the zone definition entry:

```
gameworldsp,maps/af_caves.d3dbsp
```

is built from `gameworld_sp/maps/af_caves.d3dbsp.json`.

The retail zones use entries such as:

```
gameworldsp,maps/af_caves.d3dbsp
gameworldsp,maps/af_chase.d3dbsp
gameworldsp,maps/airport.d3dbsp
```

| | |
| --- | --- |
| Zone definition type | `gameworldsp` |
| Extension | `.json` |
| Retail occurrence | 23 of the 116 English zones |

See [the project layout](../../README.md) for how this directory fits into the
tree as a whole.
