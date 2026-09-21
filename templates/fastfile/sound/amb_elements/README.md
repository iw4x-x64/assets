# `sound/amb_elements/`

The `sound/amb_elements/` directory holds ambient element loops. The category
and the `.wav` extension both form part of the asset name, while `sound/` does
not.

The leading `sound/` component is supplied by the tooling and does not appear
in the zone definition. The remainder of the path, `amb_elements/`, forms part
of the asset name.

For example, the zone definition entry:

```
loadedsound,amb_elements/example.wav
```

is built from `sound/amb_elements/example.wav`.

The retail zones use entries such as:

```
loadedsound,amb_elements/elm_ac130_hydraulics08.wav
loadedsound,amb_elements/elm_thunder_dist1.wav
loadedsound,amb_elements/elm_thunder_dist2.wav
```

| | |
| --- | --- |
| Zone definition type | `loadedsound` |
| Extension | `.wav` |
| Retail occurrence | 13 of the 116 English zones |

See [the project layout](../../README.md) for how this directory fits into the
tree as a whole.
