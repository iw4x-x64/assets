# `sound/bodyfalls/`

The `sound/bodyfalls/` directory holds audio for bodies striking surfaces. The
category and the `.wav` extension both form part of the asset name, while
`sound/` does not.

The leading `sound/` component is supplied by the tooling and does not appear
in the zone definition. The remainder of the path, `bodyfalls/`, forms part of
the asset name.

For example, the zone definition entry:

```
loadedsound,bodyfalls/example.wav
```

is built from `sound/bodyfalls/example.wav`.

The retail zones use entries such as:

```
loadedsound,bodyfalls/bodyfall_dirt01.wav
loadedsound,bodyfalls/bodyfall_dirt02.wav
loadedsound,bodyfalls/bodyfall_dirt03.wav
```

| | |
| --- | --- |
| Zone definition type | `loadedsound` |
| Extension | `.wav` |
| Retail occurrence | 51 of the 116 English zones |

See [the project layout](../../README.md) for how this directory fits into the
tree as a whole.
