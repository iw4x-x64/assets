# `sound/whizbys/`

The `sound/whizbys/` directory holds audio for rounds passing close by. The
category and the `.wav` extension both form part of the asset name, while
`sound/` does not.

The leading `sound/` component is supplied by the tooling and does not appear
in the zone definition. The remainder of the path, `whizbys/`, forms part of
the asset name.

For example, the zone definition entry:

```
loadedsound,whizbys/example.wav
```

is built from `sound/whizbys/example.wav`.

The retail zones use entries such as:

```
loadedsound,whizbys/bullet_whizby_01.wav
loadedsound,whizbys/bullet_whizby_02.wav
loadedsound,whizbys/bullet_whizby_03.wav
```

| | |
| --- | --- |
| Zone definition type | `loadedsound` |
| Extension | `.wav` |
| Retail occurrence | 2 of the 116 English zones |

See [the project layout](../../README.md) for how this directory fits into the
tree as a whole.
