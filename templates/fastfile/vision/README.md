# `vision/`

The `vision/` directory holds vision files, which describe colour grading,
exposure and tone mapping for a level or for a scripted moment.

The asset name is the path itself. A zone definition entry therefore repeats
this directory and includes the file extension.

For example, the zone definition entry:

```
rawfile,vision/example.vision
```

is built from `vision/example.vision`.

The retail zones use entries such as:

```
rawfile,vision/ac130.vision
rawfile,vision/ac130_inverted.vision
rawfile,vision/af_caves_indoors.vision
```

| | |
| --- | --- |
| Zone definition type | `rawfile` |
| Extension | `.vision` |
| Retail occurrence | 30 of the 116 English zones |

See [the project layout](../README.md) for how this directory fits into the
tree as a whole.
