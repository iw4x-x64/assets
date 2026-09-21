# `sound/ac130/`

The `sound/ac130/` directory holds audio for the AC-130 gunship. The category
and the `.wav` extension both form part of the asset name, while `sound/` does
not.

The leading `sound/` component is supplied by the tooling and does not appear
in the zone definition. The remainder of the path, `ac130/`, forms part of the
asset name.

For example, the zone definition entry:

```
loadedsound,ac130/example.wav
```

is built from `sound/ac130/example.wav`.

The retail zones use entries such as:

```
loadedsound,ac130/ac130_105canon_fire.wav
loadedsound,ac130/ac130_105canon_reload.wav
loadedsound,ac130/ac130_25mm_fire_rev01sh2.wav
```

| | |
| --- | --- |
| Zone definition type | `loadedsound` |
| Extension | `.wav` |
| Retail occurrence | 3 of the 116 English zones |

See [the project layout](../../README.md) for how this directory fits into the
tree as a whole.
