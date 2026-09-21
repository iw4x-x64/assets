# `vehicle/`

The `vehicle/` directory holds vehicle curve definitions, such as those
governing steering and speed response.

The asset name is the path itself. A zone definition entry therefore repeats
this directory and includes the file extension.

For example, the zone definition entry:

```
rawfile,vehicle/example.graph
```

is built from `vehicle/example.graph`.

Note that this directory is singular. The plural `vehicles/` directory is
unrelated and holds `vehicle` assets rather than rawfiles. Both occur in
retail zones.

The retail zones use entries such as:

```
rawfile,vehicle/default_accel.graph
rawfile,vehicle/snowmobile_accel.graph
rawfile,vehicle/snowmobile_race_accel.graph
```

| | |
| --- | --- |
| Zone definition type | `rawfile` |
| Extension | `.graph` |
| Retail occurrence | 15 of the 116 English zones |

See [the project layout](../README.md) for how this directory fits into the
tree as a whole.
