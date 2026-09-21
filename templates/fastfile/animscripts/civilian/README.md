# `animscripts/civilian/`

The `animscripts/civilian/` directory holds the animation scripts for civilian
characters.

The asset name is the path itself. A zone definition entry therefore repeats
this directory and includes the file extension.

For example, the zone definition entry:

```
rawfile,animscripts/civilian/example.gsc
```

is built from `animscripts/civilian/example.gsc`.

The retail zones use entries such as:

```
rawfile,animscripts/civilian/civilian_combat.gsc
rawfile,animscripts/civilian/civilian_cover_arrival.gsc
rawfile,animscripts/civilian/civilian_cover_crouch.gsc
```

| | |
| --- | --- |
| Zone definition type | `rawfile` |
| Extension | `.gsc` |
| Retail occurrence | 8 of the 116 English zones |

See [the project layout](../../README.md) for how this directory fits into the
tree as a whole.
