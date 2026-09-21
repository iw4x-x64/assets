# `fx/props/`

The `fx/props/` directory holds effects attached to props. The category forms
part of the asset name while `fx/` does not.

The leading `fx/` component is supplied by the tooling and does not appear in
the zone definition. The remainder of the path, `props/`, forms part of the
asset name.

For example, the zone definition entry:

```
fx,props/example
```

is built from `fx/props/example.efx`.

The retail zones use entries such as:

```
fx,props/american_smoke_grenade
fx,props/american_smoke_grenade_mp
fx,props/arcade_machine_coins
```

| | |
| --- | --- |
| Zone definition type | `fx` |
| Extension | `.efx` |
| Retail occurrence | 49 of the 116 English zones |

See [the project layout](../../README.md) for how this directory fits into the
tree as a whole.
