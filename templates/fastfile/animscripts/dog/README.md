# `animscripts/dog/`

The `animscripts/dog/` directory holds the animation scripts for dogs.

The asset name is the path itself. A zone definition entry therefore repeats
this directory and includes the file extension.

For example, the zone definition entry:

```
rawfile,animscripts/dog/example.gsc
```

is built from `animscripts/dog/example.gsc`.

The retail zones use entries such as:

```
rawfile,animscripts/dog/dog_combat.gsc
rawfile,animscripts/dog/dog_death.gsc
rawfile,animscripts/dog/dog_flashed.gsc
```

| | |
| --- | --- |
| Zone definition type | `rawfile` |
| Extension | `.gsc` |
| Retail occurrence | 5 of the 116 English zones |

See [the project layout](../../README.md) for how this directory fits into the
tree as a whole.
