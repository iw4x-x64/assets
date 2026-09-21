# `sound/items/`

The `sound/items/` directory holds audio for picking up and using items. The
category and the `.wav` extension both form part of the asset name, while
`sound/` does not.

The leading `sound/` component is supplied by the tooling and does not appear
in the zone definition. The remainder of the path, `items/`, forms part of the
asset name.

For example, the zone definition entry:

```
loadedsound,items/example.wav
```

is built from `sound/items/example.wav`.

The retail zones use entries such as:

```
loadedsound,items/item_geiger_counter_lvl1.wav
loadedsound,items/item_geiger_counter_lvl2.wav
loadedsound,items/item_geiger_counter_lvl3.wav
```

| | |
| --- | --- |
| Zone definition type | `loadedsound` |
| Extension | `.wav` |
| Retail occurrence | 5 of the 116 English zones |

See [the project layout](../../README.md) for how this directory fits into the
tree as a whole.
