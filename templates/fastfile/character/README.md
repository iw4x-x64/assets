# `character/`

The `character/` directory holds the per character scripts that bind a model
set, a voice and a loadout together.

The asset name is the path itself. A zone definition entry therefore repeats
this directory and includes the file extension.

For example, the zone definition entry:

```
rawfile,character/example.gsc
```

is built from `character/example.gsc`.

The retail zones use entries such as:

```
rawfile,character/character_airborne_assault_a.gsc
rawfile,character/character_airborne_assault_a_drone.gsc
rawfile,character/character_airborne_assault_b.gsc
```

| | |
| --- | --- |
| Zone definition type | `rawfile` |
| Extension | `.gsc` |
| Retail occurrence | 28 of the 116 English zones |

See [the project layout](../README.md) for how this directory fits into the
tree as a whole.
