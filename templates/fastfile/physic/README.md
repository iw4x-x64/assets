# `physic/`

The `physic/` directory holds physics presets, one extensionless file each,
describing mass, friction, bounce and related properties. A model refers to a
preset by name.

The directory name is supplied by the tooling and does not appear in the zone
definition, which names the asset on its own.

For example, the zone definition entry:

```
physpreset,airdrop_crate_big
```

is built from `physic/airdrop_crate_big`.

Note that the directory name is singular and is not `physics/`.

The retail zones use entries such as:

```
physpreset,,airdrop_crate_big
physpreset,airdrop_crate_big
```

| | |
| --- | --- |
| Zone definition type | `physpreset` |
| Extension | none |
| Retail occurrence | 54 of the 116 English zones |

See [the project layout](../README.md) for how this directory fits into the
tree as a whole.
