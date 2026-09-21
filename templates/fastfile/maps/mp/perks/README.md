# `maps/mp/perks/`

The `maps/mp/perks/` directory holds the scripts implementing perks.

The asset name is the path itself. A zone definition entry therefore repeats
this directory and includes the file extension.

For example, the zone definition entry:

```
rawfile,maps/mp/perks/example.gsc
```

is built from `maps/mp/perks/example.gsc`.

The retail zones use entries such as:

```
rawfile,maps/mp/perks/_perkfunctions.gsc
rawfile,maps/mp/perks/_perks.gsc
```

| | |
| --- | --- |
| Zone definition type | `rawfile` |
| Extension | `.gsc` |
| Retail occurrence | 2 of the 116 English zones |

See [the project layout](../../../README.md) for how this directory fits into
the tree as a whole.
