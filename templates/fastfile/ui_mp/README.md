# `ui_mp/`

The `ui_mp/` directory holds the menu definitions for the multiplayer
interface, together with the menu lists that group them. A `menu` entry names
a single menu, whereas a `menulist` entry names a `.txt` file that in turn
pulls in many.

The directory name is supplied by the tooling and does not appear in the zone
definition, which names the asset on its own.

For example, the zone definition entry:

```
menulist,ui_mp/example.txt
```

is built from `ui_mp/example.txt`.

Note that the two entry types are named differently. A `menu` name is bare and
carries no directory, while a `menulist` name includes the `ui_mp/` prefix
because the prefix belongs to that asset's name.

The Linker accepts `--menu-permissive` to allow script commands it does not
recognise, and `--menu-no-optimization` to keep parsed menus closer to their
source at the cost of size and performance.

Avoid giving a rawfile the same name as this directory. Retail `ui.ff`
declares `rawfile,ui` while its menus occupy a `ui/` directory, and OAT fails
to write the rawfile while still reporting that it dumped it.

The retail zones use entries such as:

```
menulist,ui_mp/barracks.menu
menulist,ui_mp/code.txt
menulist,ui_mp/gamesetup_popup.menu
```

| | |
| --- | --- |
| Zone definition type | `menu`, `menulist` |
| Extension | `.menu`, `.txt` |
| Retail occurrence | 5 of the 116 English zones |

See [the project layout](../README.md) for how this directory fits into the
tree as a whole.
