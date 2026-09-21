# `sound/physics/`

The `sound/physics/` directory holds audio for physics impacts. The category
and the `.wav` extension both form part of the asset name, while `sound/` does
not.

The leading `sound/` component is supplied by the tooling and does not appear
in the zone definition. The remainder of the path, `physics/`, forms part of
the asset name.

For example, the zone definition entry:

```
loadedsound,physics/example.wav
```

is built from `sound/physics/example.wav`.

The retail zones use entries such as:

```
loadedsound,physics/default_bump_temp.wav
loadedsound,physics/dest_cmptrmonitor01.wav
loadedsound,physics/dest_cmptrmonitor02.wav
```

| | |
| --- | --- |
| Zone definition type | `loadedsound` |
| Extension | `.wav` |
| Retail occurrence | 51 of the 116 English zones |

See [the project layout](../../README.md) for how this directory fits into the
tree as a whole.
