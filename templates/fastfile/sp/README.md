# `sp/`

The `sp/` directory holds the singleplayer data tables in CSV form, referred
to as `stringtable` assets.

The asset name is the path itself. A zone definition entry therefore repeats
this directory and includes the file extension.

For example, the zone definition entry:

```
stringtable,sp/example.csv
```

is built from `sp/example.csv`.

The retail zones use entries such as:

```
stringtable,sp/contracttable.csv
stringtable,sp/deathquotetable.csv
stringtable,sp/rankicontable.csv
```

| | |
| --- | --- |
| Zone definition type | `stringtable` |
| Extension | `.csv` |
| Retail occurrence | 1 of the 116 English zones |

See [the project layout](../README.md) for how this directory fits into the
tree as a whole.
