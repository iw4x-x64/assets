# `english/localizedstrings/`

The `localizedstrings/` directory holds string tables, one `.str` file per
localize asset. A file contains a sequence of `REFERENCE` blocks, each mapping
a key used by menus and scripts to the text displayed for it. A single
`localize` entry pulls in every string in the named file.

Neither `english/` nor `localizedstrings/` appears in the zone definition. A
localize entry names the string table on its own.

For example, the zone definition entry:

```
localize,af_caves
```

is built from `english/localizedstrings/af_caves.str`.

Only the `LANG_ENGLISH` value of each reference is read, because the zone
language is always `english` here. A `LANG_FRENCH` line in the same file is
parsed and then discarded, so a single multi-language `.str` cannot be used to
produce several localized fastfiles.

Note that retail `.str` files are encoded in CP1252 rather than UTF-8. An
accented character appears as a single byte, for example `0xE9` for `e` with
an acute accent. Configure `.gitattributes` accordingly before committing text
outside ASCII, or the encoding will be corrupted.

Defining the same reference twice for one language is a parse error rather
than a warning, and it aborts the build.

The retail zones use entries such as:

```
localize,af_caves
localize,code_post_gfx
```

| | |
| --- | --- |
| Zone definition type | `localize` |
| Extension | `.str` |
| Retail occurrence | 50 of the 116 English zones |

See [the project layout](../../README.md) for how this directory fits into the
tree as a whole.
