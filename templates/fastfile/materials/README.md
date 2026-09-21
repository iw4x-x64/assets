# `materials/`

The `materials/` directory holds material definitions in JSON form. A material
binds texture maps to a technique set and carries the render state used to
draw them, which makes it the join between `images/` and `techsets/`.
Materials are usually the most numerous authored asset in a zone.

The directory name is supplied by the tooling and does not appear in the zone
definition, which names the asset on its own.

For example, the zone definition entry:

```
material,mc/mtl_example
```

is built from `materials/mc/mtl_example.json`.

The subdirectories below are a naming convention rather than an engine
requirement. A material in `mc/` is named `mc/<name>`, because the
subdirectory forms part of the asset name while `materials/` does not.

Note that a material referencing an image that the zone does not provide will
fail the build, so the corresponding `image` entries belong in the same zone
definition unless a loaded zone supplies them.

The retail zones use entries such as:

```
material,$additive
material,$default
```

| | |
| --- | --- |
| Zone definition type | `material` |
| Extension | `.json` |
| Retail occurrence | 110 of the 116 English zones |

See [the project layout](../README.md) for how this directory fits into the
tree as a whole.
