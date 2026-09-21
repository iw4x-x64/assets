# `mp/configstrings/`

The `mp/configstrings/` directory holds the config string tables, which are
keyed by map and gametype in CSV form.

The asset name is the path itself. A zone definition entry therefore repeats
this directory and includes the file extension.

For example, the zone definition entry:

```
stringtable,mp/configstrings/example.csv
```

is built from `mp/configstrings/example.csv`.

The retail zones use entries such as:

```
stringtable,mp/configstrings/configstrings_pc_mp_abandon_ctf.csv
stringtable,mp/configstrings/configstrings_pc_mp_abandon_dd.csv
stringtable,mp/configstrings/configstrings_pc_mp_abandon_dm.csv
```

| | |
| --- | --- |
| Zone definition type | `stringtable` |
| Extension | `.csv` |
| Retail occurrence | 26 of the 116 English zones |

See [the project layout](../../README.md) for how this directory fits into the
tree as a whole.
