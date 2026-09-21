# `sound/footsteps/`

The `sound/footsteps/` directory holds footstep audio. The category and the
`.wav` extension both form part of the asset name, while `sound/` does not.

The leading `sound/` component is supplied by the tooling and does not appear
in the zone definition. The remainder of the path, `footsteps/`, forms part of
the asset name.

For example, the zone definition entry:

```
loadedsound,footsteps/example.wav
```

is built from `sound/footsteps/example.wav`.

The retail zones use entries such as:

```
loadedsound,footsteps/crawl01.wav
loadedsound,footsteps/crawl02.wav
loadedsound,footsteps/foot_carpet01.wav
```

| | |
| --- | --- |
| Zone definition type | `loadedsound` |
| Extension | `.wav` |
| Retail occurrence | 25 of the 116 English zones |

See [the project layout](../../README.md) for how this directory fits into the
tree as a whole.
