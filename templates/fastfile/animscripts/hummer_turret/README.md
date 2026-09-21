# `animscripts/hummer_turret/`

The `animscripts/hummer_turret/` directory holds the animation scripts for
gunners manning a Humvee turret.

The asset name is the path itself. A zone definition entry therefore repeats
this directory and includes the file extension.

For example, the zone definition entry:

```
rawfile,animscripts/hummer_turret/example.gsc
```

is built from `animscripts/hummer_turret/example.gsc`.

The retail zones use entries such as:

```
rawfile,animscripts/hummer_turret/common.gsc
rawfile,animscripts/hummer_turret/minigun_code.gsc
rawfile,animscripts/hummer_turret/minigun_stand.gsc
```

| | |
| --- | --- |
| Zone definition type | `rawfile` |
| Extension | `.gsc` |
| Retail occurrence | 4 of the 116 English zones |

See [the project layout](../../README.md) for how this directory fits into the
tree as a whole.
