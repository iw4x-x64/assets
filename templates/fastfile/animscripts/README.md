# `animscripts/`

The `animscripts/` directory holds the scripts that drive character animation
state, governing how a character moves, reacts, takes cover and dies.

The asset name is the path itself. A zone definition entry therefore repeats
this directory and includes the file extension.

For example, the zone definition entry:

```
rawfile,animscripts/example.gsc
```

is built from `animscripts/example.gsc`.

The retail zones use entries such as:

```
rawfile,animscripts/animmode.gsc
rawfile,animscripts/animset.gsc
rawfile,animscripts/battlechatter.gsc
```

| | |
| --- | --- |
| Zone definition type | `rawfile` |
| Extension | `.gsc` |
| Retail occurrence | 15 of the 116 English zones |

See [the project layout](../README.md) for how this directory fits into the
tree as a whole.
