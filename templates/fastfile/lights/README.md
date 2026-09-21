# `lights/`

The `lights/` directory holds light definitions, one extensionless file each,
describing a light's attenuation and projection. They are referred to by name
from world lighting data.

The directory name is supplied by the tooling and does not appear in the zone
definition, which names the asset on its own.

For example, the zone definition entry:

```
lightdef,florescent
```

is built from `lights/florescent`.

The retail zones use entries such as:

```
lightdef,florescent
lightdef,light_dynamic
```

| | |
| --- | --- |
| Zone definition type | `lightdef` |
| Extension | none |
| Retail occurrence | 50 of the 116 English zones |

See [the project layout](../README.md) for how this directory fits into the
tree as a whole.
