# `comworld/maps/`

The `comworld/maps/` directory holds compiled lighting data for a map,
principally the light set used for static lighting, for singleplayer maps. The
`maps/` component forms part of the asset name.

The leading `comworld/` component is supplied by the tooling and does not
appear in the zone definition. The remainder of the path, `maps/`, forms part
of the asset name.

For example, the zone definition entry:

```
comworld,maps/af_caves.d3dbsp
```

is built from `comworld/maps/af_caves.d3dbsp.json`.

The retail zones use entries such as:

```
comworld,maps/af_caves.d3dbsp
comworld,maps/af_chase.d3dbsp
comworld,maps/airport.d3dbsp
```

| | |
| --- | --- |
| Zone definition type | `comworld` |
| Extension | `.json` |
| Retail occurrence | 49 of the 116 English zones |

See [the project layout](../../README.md) for how this directory fits into the
tree as a whole.
