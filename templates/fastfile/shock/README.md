# `shock/`

The `shock/` directory holds shellshock definitions, which describe the
visual, audio and control effects applied when a player is concussed.

The asset name is the path itself. A zone definition entry therefore repeats
this directory and includes the file extension.

For example, the zone definition entry:

```
rawfile,shock/example.shock
```

is built from `shock/example.shock`.

The retail zones use entries such as:

```
rawfile,shock/ac130.shock
rawfile,shock/af_cave_collapse.shock
rawfile,shock/af_chase_boatdrive_end.shock
```

| | |
| --- | --- |
| Zone definition type | `rawfile` |
| Extension | `.shock` |
| Retail occurrence | 40 of the 116 English zones |

See [the project layout](../README.md) for how this directory fits into the
tree as a whole.
