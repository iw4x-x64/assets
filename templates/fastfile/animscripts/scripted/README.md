# `animscripts/scripted/`

The `animscripts/scripted/` directory holds the animation scripts for scripted
sequences.

The asset name is the path itself. A zone definition entry therefore repeats
this directory and includes the file extension.

For example, the zone definition entry:

```
rawfile,animscripts/scripted/example.gsc
```

is built from `animscripts/scripted/example.gsc`.

The retail zones use entries such as:

```
rawfile,animscripts/scripted/truckride_backoftruck.gsc
```

| | |
| --- | --- |
| Zone definition type | `rawfile` |
| Extension | `.gsc` |
| Retail occurrence | 1 of the 116 English zones |

See [the project layout](../../README.md) for how this directory fits into the
tree as a whole.
