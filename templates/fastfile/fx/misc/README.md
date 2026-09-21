# `fx/misc/`

The `fx/misc/` directory holds effects that belong to no other category. The
category forms part of the asset name while `fx/` does not.

The leading `fx/` component is supplied by the tooling and does not appear in
the zone definition. The remainder of the path, `misc/`, forms part of the
asset name.

For example, the zone definition entry:

```
fx,misc/example
```

is built from `fx/misc/example.efx`.

The retail zones use entries such as:

```
fx,misc/105mm_tracer
fx,misc/25mm_tracer
fx,misc/40mm_tracer
```

| | |
| --- | --- |
| Zone definition type | `fx` |
| Extension | `.efx` |
| Retail occurrence | 58 of the 116 English zones |

See [the project layout](../../README.md) for how this directory fits into the
tree as a whole.
