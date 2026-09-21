# `sound/level/`

The `sound/level/` directory holds audio belonging to a particular level. The
category and the `.wav` extension both form part of the asset name, while
`sound/` does not.

The leading `sound/` component is supplied by the tooling and does not appear
in the zone definition. The remainder of the path, `level/`, forms part of the
asset name.

For example, the zone definition entry:

```
loadedsound,level/example.wav
```

is built from `sound/level/example.wav`.

The retail zones use entries such as:

```
loadedsound,level/af_chase_collapse_dx_01.wav
loadedsound,level/af_chase_fightb_dx2.wav
loadedsound,level/af_chase_fightb_long_pri_dx.wav
```

| | |
| --- | --- |
| Zone definition type | `loadedsound` |
| Extension | `.wav` |
| Retail occurrence | 33 of the 116 English zones |

See [the project layout](../../README.md) for how this directory fits into the
tree as a whole.
