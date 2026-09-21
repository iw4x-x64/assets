# `maps/`

The `maps/` directory is the most mixed in a zone. It holds the per level
scripts as rawfiles, the entity lists that place everything in a map, and a
number of string tables.

Note that the compiled world data for the same maps does not live here. It is
found under `gfxworld/`, `comworld/`, `fxworld/`, `clipmap_mp/` and
`gameworld_mp/` or `gameworld_sp/`, each keyed by the same
`maps/<name>.d3dbsp` asset name.

The asset name is the path itself. A zone definition entry therefore repeats
this directory and includes the file extension.

For example, the zone definition entry:

```
mapents,maps/af_caves.d3dbsp
```

is built from `maps/af_caves.d3dbsp.ents`.

As with the world assets, the extension is appended to the full asset name
rather than replacing it, giving `<name>.d3dbsp.ents`.

The `addonmapents` type is the downloadable content variant. OAT writes its
string form but not its binary data and cannot read it back, so a zone using
it will not round trip.

The retail zones use entries such as:

```
addonmapents,maps/so_ac130_co_hunted.mapents
addonmapents,maps/so_assault_oilrig.mapents
addonmapents,maps/so_chopper_invasion.mapents
```

| | |
| --- | --- |
| Zone definition type | `rawfile`, `mapents`, `addonmapents`, `stringtable` |
| Extension | `.gsc`, `.json`, `.mapents` |
| Retail occurrence | 76 of the 116 English zones |

See [the project layout](../README.md) for how this directory fits into the
tree as a whole.
