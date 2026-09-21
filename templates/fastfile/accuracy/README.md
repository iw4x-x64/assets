# `accuracy/`

The `accuracy/` directory holds the accuracy curves used when AI fire a
weapon. A weapon definition names its accuracy graphs and the curves are
written here as a consequence, so they are never listed in a zone definition
themselves.

This directory does not appear in a zone definition. Its files are written by
the dumper of another asset and are referenced by name from within that asset.

Files here are named `accuracy/aivsai/pistol.accu`.

The files are written by `AccuracyGraphWriter` and begin with the header
`WEAPONACCUFILE`, followed by a knot count and one `x y` pair per line.

Note that this can be confirmed against the retail data: no `.accu` file
matches any entry in any of the 116 English zone definitions.

| | |
| --- | --- |
| Zone definition type | none |
| Retail occurrence | 45 of the 116 English zones |

See [the project layout](../README.md) for how this directory fits into the
tree as a whole.
