# `maps/mp/killstreaks/`

The `maps/mp/killstreaks/` directory holds the scripts implementing killstreak
rewards.

The asset name is the path itself. A zone definition entry therefore repeats
this directory and includes the file extension.

For example, the zone definition entry:

```
rawfile,maps/mp/killstreaks/example.gsc
```

is built from `maps/mp/killstreaks/example.gsc`.

The retail zones use entries such as:

```
rawfile,maps/mp/killstreaks/_ac130.gsc
rawfile,maps/mp/killstreaks/_airdrop.gsc
rawfile,maps/mp/killstreaks/_airstrike.gsc
```

| | |
| --- | --- |
| Zone definition type | `rawfile` |
| Extension | `.gsc` |
| Retail occurrence | 2 of the 116 English zones |

See [the project layout](../../../README.md) for how this directory fits into
the tree as a whole.
