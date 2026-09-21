# `mp/`

The `mp/` directory holds the multiplayer data tables. Most entries here are
string tables in CSV form rather than rawfiles. The directory also holds the
structured data definitions that describe the player data layout used for
statistics and loadouts.

The asset name is the path itself. A zone definition entry therefore repeats
this directory and includes the file extension.

For example, the zone definition entry:

```
stringtable,mp/example.csv
```

is built from `mp/example.csv`.

Note that OAT represents `structureddatadef` in a format of its own devising,
because the original is not documented. Changing a definition alters the
player data layout and breaks compatibility with existing saved data.

The retail zones use entries such as:

```
rawfile,mp/basemaps.arena
rawfile,mp/mappack.info
rawfile,mp/playeranim.script
```

| | |
| --- | --- |
| Zone definition type | `rawfile`, `stringtable`, `structureddatadef` |
| Extension | `.csv`, `.def`, `.txt` |
| Retail occurrence | 32 of the 116 English zones |

See [the project layout](../README.md) for how this directory fits into the
tree as a whole.
