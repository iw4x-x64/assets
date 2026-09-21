# `phys_collmaps/`

The `phys_collmaps/` directory holds collision shapes for models that are
simulated by the physics system. Each asset is a pair of files: a `.map`
carrying the brush geometry and a `.json` beside it carrying the collision
metadata. Both are required.

The directory name is supplied by the tooling and does not appear in the zone
definition, which names the asset on its own.

For example, the zone definition entry:

```
physcollmap,accessories_gas_canister_1
```

is built from `phys_collmaps/accessories_gas_canister_1.map`.

The retail zones use entries such as:

```
physcollmap,accessories_gas_canister_1
physcollmap,accessories_sack_coffee
```

| | |
| --- | --- |
| Zone definition type | `physcollmap` |
| Extension | `.map`, `.json` |
| Retail occurrence | 69 of the 116 English zones |

See [the project layout](../README.md) for how this directory fits into the
tree as a whole.
