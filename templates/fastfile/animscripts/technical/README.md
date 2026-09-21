# `animscripts/technical/`

The `animscripts/technical/` directory holds the animation scripts for gunners
manning an armed pickup.

The asset name is the path itself. A zone definition entry therefore repeats
this directory and includes the file extension.

For example, the zone definition entry:

```
rawfile,animscripts/technical/example.gsc
```

is built from `animscripts/technical/example.gsc`.

The retail zones use entries such as:

```
rawfile,animscripts/technical/common.gsc
rawfile,animscripts/technical/stand.gsc
```

| | |
| --- | --- |
| Zone definition type | `rawfile` |
| Extension | `.gsc` |
| Retail occurrence | 3 of the 116 English zones |

See [the project layout](../../README.md) for how this directory fits into the
tree as a whole.
