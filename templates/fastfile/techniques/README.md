# `techniques/`

The `techniques/` directory holds the individual rendering techniques named by
the technique sets in `techsets/`. A technique in turn names the vertex and
pixel shaders it draws with, which resolve to files in `shader_bin/`.

This directory does not appear in a zone definition. Its files are written by
the dumper of another asset and are referenced by name from within that asset.

Files here are named `techniques/<name>.tech`.

Note that OAT handles shader bytecode only. It neither compiles shader source
nor recovers source from bytecode, so a technique can only refer to shaders
that already exist as compiled objects.

| | |
| --- | --- |
| Zone definition type | none |
| Extension | `.tech` |
| Retail occurrence | 103 of the 116 English zones |

See [the project layout](../README.md) for how this directory fits into the
tree as a whole.
