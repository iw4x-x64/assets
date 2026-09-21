# `sound/vehicles/`

The `sound/vehicles/` directory holds vehicle audio. The category and the
`.wav` extension both form part of the asset name, while `sound/` does not.

The leading `sound/` component is supplied by the tooling and does not appear
in the zone definition. The remainder of the path, `vehicles/`, forms part of
the asset name.

For example, the zone definition entry:

```
loadedsound,vehicles/example.wav
```

is built from `sound/vehicles/example.wav`.

The retail zones use entries such as:

```
loadedsound,vehicles/airport_tire_skid_2.wav
loadedsound,vehicles/horn_beep.wav
loadedsound,vehicles/mrk_tank_03_idle.wav
```

| | |
| --- | --- |
| Zone definition type | `loadedsound` |
| Extension | `.wav` |
| Retail occurrence | 24 of the 116 English zones |

See [the project layout](../../README.md) for how this directory fits into the
tree as a whole.
