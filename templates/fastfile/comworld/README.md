# `comworld/`

The `comworld/` directory holds compiled lighting data for a map, principally
the light set used for static lighting.

This is compiled output. A `.map` source compiles into it and cannot be
recovered from it, so the files here are best treated as build artefacts of
the map pipeline rather than as editable sources.

The directory name is supplied by the tooling and does not appear in the zone
definition, which names the asset on its own.

For example, the zone definition entry:

```
comworld,maps/af_caves.d3dbsp
```

is built from `comworld/maps/af_caves.d3dbsp.json`.

Note that the `.d3dbsp` suffix belongs to the asset name and `.json` is
appended to it, so the file on disk ends in `.d3dbsp.json`.

The retail zones use entries such as:

```
comworld,maps/af_caves.d3dbsp
comworld,maps/mp/mp_afghan.d3dbsp
```

| | |
| --- | --- |
| Zone definition type | `comworld` |
| Retail occurrence | 49 of the 116 English zones |

See [the project layout](../README.md) for how this directory fits into the
tree as a whole.
