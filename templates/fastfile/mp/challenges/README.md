# `mp/challenges/`

The `mp/challenges/` directory holds the challenge tables in CSV form.

The asset name is the path itself. A zone definition entry therefore repeats
this directory and includes the file extension.

For example, the zone definition entry:

```
stringtable,mp/challenges/example.csv
```

is built from `mp/challenges/example.csv`.

The retail zones use entries such as:

```
stringtable,mp/challenges/aa12_challenges.csv
stringtable,mp/challenges/ak47_challenges.csv
stringtable,mp/challenges/at4_challenges.csv
```

| | |
| --- | --- |
| Zone definition type | `stringtable` |
| Extension | `.csv` |
| Retail occurrence | 1 of the 116 English zones |

See [the project layout](../../README.md) for how this directory fits into the
tree as a whole.
