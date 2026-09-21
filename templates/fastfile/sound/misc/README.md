# `sound/misc/`

The `sound/misc/` directory holds audio that belongs to no other category. The
category and the `.wav` extension both form part of the asset name, while
`sound/` does not.

The leading `sound/` component is supplied by the tooling and does not appear
in the zone definition. The remainder of the path, `misc/`, forms part of the
asset name.

For example, the zone definition entry:

```
loadedsound,misc/example.wav
```

is built from `sound/misc/example.wav`.

The retail zones use entries such as:

```
loadedsound,misc/alarm_altitude_01_short.wav
loadedsound,misc/alarm_altitude_loop02.wav
loadedsound,misc/alarm_missile_incoming_01.wav
```

| | |
| --- | --- |
| Zone definition type | `loadedsound` |
| Extension | `.wav` |
| Retail occurrence | 34 of the 116 English zones |

See [the project layout](../../README.md) for how this directory fits into the
tree as a whole.
