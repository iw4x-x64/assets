# `xmodelalias/`

The `xmodelalias/` directory holds model alias lists, which let script choose
a model from a named group.

The asset name is the path itself. A zone definition entry therefore repeats
this directory and includes the file extension.

For example, the zone definition entry:

```
rawfile,xmodelalias/example.gsc
```

is built from `xmodelalias/example.gsc`.

The retail zones use entries such as:

```
rawfile,xmodelalias/alias_airborne_heads.gsc
rawfile,xmodelalias/alias_city_civ_male_heads.gsc
rawfile,xmodelalias/alias_civilian_slum_heads.gsc
```

| | |
| --- | --- |
| Zone definition type | `rawfile` |
| Extension | `.gsc` |
| Retail occurrence | 23 of the 116 English zones |

See [the project layout](../README.md) for how this directory fits into the
tree as a whole.
