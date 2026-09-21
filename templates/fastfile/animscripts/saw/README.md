# `animscripts/saw/`

The `animscripts/saw/` directory holds the animation scripts for gunners
manning a SAW.

The asset name is the path itself. A zone definition entry therefore repeats
this directory and includes the file extension.

For example, the zone definition entry:

```
rawfile,animscripts/saw/example.gsc
```

is built from `animscripts/saw/example.gsc`.

The retail zones use entries such as:

```
rawfile,animscripts/saw/common.gsc
rawfile,animscripts/saw/crouch.gsc
rawfile,animscripts/saw/prone.gsc
```

| | |
| --- | --- |
| Zone definition type | `rawfile` |
| Extension | `.gsc` |
| Retail occurrence | 1 of the 116 English zones |

See [the project layout](../../README.md) for how this directory fits into the
tree as a whole.
