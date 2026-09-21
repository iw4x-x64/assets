# `soundaliases/`

The `soundaliases/` directory holds alias tables in CSV form. An alias maps a
named handle to one or more files in `sound/` and carries the volume, falloff,
pitch and channel settings used when it is played. Scripts, weapons and
effects refer to aliases rather than to sound files directly, so most audio
work happens at this level.

The directory name is supplied by the tooling and does not appear in the zone
definition, which names the asset on its own.

For example, the zone definition entry:

```
sound,aagun_fire_dist_long
```

is built from `soundaliases/<table>.csv`.

Note that one CSV file holds many aliases and the zone definition names the
alias rather than the file, so there is no one to one relationship between
entries and files here.

A `.vfcurve` file in this directory is a volume falloff curve referred to by
an alias. The separate `soundcurve` asset type also resolves here.

The retail zones use entries such as:

```
sound,aagun_fire_dist_long
sound,aagun_fire_dist_short
```

| | |
| --- | --- |
| Zone definition type | `sound` |
| Extension | `.csv`, `.vfcurve` |
| Retail occurrence | 78 of the 116 English zones |

See [the project layout](../README.md) for how this directory fits into the
tree as a whole.
