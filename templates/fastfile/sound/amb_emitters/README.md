# `sound/amb_emitters/`

The `sound/amb_emitters/` directory holds ambient audio emitted from a
position in the world. The category and the `.wav` extension both form part of
the asset name, while `sound/` does not.

The leading `sound/` component is supplied by the tooling and does not appear
in the zone definition. The remainder of the path, `amb_emitters/`, forms part
of the asset name.

For example, the zone definition entry:

```
loadedsound,amb_emitters/example.wav
```

is built from `sound/amb_emitters/example.wav`.

The retail zones use entries such as:

```
loadedsound,amb_emitters/amb_rain_car.wav
loadedsound,amb_emitters/amb_rain_carlite.wav
loadedsound,amb_emitters/amb_rain_foliage.wav
```

| | |
| --- | --- |
| Zone definition type | `loadedsound` |
| Extension | `.wav` |
| Retail occurrence | 51 of the 116 English zones |

See [the project layout](../../README.md) for how this directory fits into the
tree as a whole.
