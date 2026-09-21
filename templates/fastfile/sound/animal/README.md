# `sound/animal/`

The `sound/animal/` directory holds animal audio. The category and the `.wav`
extension both form part of the asset name, while `sound/` does not.

The leading `sound/` component is supplied by the tooling and does not appear
in the zone definition. The remainder of the path, `animal/`, forms part of
the asset name.

For example, the zone definition entry:

```
loadedsound,animal/example.wav
```

is built from `sound/animal/example.wav`.

The retail zones use entries such as:

```
loadedsound,animal/animal_chicken_disturbed1.wav
loadedsound,animal/animal_chicken_disturbed2.wav
loadedsound,animal/animal_chicken_disturbed3.wav
```

| | |
| --- | --- |
| Zone definition type | `loadedsound` |
| Extension | `.wav` |
| Retail occurrence | 13 of the 116 English zones |

See [the project layout](../../README.md) for how this directory fits into the
tree as a whole.
