# `vehicles/`

The `vehicles/` directory holds vehicle definitions, one extensionless file
each, written in the info string format. A definition covers handling, health,
the models the vehicle uses, its sound aliases and its turret configuration.

The directory name is supplied by the tooling and does not appear in the zone
definition, which names the asset on its own.

For example, the zone definition entry:

```
vehicle,blackhawk
```

is built from `vehicles/blackhawk`.

Note that this directory is plural. The singular `vehicle/` directory is
unrelated and holds rawfile curve definitions. Both occur in retail zones, and
confusing the two produces an asset that cannot be resolved.

The retail zones use entries such as:

```
vehicle,blackhawk
vehicle,cobra
```

| | |
| --- | --- |
| Zone definition type | `vehicle` |
| Extension | none |
| Retail occurrence | 27 of the 116 English zones |

See [the project layout](../README.md) for how this directory fits into the
tree as a whole.
