# `video/`

The `video/` directory holds the tables describing video playback entries.

The asset name is the path itself. A zone definition entry therefore repeats
this directory and includes the file extension.

For example, the zone definition entry:

```
rawfile,video/example.txt
```

is built from `video/example.txt`.

The retail zones use entries such as:

```
rawfile,video/cin_levels.txt
```

| | |
| --- | --- |
| Zone definition type | `rawfile` |
| Extension | `.txt`, `.csv` |
| Retail occurrence | 1 of the 116 English zones |

See [the project layout](../README.md) for how this directory fits into the
tree as a whole.
