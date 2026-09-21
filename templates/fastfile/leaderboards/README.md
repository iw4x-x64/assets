# `leaderboards/`

The `leaderboards/` directory holds leaderboard definitions in JSON form,
giving the columns a leaderboard tracks and how each is aggregated.

The directory name is supplied by the tooling and does not appear in the zone
definition, which names the asset on its own.

For example, the zone definition entry:

```
leaderboard,example
```

is built from `leaderboards/example.json`.

| | |
| --- | --- |
| Zone definition type | `leaderboard` |
| Extension | `.json` |
| Retail occurrence | 1 of the 116 English zones |

See [the project layout](../README.md) for how this directory fits into the
tree as a whole.
