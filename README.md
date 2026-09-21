# assets

This project builds the IW4 x64 fastfiles shipped by IW4x and installs
them into a game directory.

The actual fastfile writer is the Linker from
[open-asset-tools](https://github.com/iw4x-x64/oat). We don't carry a
copy of the Linker here. The build treats it in much the same way a
normal build treats a compiler: it knows how to invoke it, what inputs
belong to each invocation, and what output should appear when the
invocation succeeds.

There is a small complication here compared to compiling source code. A
C++ compiler can tell the build system which headers it discovered. The
Linker doesn't provide equivalent dependency information for the assets
pulled into a zone. So we have to describe that part of the dependency
graph ourselves. See [Dependency tracking](#dependency-tracking) below
for the details.

The useful result is that changing an asset causes the fastfiles which
may contain that asset to be rebuilt. A change doesn't turn into an
unconditional rebuild of the entire package.

## Requirements

We need an x64 build of the Linker.

IW4MS is the x64 release of IW4 and its fastfile format serialises pointers as
eight-byte values. The Linker checks its own architecture before writing such a
zone, so using its 32-bit build fails early with:

```text
Writing IW4MS zones needs a 64 bit build: its pointers are 8 bytes wide.
```

This check is useful since a 32-bit Linker cannot produce the file we need and
letting the build proceed any further would merely turn a configuration mistake
into a less obvious failure later.

One way of building the required Linker is:

```sh
git clone https://github.com/iw4x-x64/oat
cd oat
./generate.sh
make -C build -j$(nproc) config=release_x64 LinkerCli
```

The resulting binaries are placed in:

```text
build/bin/Release_x64/
```

Note that the make target is called `LinkerCli` but the executable it produces
is called `Linker`. The corresponding Unlinker target follows the same scheme:
`UnlinkerCli` produces `Unlinker`.

This distinction is easy to miss when copying the target name from the make
command into `config.assets.linker`, so it is worth keeping the two names
separate here.

## Building

Normally the project only needs to be configured once. Point it at the Linker
and at the game directory:

```sh
b configure                                     \
  config.assets.linker=/path/to/Linker          \
  "config.install.root='/path/to/the game'"
```

Then the usual cycle is:

```sh
b
b test
b install
b uninstall
```

There is no requirement to run `b` before `b install`. Installation has the
build as a prerequisite, so:

```sh
b install
```

is enough after changing an asset. build2 first brings the required fastfile
targets up to date and then copies their current outputs into the configured
game directory.

This is useful for the common edit-test cycle. Change an asset, run
`b install`, and the installed copy is updated from the same dependency graph
that produced the fastfile. There is no separate staging step whose contents
can drift from the build tree.

`b uninstall` follows the installation metadata in the other direction. It
removes the files this project installed. It does not treat the destination
group as a directory owned by this package, so unrelated fastfiles already
present there are left alone.

### Finding the Linker

`config.assets.linker` does not have to be set when `Linker` can be found on
`PATH`.

So, for example, a developer who has a single OAT installation in their normal
tool path can configure with just:

```sh
b configure "config.install.root='/path/to/the game'"
```

An explicit `config.assets.linker` becomes useful when the Linker lives outside
`PATH` or when several builds of OAT exist on the same machine and we want this
configuration tied to one of them.

The path is kept as project configuration for the same reason a compiler path
is normally configuration: once the build has been configured, rerunning it
should keep using the same tool instead of silently selecting whichever
executable happens to appear first in a changed environment.

### Testing

`b test` reads every produced fastfile back through the Unlinker.

The test is intentionally simple. Building a file successfully tells us that
the Linker accepted the source material. Reading it back gives us a second pass
through the format and catches a class of bad outputs that would otherwise
first appear when the game tried to load them.

By default the Unlinker is expected beside the configured Linker. This matches
the OAT build layout where the pair is produced into the same directory.

If that is not the layout being used, set `config.assets.unlinker` explicitly.

### The quoted install root

The quoting around `config.install.root` in the configure command is
intentional:

```sh
"config.install.root='/path/to/the game'"
```

There are two parsers involved here. The shell parses the command line first.
build2 then parses the value assigned to `config.install.root`.

A normal game directory can contain spaces, for example:

```text
Call of Duty Modern Warfare 2
```

The outer double quotes keep the shell from splitting the assignment. The inner
single quotes remain part of the value seen by build2 long enough for its own
parser to treat the path as one name.

Dropping that inner layer can leave build2 looking at several names where an
`abs_dir_path` requires one. The resulting diagnostic is:

```text
error: invalid abs_dir_path value: multiple names in variable config.install.root
```

So the slightly odd-looking quoting belongs to the interface between the shell
and build2. It isn't decoration around a path that happens to contain spaces.

### What gets installed

An installation contains fastfiles only.

The installation root here is the game directory. It isn't a package prefix
owned by this project. Copying `README.md`, the licence, or the package manifest
there would leave project material beside game files with no consumer for it.

For this reason those files remain part of the source distribution and are not
installation targets.

## Configuration

| Variable                             | Default                 | Meaning                                           |
| ------------------------------------ | ----------------------- | ------------------------------------------------- |
| `config.assets.linker`               | found on `PATH`         | Linker used to build fastfiles                    |
| `config.assets.unlinker`             | found beside the Linker | Unlinker used by `b test`                         |
| `config.assets.languages`            | all four shipped       | language groups selected for building             |
| `config.assets.menu_permissive`      | `false`                 | permit unrecognised menu script commands          |
| `config.assets.menu_no_optimization` | `false`                 | preserve parsed menus closer to their source form |

Most configurations only need an install root and, when necessary, an explicit
Linker path.

The remaining variables change what gets built or how the Linker parses a
particular class of source. They are configuration variables so a build
directory records those choices and keeps applying them on later invocations.

## Layout

The source tree follows the locations the Linker already knows how to search:

```text
zone_source/<project>.zone     zone definitions, one per fastfile

zone_raw/<project>/            assets belonging to one project

raw/                           assets shared by every project

lang/<language>/               per-language overlay
                               see doc/localization.md

source_data/                   GDT files

zone/buildfile                 declares the fastfiles and their groups

templates/fastfile/            skeleton for a new fastfile project
```

There is no extra mapping layer between these directories and the Linker.

For example, placing project assets under:

```text
zone_raw/my_project/
```

puts them on the Linker's normal project search path when building the
corresponding zone. Keeping our source layout identical to that model makes it
possible to inspect an asset path and reason about where the Linker will look
without translating it through another project-specific convention.

The same idea applies to shared assets under `raw/`. A project can refer to an
asset supplied there using the naming rules the Linker already implements.

Language overlays need some extra handling and are described in
[doc/localization.md](doc/localization.md).

## Groups

Every produced fastfile belongs to a group.

The installed path has the form:

```text
zone/iw4x/x64/<group>/
```

The group is part of how IW4x searches for zones at runtime, so this isn't just
an installation convenience. Choosing the group determines the location from
which the engine can discover the fastfile.

`zone/buildfile` is the source of that assignment. A typical declaration looks
like this:

```build2
localized   = ui_mp common_mp    # Built once per configured language.
patch       = mp_foo             # Built once into patch/.
dlc         =                    # Built once into dlc/.
zonebuilder = example            # Built once into zonebuilder/.
```

A normal group corresponds directly to one installation directory. So:

```build2
patch = mp_foo
```

produces one `mp_foo.ff` and installs it under:

```text
zone/iw4x/x64/patch/
```

The `localized` group is the interesting case.

A localized fastfile is produced once for every selected language from
`config.assets.languages`. By default that is every language the retail game
ships: English, French, Italian and Spanish. Naming fewer builds less. With:

```build2
config.assets.languages=english french
```

a localized zone has an English instance under:

```text
zone/iw4x/x64/patch/english/
```

and a French instance under:

```text
zone/iw4x/x64/patch/french/
```

Each instance is still the same logical fastfile target from the project's
point of view. Its source view changes with the language overlay used for that
build.

### Why every language still exists in the build graph

There is a slightly non-obvious detail here.

The complete set of languages is a property of the project. The configured
selection decides which members of that set participate in the current build.

It is tempting to construct targets only for the languages named in
`config.assets.languages`. Doing that makes the shape of the project depend on
the local configuration. Commands concerned with the source package would then
see a different graph on a machine configured for English from one configured
for French.

In particular, `dist` must describe the source project itself. Its result
cannot depend on which language somebody happened to enable in the build
directory used to prepare the distribution.

So the language targets exist independently of that selection. Their
`include` prerequisite variable decides which ones participate in an ordinary
build.

This keeps configuration responsible for selection without making it redefine
the project.

## Starting a project

There is a template under `templates/fastfile/` for creating another fastfile
project.

Start by copying it:

```sh
cp -r templates/fastfile zone_raw/my_project
```

Then rename its zone definition:

```sh
mv zone_raw/my_project/zone_source/{TEMPLATE,my_project}.zone
```

Finally add `my_project` to the appropriate group in `zone/buildfile`.

At that point the project has the directory structure expected by the Linker
and a zone definition whose file name matches the build target.

Each directory in the template contains a `README.md`.

Those files are intentionally close to the empty directories they describe.
Asset naming in OAT is not completely uniform. For one asset type the
directory forms part of the asset name. For another the Linker supplies that
portion from the asset type itself. Looking at a plausible filesystem path is
then not always enough to infer the correct line for the zone definition.

The local README records the convention at the place where it matters, so
someone adding the first asset to an otherwise empty directory does not have to
recover that rule from an existing zone or from Linker source.

The README has a second, mundane job: Git does not track empty directories.
Keeping the file in the template means the complete skeleton survives a clone
even before any real assets have been added.

Once a copied project no longer needs those descriptions they may be removed
from that copy. The template keeps them.

## Dependency tracking

There is no dependency file emitted by the Linker.

This matters since a zone definition is not the complete set of filesystem
inputs used to produce a fastfile. The definition names assets and the Linker
then searches its source directories to resolve them. Some of those assets can
refer to further source material internally.

With a C or C++ compilation we can let the compiler discover headers and record
the result in the build database. There is no corresponding output from the
Linker that says, in effect, "this invocation read these files".

So the build describes conservative dependency roots instead.

For a project-local asset, that root is the project's tree under
`zone_raw/<project>/`. A modification there makes the project fastfile a
candidate for rebuilding.

Shared assets live under `raw/`. Since any zone may resolve an asset there, a
change in that tree can invalidate every fastfile that searches it.

A localized build gets the selected language overlay as another dependency
root. Changing translated source then rebuilds the language instance that sees
that overlay.

GDT source is treated the same way through `source_data/`.

This deliberately over-approximates the dependency relation. A file changed
under `raw/` may cause a zone to rebuild even when that particular zone never
reads it.

For this build that is the safe approximation. Missing a real dependency can
leave an old fastfile in place after its input changed. Recording a dependency
that turns out not to be used costs another Linker invocation.

We could try to recover a narrower graph by parsing zone definitions in the
buildfile and reproducing enough of the Linker's asset lookup rules to infer
what it might read. That would create a second implementation of those rules.
Each unsupported asset form would then become a chance to keep a stale
fastfile.

So the build tracks the directories that define the Linker's input view and
lets the Linker remain the authority on the contents of a zone.

If OAT eventually exposes complete dependency information, this is the part of
the build that can become more precise without changing how projects are laid
out.

## Documentation

[doc/localization.md](doc/localization.md) describes how a language-specific
fastfile is assembled and why the language overlay has its current layout.

[templates/fastfile/README.md](templates/fastfile/README.md) describes the
per-project skeleton in more detail, including how asset names map onto paths
under `zone_raw/`.
