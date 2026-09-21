# Fastfile project template

This directory is a starting point for a new IW4 x64 fastfile project.
The usual way to use it is to copy the whole tree into `zone_raw/` and
then rename the zone definition to the name of the project:

```
cp -r templates/fastfile zone_raw/my_project
mv zone_raw/my_project/zone_source/{TEMPLATE,my_project}.zone
```

The name of the `.zone` file matters here. The Linker uses it to find
the build target, and from that target it gets the project name used in
its search paths. So, for a project called `my_project`, we want
`zone_source/my_project.zone`.

Now, most of the directories in this template would normally be empty.
Each one contains a `README.md` partly to keep it in git and partly to
document what the Linker expects to find there. Once the template has
been copied, those files no longer serve the first purpose and can be
removed:

```
find zone_raw/my_project -name README.md -delete
```

There is no need to keep the entire directory tree either. The Linker
only looks for files required by the assets named in the zone
definition. So if, say, the project has no models, removing `xmodel/`
and `model_export/` has no effect on the resulting fastfile. Keeping
such directories is mostly useful when discovering the layout or when
they are expected to gain files later.

## Layout

The directory tree is arranged to fit the Linker's normal search paths.
In particular, a project under `zone_raw/<project>/` can refer to its
files without adding project-specific search path options:

| Search path | Default                                                                              |
| ----------- | ------------------------------------------------------------------------------------ |
| asset       | `?bin?/raw/?game?;?base?/raw;?base?/raw/?game?;?base?/zone_raw/?project?`            |
| source      | `?base?/zone_source;?base?/zone_raw/?project?;?base?/zone_raw/?project?/zone_source` |
| gdt         | `?base?/source_data;?base?/zone_raw/?project?/source_data`                           |

Here `?base?` is the directory against which the Linker is invoked.
`?project?` comes from the project being built. `?game?` is the short
game name, and `?bin?` is the directory containing the Linker.

The distinction between the asset and source search paths is worth
keeping in mind. A zone definition is found through the source path.
Most files named by assets are found through the asset path. GDT source
data has its own path. Since `zone_raw/<project>/` occurs in the
relevant defaults, the template can place all of these underneath one
project directory without teaching the Linker another layout.

## How a name maps to a path

Perhaps the slightly confusing part of the layout is that a directory
name does not always form part of the asset name.

For many asset types the directory is implied by the type itself. If the
zone contains:

```
fx,muzzleflashes/pistolflash
```

then the Linker looks under `fx/` and reads:

```
fx/muzzleflashes/pistolflash.efx
```

So writing `fx/muzzleflashes/pistolflash` as the asset name would repeat
a piece of information the `fx` asset loader already supplies.

The same rule gives us, for example:

```
loadedsound,ac130/engine.wav
image,example_image
weapon,uzi_akimbo
```

with their files at:

```
sound/ac130/engine.wav
images/example_image.iwi
weapons/uzi_akimbo
```

Notice that the filename conventions differ between asset types. An
image name drops the `.iwi` extension, a loaded sound keeps `.wav`, and
a weapon has no extension at all. This is intentional. The asset reader
for each type defines how its logical name is turned into a filename.

Rawfiles work differently. Their asset name is already a path relative
to the asset search root, so the directory and extension remain part of
the name:

```
rawfile,animscripts/dog/dog_combat.gsc
rawfile,character/char_example.gsc
```

In these cases there is no `rawfile/` directory for the Linker to
prepend. The name after `rawfile,` is the path it is trying to resolve.

There is one more case in this template where the directory does not
appear in the zone definition at all. Files under `accuracy/` belong to
the on-disk representation of a weapon. They are produced by the weapon
dumper and named from the weapon data that refers to them. So an
accuracy curve is not an asset that should be added to the zone
independently.

A useful way to read the tree, then, is to start with the asset type in
the zone definition and ask what that asset reader expects. Some readers
supply their own directory and filename convention. A rawfile supplies
its path directly. A few files exist only as backing data for another
asset.

## Directories

The table below gives the top-level layout. The `README.md` inside each
directory goes into the format used there and, where useful, points out
how the same asset appears in retail data.

### Directories selected by an asset reader

For these directories the asset type tells the Linker where to look. The
directory name itself normally does not appear at the front of the asset
name.

| Directory                   | Zone definition type              | Extension          |
| --------------------------- | --------------------------------- | ------------------ |
| `zone_source/`              | none, holds `<project>.zone`      | `.zone`            |
| `english/localizedstrings/` | `localize`                        | `.str`             |
| `images/`                   | `image`                           | `.iwi`, `.dds`     |
| `materials/`                | `material`                        | `.json`            |
| `techsets/`                 | `techniqueset`                    | `.techset`         |
| `techniques/`               | none, named by a technique set    | `.tech`            |
| `shader_bin/`               | `pixelshader`, `vertexshader`     | `.cso`             |
| `vertexdecl/`               | `vertexdecl`                      | `.json`            |
| `xmodel/`                   | `xmodel`                          | `.json`            |
| `model_export/`             | none, named by a model definition | `.glb`             |
| `xanim/`                    | `xanim`                           | none               |
| `fx/`                       | `fx`                              | `.efx`             |
| `sound/`                    | `loadedsound`                     | `.wav`             |
| `soundaliases/`             | `sound`, `soundcurve`             | `.csv`, `.vfcurve` |
| `weapons/`                  | `weapon`                          | none               |
| `physic/`                   | `physpreset`                      | none               |
| `phys_collmaps/`            | `physcollmap`                     | `.map` and `.json` |
| `lights/`                   | `lightdef`                        | none               |
| `tracer/`                   | `tracer`                          | none               |
| `vehicles/`                 | `vehicle`                         | none               |
| `fonts/`                    | `font`                            | `.json`            |
| `impactfx/`                 | `impactfx`                        | `.json`            |
| `leaderboards/`             | `leaderboard`                     | `.json`            |
| `clipmap_mp/maps/`          | `clipmap`                         | `.json`            |
| `comworld/maps/`            | `comworld`                        | `.json`            |
| `fxworld/maps/`             | `fxworld`                         | `.json`            |
| `gameworld_mp/maps/`        | `gameworldmp`                     | `.json`            |
| `gameworld_sp/maps/`        | `gameworldsp`                     | `.json`            |
| `gfxworld/maps/`            | `gfxworld`                        | `.json`            |
| `ui/`, `ui_mp/`             | `menu`, `menulist`                | `.menu`, `.txt`    |

A few entries in this table have no zone type of their own. For example,
`model_export/` contains data named by an `xmodel`, and `techniques/`
contains data named by a technique set. They still live in directories
selected by the reader of the owning asset.

### Directories that form part of the asset name

These paths are normally loaded as `rawfile`. Here the path under the
project root is the asset name, so keep the directory and filename
extension in the zone definition.

| Directory         | Contents                                                     |
| ----------------- | ------------------------------------------------------------ |
| `aim_assist/`     | aim assist curves                                            |
| `aitype/`         | AI archetype scripts                                         |
| `animscripts/`    | character animation state scripts                            |
| `animtrees/`      | animation trees                                              |
| `character/`      | character definitions                                        |
| `codescripts/`    | scripts the engine calls of its own accord                   |
| `common_scripts/` | the shared script library                                    |
| `info/`           | assorted engine information files                            |
| `maps/`           | level scripts, and `mapents` and `addonmapents` entity lists |
| `mp/`             | multiplayer tables, as `stringtable` and `structureddatadef` |
| `mptype/`         | multiplayer character type scripts                           |
| `radiant/`        | Radiant editor data                                          |
| `rumble/`         | controller vibration patterns                                |
| `scriptdebugger/` | script debugger data                                         |
| `shock/`          | shellshock definitions                                       |
| `sp/`             | singleplayer tables, as `stringtable`                        |
| `vehicle/`        | vehicle curve definitions                                    |
| `video/`          | video playback tables                                        |
| `vision/`         | colour grading and tone mapping files                        |
| `xmodelalias/`    | model alias lists                                            |

For example, a file at:

```
character/char_example.gsc
```

is named in the zone as:

```
rawfile,character/char_example.gsc
```

There is no extra mapping hidden here. The rawfile name is the path.

### Files written as part of another asset

The accuracy files are a little different again:

| Directory                                  | Written by          | Format                    |
| ------------------------------------------ | ------------------- | ------------------------- |
| `accuracy/aivsai/`, `accuracy/aivsplayer/` | the `weapon` dumper | `.accu`, `WEAPONACCUFILE` |

These files belong to a weapon's serialized representation. The weapon
refers to them by name, and the dumper writes them when it writes the
weapon. They should not be added to the zone definition as separate
assets.

## Points to watch

There are a few names in this tree that look more related than they
really are. The easiest one to trip over is `vehicle/` versus
`vehicles/`.

`vehicles/` is where the `vehicle` asset reader looks for vehicle
assets. The singular `vehicle/` directory contains curve files loaded as
rawfiles. Both forms occur in the retail data, so neither spelling is an
alias for the other.

Localized strings have another slightly surprising rule. The Linker
reads them from:

```
english/localizedstrings/
```

This path remains `english/localizedstrings/` when building text for
another language. IW4MS sets the zone language to `LANGUAGE_NONE`, which
OAT maps to the string `english`, and the localized string reader takes
the `LANG_ENGLISH` value from each reference.

So `english` in this path is really part of the import convention used
by this toolchain. It is not selecting the language of the fastfile. To
build another translation, give the Linker a project tree whose
`english/localizedstrings/` contains that translation.

Note that retail `.str` files use CP1252. Text outside ASCII needs to
remain in that encoding when it is committed and checked out. Set the
corresponding `.gitattributes` rule before adding such a file; otherwise
git may leave the working tree with bytes that the game no longer
interprets as the intended text.

Finally, asset names and directory names share the same project tree,
and a name can occupy both roles. Retail `ui.ff`, for example, contains:

```
rawfile,ui
```

and has menu files under:

```
ui/
```

OAT currently reports the rawfile as dumped even though it cannot create
a file called `ui` where the `ui/` directory already exists.

So avoid giving a rawfile the same path as a directory created for
another asset. Once a directory exists at that path, the rawfile dumper
has nowhere to write the file.
