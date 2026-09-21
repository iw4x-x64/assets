# `english/`

The `english/` directory is the parent of `localizedstrings/`. Its name is a
constant in this pipeline rather than a selector, and a sibling directory
named after another language has no effect.

The directory name is supplied by the tooling and does not appear in the zone
definition, which names the asset on its own.

The IW4MS zone loader sets the zone language to `LANGUAGE_NONE`, which OAT
maps to the string `english`. The Linker therefore reads
`english/localizedstrings/` whatever language the text in it is actually
written in. Producing a fastfile in another language means pointing the Linker
at a different tree whose `english/localizedstrings/` holds that language's
text, not adding a directory beside this one.

| | |
| --- | --- |
| Zone definition type | none |
| Retail occurrence | 50 of the 116 English zones |

See [the project layout](../README.md) for how this directory fits into the
tree as a whole.
