# `clipmap_mp/maps/`

The `clipmap_mp/maps/` directory holds compiled collision geometry for a map,
being the brushes and models the engine traces against, for singleplayer maps.
The `maps/` component forms part of the asset name.

The leading `clipmap_mp/` component is supplied by the tooling and does not
appear in the zone definition. The remainder of the path, `maps/`, forms part
of the asset name.

For example, the zone definition entry:

```
clipmap,maps/af_caves.d3dbsp
```

is built from `clipmap_mp/maps/af_caves.d3dbsp.json`.

The retail zones use entries such as:

```
clipmap,maps/af_caves.d3dbsp
clipmap,maps/af_chase.d3dbsp
clipmap,maps/airport.d3dbsp
```

| | |
| --- | --- |
| Zone definition type | `clipmap` |
| Extension | `.json` |
| Retail occurrence | 49 of the 116 English zones |

See [the project layout](../../README.md) for how this directory fits into the
tree as a whole.
