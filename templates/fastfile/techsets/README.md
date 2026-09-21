# `techsets/`

The `techsets/` directory holds technique sets. A technique set names the
group of rendering techniques a material may be drawn with, one per pass or
lighting variant. A material refers to a technique set by name, and the set in
turn refers to the techniques in `techniques/`.

The directory name is supplied by the tooling and does not appear in the zone
definition, which names the asset on its own.

For example, the zone definition entry:

```
techniqueset,2d
```

is built from `techsets/2d.techset`.

The retail zones use entries such as:

```
techniqueset,,2d
techniqueset,2d
```

| | |
| --- | --- |
| Zone definition type | `techniqueset` |
| Extension | `.techset` |
| Retail occurrence | 103 of the 116 English zones |

See [the project layout](../README.md) for how this directory fits into the
tree as a whole.
