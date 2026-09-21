# `sound/mp/`

The `sound/mp/` directory holds audio used only in multiplayer. The category
and the `.wav` extension both form part of the asset name, while `sound/` does
not.

The leading `sound/` component is supplied by the tooling and does not appear
in the zone definition. The remainder of the path, `mp/`, forms part of the
asset name.

For example, the zone definition entry:

```
loadedsound,mp/example.wav
```

is built from `sound/mp/example.wav`.

The retail zones use entries such as:

```
loadedsound,mp/mp_experiencefill_onesecond.wav
loadedsound,mp/mp_flag_lost_hit01.wav
loadedsound,mp/mp_painkiller_lp01.wav
```

| | |
| --- | --- |
| Zone definition type | `loadedsound` |
| Extension | `.wav` |
| Retail occurrence | 3 of the 116 English zones |

See [the project layout](../../README.md) for how this directory fits into the
tree as a whole.
