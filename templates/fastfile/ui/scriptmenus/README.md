# `ui/scriptmenus/`

The `ui/scriptmenus/` directory holds menus that are opened by script rather
than directly by the interface.

A `menu` name is bare and carries no directory, so neither `ui/` nor
`scriptmenus/` appears in the zone definition. The file is found by name
wherever it sits below the project.

For example, the zone definition entry:

```
menu,example
```

is built from `ui/scriptmenus/example.menu`.

The retail zones use entries such as:

```
menu,ac130_hud_hd
menu,ac130_hud_sd
```

| | |
| --- | --- |
| Zone definition type | `menu` |
| Extension | `.menu` |
| Retail occurrence | 26 of the 116 English zones |

See [the project layout](../../README.md) for how this directory fits into the
tree as a whole.
