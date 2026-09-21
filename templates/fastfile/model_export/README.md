# `model_export/`

The `model_export/` directory holds the mesh geometry for the definitions in
`xmodel/`, one file per level of detail. A file here is named by the model
definition that owns it and is never listed in a zone definition on its own.

This directory does not appear in a zone definition. Its files are written by
the dumper of another asset and are referenced by name from within that asset.

Files here are named `model_export/example_model_lod0.glb`.

| | |
| --- | --- |
| Zone definition type | none |
| Extension | `.glb` |
| Retail occurrence | 77 of the 116 English zones |

See [the project layout](../README.md) for how this directory fits into the
tree as a whole.
