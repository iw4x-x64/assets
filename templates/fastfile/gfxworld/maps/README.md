# `gfxworld/maps/`

The `gfxworld/maps/` directory holds compiled render geometry for a map,
comprising its surfaces, lightmaps, portals and the placement of static
models, for singleplayer maps. The `maps/` component forms part of the asset
name.

The leading `gfxworld/` component is supplied by the tooling and does not
appear in the zone definition. The remainder of the path, `maps/`, forms part
of the asset name.

For example, the zone definition entry:

```
gfxworld,maps/af_caves.d3dbsp
```

is built from `gfxworld/maps/af_caves.d3dbsp.json`.

The retail zones use entries such as:

```
gfxworld,maps/af_caves.d3dbsp
gfxworld,maps/af_chase.d3dbsp
gfxworld,maps/airport.d3dbsp
```

| | |
| --- | --- |
| Zone definition type | `gfxworld` |
| Extension | `.json` |
| Retail occurrence | 49 of the 116 English zones |

See [the project layout](../../README.md) for how this directory fits into the
tree as a whole.
