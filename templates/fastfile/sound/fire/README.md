# `sound/fire/`

The `sound/fire/` directory holds fire audio. The category and the `.wav`
extension both form part of the asset name, while `sound/` does not.

The leading `sound/` component is supplied by the tooling and does not appear
in the zone definition. The remainder of the path, `fire/`, forms part of the
asset name.

For example, the zone definition entry:

```
loadedsound,fire/example.wav
```

is built from `sound/fire/example.wav`.

The retail zones use entries such as:

```
loadedsound,fire/fire_med_loop02_res.wav
loadedsound,fire/fire_metal_lrg1v2res.wav
loadedsound,fire/fire_metal_med1v2res.wav
```

| | |
| --- | --- |
| Zone definition type | `loadedsound` |
| Extension | `.wav` |
| Retail occurrence | 51 of the 116 English zones |

See [the project layout](../../README.md) for how this directory fits into the
tree as a whole.
