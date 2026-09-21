# `common_scripts/`

The `common_scripts/` directory holds the shared script library that levels
call into, comprising utility routines, common triggers and helpers.

The asset name is the path itself. A zone definition entry therefore repeats
this directory and includes the file extension.

For example, the zone definition entry:

```
rawfile,common_scripts/example.gsc
```

is built from `common_scripts/example.gsc`.

The retail zones use entries such as:

```
rawfile,common_scripts/_artcommon.gsc
rawfile,common_scripts/_createfx.gsc
rawfile,common_scripts/_createfxmenu.gsc
```

| | |
| --- | --- |
| Zone definition type | `rawfile` |
| Extension | `.gsc` |
| Retail occurrence | 48 of the 116 English zones |

See [the project layout](../README.md) for how this directory fits into the
tree as a whole.
