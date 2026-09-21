# `radiant/`

The `radiant/` directory holds data used by the Radiant level editor, carried
in the fastfile as rawfiles.

The asset name is the path itself. A zone definition entry therefore repeats
this directory and includes the file extension.

For example, the zone definition entry:

```
rawfile,radiant/example.txt
```

is built from `radiant/example.txt`.

The retail zones use entries such as:

```
rawfile,radiant/keys.txt
```

| | |
| --- | --- |
| Zone definition type | `rawfile` |
| Extension | `.txt` |
| Retail occurrence | 2 of the 116 English zones |

See [the project layout](../README.md) for how this directory fits into the
tree as a whole.
