# `sound/events/`

The `sound/events/` directory holds audio played by scripted events. The
category and the `.wav` extension both form part of the asset name, while
`sound/` does not.

The leading `sound/` component is supplied by the tooling and does not appear
in the zone definition. The remainder of the path, `events/`, forms part of
the asset name.

For example, the zone definition entry:

```
loadedsound,events/example.wav
```

is built from `sound/events/example.wav`.

The retail zones use entries such as:

```
loadedsound,events/alarm_metal_detector1.wav
loadedsound,events/elev_bell_ding1.wav
loadedsound,events/elev_door_close1.wav
```

| | |
| --- | --- |
| Zone definition type | `loadedsound` |
| Extension | `.wav` |
| Retail occurrence | 51 of the 116 English zones |

See [the project layout](../../README.md) for how this directory fits into the
tree as a whole.
