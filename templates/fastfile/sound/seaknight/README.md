# `sound/seaknight/`

The `sound/seaknight/` directory holds audio for the Sea Knight helicopter.
The category and the `.wav` extension both form part of the asset name, while
`sound/` does not.

The leading `sound/` component is supplied by the tooling and does not appear
in the zone definition. The remainder of the path, `seaknight/`, forms part of
the asset name.

For example, the zone definition entry:

```
loadedsound,seaknight/example.wav
```

is built from `sound/seaknight/example.wav`.

The retail zones use entries such as:

```
loadedsound,seaknight/seaknight_door_close.wav
loadedsound,seaknight/seaknight_door_open.wav
```

| | |
| --- | --- |
| Zone definition type | `loadedsound` |
| Extension | `.wav` |
| Retail occurrence | 7 of the 116 English zones |

See [the project layout](../../README.md) for how this directory fits into the
tree as a whole.
