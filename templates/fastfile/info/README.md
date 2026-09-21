# `info/`

The `info/` directory holds assorted engine information files that belong to
no other category.

The asset name is the path itself. A zone definition entry therefore repeats
this directory and includes the file extension.

For example, the zone definition entry:

```
rawfile,info/example
```

is built from `info/example`.

The retail zones use entries such as:

```
rawfile,info/ai_lochit_dmgtable
rawfile,info/bullet_penetration_mp
rawfile,info/bullet_penetration_sp
```

| | |
| --- | --- |
| Zone definition type | `rawfile` |
| Extension | none |
| Retail occurrence | 2 of the 116 English zones |

See [the project layout](../README.md) for how this directory fits into the
tree as a whole.
