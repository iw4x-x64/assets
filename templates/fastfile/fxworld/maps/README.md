# `fxworld/maps/`

The `fxworld/maps/` directory holds compiled per map effects data, including
the state of the glass system, for singleplayer maps. The `maps/` component
forms part of the asset name.

The leading `fxworld/` component is supplied by the tooling and does not
appear in the zone definition. The remainder of the path, `maps/`, forms part
of the asset name.

For example, the zone definition entry:

```
fxworld,maps/af_caves.d3dbsp
```

is built from `fxworld/maps/af_caves.d3dbsp.json`.

The retail zones use entries such as:

```
fxworld,maps/af_caves.d3dbsp
fxworld,maps/af_chase.d3dbsp
fxworld,maps/airport.d3dbsp
```

| | |
| --- | --- |
| Zone definition type | `fxworld` |
| Extension | `.json` |
| Retail occurrence | 49 of the 116 English zones |

See [the project layout](../../README.md) for how this directory fits into the
tree as a whole.
