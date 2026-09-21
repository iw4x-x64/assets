# `sound/airplane/`

The `sound/airplane/` directory holds aircraft audio. The category and the
`.wav` extension both form part of the asset name, while `sound/` does not.

The leading `sound/` component is supplied by the tooling and does not appear
in the zone definition. The remainder of the path, `airplane/`, forms part of
the asset name.

For example, the zone definition entry:

```
loadedsound,airplane/example.wav
```

is built from `sound/airplane/example.wav`.

The retail zones use entries such as:

```
loadedsound,airplane/mrk_heartbeat_slowmo.wav
```

| | |
| --- | --- |
| Zone definition type | `loadedsound` |
| Extension | `.wav` |
| Retail occurrence | 3 of the 116 English zones |

See [the project layout](../../README.md) for how this directory fits into the
tree as a whole.
