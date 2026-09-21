# `sound/`

The `sound/` directory holds the audio data for `LoadedSound` assets, grouped
into the category subdirectories listed below.

The directory name is supplied by the tooling and does not appear in the zone
definition, which names the asset on its own.

For example, the zone definition entry:

```
loadedsound,ac130/ac130_40mm_fire_c2.wav
```

is built from `sound/ac130/ac130_40mm_fire_c2.wav`.

Note that the asset name includes both the category and the `.wav` extension,
but not the `sound/` prefix.

The named handles that scripts, weapons and effects actually use are sound
aliases and live in `soundaliases/`. A zone that plays audio normally needs
entries in both directories.

The retail zones use entries such as:

```
loadedsound,ac130/ac130_40mm_fire_c2.wav
loadedsound,amb_elements/elm_ac130_hydraulics08.wav
```

| | |
| --- | --- |
| Zone definition type | `loadedsound` |
| Extension | `.wav`, `.csv` |
| Retail occurrence | 75 of the 116 English zones |

See [the project layout](../README.md) for how this directory fits into the
tree as a whole.
