# `fonts/`

The `fonts/` directory holds font assets in JSON form, comprising the glyph
table and metrics.

Unusually for a directory the tooling supplies, the asset name here begins
with `fonts/`, because that prefix is part of the name as the game stores it.
The entry therefore repeats the directory.

For example, the zone definition entry:

```
font,fonts/bigFont
```

is built from `fonts/bigFont.json`.

Note that the asset name here begins with `fonts/` even though this is
otherwise a directory the tooling supplies. The prefix is part of the name as
the game stores it, so the entry repeats the directory.

The material a font is drawn with lives in `materials/fonts/`.

The retail zones use entries such as:

```
font,fonts/bigDevFont
font,fonts/bigFont
font,fonts/boldFont
```

| | |
| --- | --- |
| Zone definition type | `font` |
| Extension | `.json` |
| Retail occurrence | 3 of the 116 English zones |

See [the project layout](../README.md) for how this directory fits into the
tree as a whole.
