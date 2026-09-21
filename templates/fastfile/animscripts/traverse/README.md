# `animscripts/traverse/`

The `animscripts/traverse/` directory holds the animation scripts for
traversal moves such as climbing and vaulting.

The asset name is the path itself. A zone definition entry therefore repeats
this directory and includes the file extension.

For example, the zone definition entry:

```
rawfile,animscripts/traverse/example.gsc
```

is built from `animscripts/traverse/example.gsc`.

The retail zones use entries such as:

```
rawfile,animscripts/traverse/crouch_jump_down_40.gsc
rawfile,animscripts/traverse/duck_under_56.gsc
rawfile,animscripts/traverse/fence_climb.gsc
```

| | |
| --- | --- |
| Zone definition type | `rawfile` |
| Extension | `.gsc` |
| Retail occurrence | 2 of the 116 English zones |

See [the project layout](../../README.md) for how this directory fits into the
tree as a whole.
