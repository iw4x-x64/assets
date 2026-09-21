# `tracer/`

The `tracer/` directory holds tracer definitions, one extensionless file each,
giving the material, width, length, speed and colour of a round's visible
trail. Weapons refer to them by name.

The directory name is supplied by the tooling and does not appear in the zone
definition, which names the asset on its own.

For example, the zone definition entry:

```
tracer,assaultrifle
```

is built from `tracer/assaultrifle`.

The retail zones use entries such as:

```
tracer,assaultrifle
tracer,,defaulttracer
```

| | |
| --- | --- |
| Zone definition type | `tracer` |
| Extension | none |
| Retail occurrence | 27 of the 116 English zones |

See [the project layout](../README.md) for how this directory fits into the
tree as a whole.
