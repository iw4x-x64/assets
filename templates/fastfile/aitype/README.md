# `aitype/`

The `aitype/` directory holds the scripts defining each AI archetype, covering
its weapon, accuracy, health and behaviour hooks.

The asset name is the path itself. A zone definition entry therefore repeats
this directory and includes the file extension.

For example, the zone definition entry:

```
rawfile,aitype/example.gsc
```

is built from `aitype/example.gsc`.

The retail zones use entries such as:

```
rawfile,aitype/ally_airport_comrad_m4.gsc
rawfile,aitype/ally_airport_comrad_saw.gsc
rawfile,aitype/ally_airport_comrad_shotgun.gsc
```

| | |
| --- | --- |
| Zone definition type | `rawfile` |
| Extension | `.gsc` |
| Retail occurrence | 27 of the 116 English zones |

See [the project layout](../README.md) for how this directory fits into the
tree as a whole.
