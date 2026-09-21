# `xmodel/`

The `xmodel/` directory holds model definitions in JSON form. A definition
carries the level of detail list, the materials the model is drawn with, and
its bone and collision information. The definition is the asset; the mesh data
it refers to lives in `model_export/`.

The directory name is supplied by the tooling and does not appear in the zone
definition, which names the asset on its own.

For example, the zone definition entry:

```
xmodel,example_model
```

is built from `xmodel/example_model.json`.

Each level of detail is a separate mesh file, suffixed `_lod0`, `_lod1` and so
on. The Linker reads mesh data according to the extension named in the JSON
and accepts `.glb` and `.gltf`.

Note that the Unlinker can also write `XMODEL_EXPORT`, `XMODEL_BIN` and `OBJ`
through `--model-format`, but only the glTF formats can be read back, so a
tree intended for rebuilding should keep the default.

The retail zones use entries such as:

```
xmodel,727_coach_seat01
xmodel,727_overhead_door
```

| | |
| --- | --- |
| Zone definition type | `xmodel` |
| Extension | `.json` |
| Retail occurrence | 77 of the 116 English zones |

See [the project layout](../README.md) for how this directory fits into the
tree as a whole.
