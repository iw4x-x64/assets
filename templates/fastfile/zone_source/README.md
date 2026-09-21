# `zone_source/`

The `zone_source/` directory is where the source of a fastfile starts.
The Linker is given a target name and looks for `<target>.zone` on its
source search path. So, perhaps somewhat unusually, the file name itself
names the build target. There is no corresponding declaration inside the
file. Rename the file and, from the Linker's point of view, you have
renamed the target.

A zone definition is, at its simplest, a sequence of assets to place in
the fastfile. Each asset is written on its own line in the form
`<type>,<name>`. For example:

```text
material,white
```

The definition starts with:

```text
>game,IW4MS
```

This tells the Linker which fastfile format it is writing. `IW4MS` is
the 64-bit IW4 format used here, so this is part of the file format
selection.

Lines beginning with `//` are comments and are ignored by the Linker.

Note that `zone_source/` is a tooling convention. Its name is never
written into the zone definition and does not become part of the asset
name. The definition names the asset directly, and the build arranges
for the Linker to find the definition through its source search path.
This distinction is easy to miss when first looking at the tree since
the directory appears to provide some namespace of its own when, as far
as the Linker is concerned, it does not.

Perhaps the less obvious part of the format is the empty field between
the asset type and its name. Compare:

```text
material,white
material,,white
```

The first form defines `white` in this fastfile. The Linker reads the
material and writes the resulting asset into the zone.

The second form is a reference. It says that this fastfile uses `white`,
but does not provide it. The asset is expected to come from some zone
that the game has already loaded by the time this reference is resolved.

That extra comma is significant. Leaving it out for an asset that should
have been referenced causes another copy of the asset to be written into
the fastfile. Adding it to an asset that this zone was meant to provide
leaves the fastfile dependent on some other loaded zone providing that
asset.

The Linker cannot in practice prove that such a reference will be
satisfied at runtime. It is building one zone and does not know the
complete load state in which the game will eventually use it. So a
dangling reference can quite happily survive the build and fail much
later when the game tries to use the asset. This is why the distinction
deserves some care when editing a definition.

There are a few directives mixed in with the asset entries.

`>name,<zone>` changes the name written for the resulting fastfile.
Normally the file name already gives us the name we want, so there is no
reason to spell it twice. The directive becomes useful when the build
target and the zone shipped to the game need different names.

`include,<project>` reads another zone definition as part of this one.
This is useful for definitions that share a common body and saves us
from copying the same asset entries into each target.

`ignore,<zone>` tells the Linker that assets supplied by another zone
should not be written here. Think of this as describing an existing
ownership relationship between zones. The resulting fastfile can refer
to those assets with the expectation that the named zone supplies them.

`build,<target>` asks the Linker to build another target. This lets one
zone definition pull another build into the same invocation when the two
need to be produced together.

`>gdt,<name>` loads a GDT from the GDT search path. The path itself does
not belong in the zone definition; the Linker resolves the name using
the search paths it was given by the surrounding build.

So the `.zone` file describes what the fastfile contains and which
existing content it expects to find at runtime. The surrounding build
supplies where the source lives and where the resulting `.ff` is
installed.

|                      |                              |
| -------------------- | ---------------------------- |
| Zone definition type | none                         |
| Extension            | `.zone`                      |
| Retail occurrence    | 116 of the 116 English zones |

See [the project layout](../README.md) for how this directory fits into the
tree as a whole.
