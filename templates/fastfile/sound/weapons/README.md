# `sound/weapons/`

The `sound/weapons/` directory holds weapon audio. The category and the `.wav`
extension both form part of the asset name, while `sound/` does not.

The leading `sound/` component is supplied by the tooling and does not appear
in the zone definition. The remainder of the path, `weapons/`, forms part of
the asset name.

For example, the zone definition entry:

```
loadedsound,weapons/example.wav
```

is built from `sound/weapons/example.wav`.

The retail zones use entries such as:

```
loadedsound,weapons/50cal/weap_50cal_slst_21e.wav
loadedsound,weapons/50cal/weap_50cal_temp_v2.wav
loadedsound,weapons/abrams_120/weap_abrams120mm_fire1v6.wav
```

| | |
| --- | --- |
| Zone definition type | `loadedsound` |
| Extension | `.wav` |
| Retail occurrence | 53 of the 116 English zones |

See [the project layout](../../README.md) for how this directory fits into the
tree as a whole.
