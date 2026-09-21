# `sound/foley/`

The `sound/foley/` directory holds foley audio for character movement. The
category and the `.wav` extension both form part of the asset name, while
`sound/` does not.

The leading `sound/` component is supplied by the tooling and does not appear
in the zone definition. The remainder of the path, `foley/`, forms part of the
asset name.

For example, the zone definition entry:

```
loadedsound,foley/example.wav
```

is built from `sound/foley/example.wav`.

The retail zones use entries such as:

```
loadedsound,foley/foly_chemlight_crack_v1.wav
loadedsound,foley/foly_chemlight_crack_v2.wav
loadedsound,foley/foly_chemlight_crack_v3.wav
```

| | |
| --- | --- |
| Zone definition type | `loadedsound` |
| Extension | `.wav` |
| Retail occurrence | 45 of the 116 English zones |

See [the project layout](../../README.md) for how this directory fits into the
tree as a whole.
