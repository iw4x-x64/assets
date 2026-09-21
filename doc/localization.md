# Localization

A fastfile contains the localized text that its assets refer to. There
is no runtime translation step after the zone has been loaded. So, for
the zones whose contents vary with language, we have to build one
fastfile per language.

This sounds simple enough until we get to the Linker. Its idea of a
language is somewhat different from what one might expect, and that ends
up determining the layout of the source tree here. In particular, seeing
French text under an `english/` directory is quite intentional.

## What the Linker does

The Linker has no language option. More interestingly, adding such an
option at the command line would not by itself change what gets loaded.
The language is already fixed further down in the zone loading path.

The IW4MS zone loader creates the zone with its language set to
`LANGUAGE_NONE`. That value is left alone for the lifetime of the load.
`LocalizeCommon::GetNameOfLanguage` maps `LANGUAGE_NONE` to `english`,
so when the localize loader goes looking for a string asset it
constructs a path of the form:

```
english/localizedstrings/<asset>.str
```

Now there is a second language decision inside the `.str` parser. A
string file may contain several values for the same reference, each
tagged with a `LANG_*` value. The parser keeps the value corresponding
to the zone language. For the zones the Linker constructs, that ends up
being `LANG_ENGLISH`.

So there are really two fixed assumptions involved here. Asset lookup
goes through `english/localizedstrings/`, and the value selected from
the resulting file is `LANG_ENGLISH`.

This has a slightly surprising consequence. Consider a file containing
the same reference in English and French:

```
REFERENCE           PLATFORM_STEAM_DISCONNECTED
LANG_ENGLISH        "Disconnected from Steam."
LANG_FRENCH         "Déconnexion de Steam."
```

Feeding that file to the Linker twice does not give us an English
fastfile and a French fastfile. Both invocations construct the same zone
language, so both select the `LANG_ENGLISH` value. The French value is
parsed, then has no part in the resulting zone.

Putting the file under `french/localizedstrings/` does not change this
either. The localize loader never constructs that path. From its point
of view the file simply does not exist.

Perhaps the easiest way to see this is to dump one of the retail
localized fastfiles. Dumping the French `code_post_gfx.ff`, for example,
gives us:

```
english/localizedstrings/code_post_gfx.str
```

and the file contains:

```
REFERENCE           PLATFORM_STEAM_DISCONNECTED
LANG_ENGLISH        "Déconnexion de Steam."
```

That looks wrong if the directory name and `LANG_ENGLISH` tag are read
as descriptions of the text. They are really part of the input
convention expected by this Linker. The French identity came from the
fastfile we dumped. Once the asset is represented as Linker input, the
text has to occupy the slot that this particular loading path actually
reads.

So keep that distinction in mind when looking at `lang/` below. The
directory called `english` describes the path presented to the Linker.
It says nothing about the natural language of the bytes in the file.

## How a language is built here

We deal with the fixed Linker language by changing its asset search tree
for each build.

For French, for example, the language-specific part of that tree
contains:

```
lang/french/english/localizedstrings/<asset>.str
```

The Linker still asks for:

```
english/localizedstrings/<asset>.str
```

It sees `lang/french/` earlier on the search path, so the French version
is the one it finds.

Now this means the `english/` component under `lang/french/` is
deliberate. We are reproducing the path the Linker asks for inside an
overlay whose outer directory identifies which build we are performing.

A language in the build system is represented by a group. Building the
`french` group means producing the complete set of localized fastfiles
with the French overlay active. They are installed under
`zone/iw4x/x64/patch/french/`, which keeps them apart from the stock
fastfiles in the retail language directories.

There is a useful property to doing this with an asset search path
instead of special-casing localized strings. The overlay is an ordinary
asset tree. It can replace any asset whose language-specific version
differs from the shared one.

For example, some retail zones use a different image for a non-English
build. Such an image can live under:

```
lang/french/
```

at the same relative path that the Linker would normally use. No extra
language machinery is needed for it. From the Linker's point of view it
found an asset earlier on its search path, which is exactly the same
thing that happened for the `.str` file.

`zone/buildfile` adds the corresponding overlay directory whenever it
builds a group. We do this for every group, including groups for which
no overlay directory exists.

That last part is intentional. The Linker accepts a search path naming a
directory that is absent. So `patch` or `dlc`, for example, can go
through the same rule without teaching the buildfile which groups
currently have language-specific files. If one of those groups gains an
overlay later, merely creating the directory is enough for the existing
build rule to start using it.

This keeps the source tree as the description of the difference. An
absent overlay means that group uses the shared asset. A present file
means that file replaces the shared one for that group.

## Which zones are localized

One tempting way to derive the language groups would be to look for
localize assets in each retail zone. That does not describe the retail
data closely enough.

There are 116 zones in a retail IW4 x64 installation. Of those, 50
contain localize assets. There are likewise 50 zones whose resulting
fastfiles differ between the shipped languages. Those sets happen to
have the same size, yet they do not contain exactly the same zones.

For example, `localized_common_mp` contains localize assets and still
produces the same bytes for all four shipped languages. `patch_mp`
behaves the same way. So the presence of a localize asset does not imply
that we need a different output fastfile.

The reverse case exists too. `so_bridge` differs between languages
without containing any localize asset. The same is true for
`so_ghillies`. So looking for localize assets would miss real
language-specific fastfiles.

There is one more wrinkle worth keeping here since it explains why the
overlay is allowed to contain arbitrary assets. Five zones change their
asset list between languages. The differing asset is an image whose name
encodes the language variant.

For `contingency` and `invasion`, the relevant choice is between:

```
image,friendorfoe_self_sp
image,friendorfoe_self_sp_french
```

`localized_common_mp` similarly uses:

```
image,killcamindicator_english
image,killcamindicator_french
```

And `localized_ui_mp` and `ui` select between:

```
image,specialty_new
image,specialty_new_nonenglish
```

So a language-specific zone is best treated as a zone built from a
language-specific asset view. Localized strings are the common case. The
retail data already contains cases where the distinction reaches another
asset type, and the overlay naturally represents those cases too.

Note that this is why we do not try to infer localization from the
`.zone` definition alone. Two languages can use the same definition and
feed different asset contents into it. They can equally end up needing a
different asset name. The reliable description is the retail result we
are reproducing, with the corresponding difference expressed in
`lang/<language>/`.

## Encoding

There is one final trap here that is independent of the Linker's
language selection.

Retail `.str` files use CP1252. They are not UTF-8.

For a character such as `é`, the retail representation contains the
single byte `0xE9`. The UTF-8 representation of the same visible
character contains a different byte sequence. An editor can display both
forms identically, which makes an accidental conversion rather easy to
miss during review.

For this reason `.gitattributes` marks `*.str` as binary. Git must
preserve these files byte for byte and leave line-ending or
text-encoding conversion out of the checkout path.

Note that this matters most after a bulk edit or after passing the files
through a tool that assumes UTF-8. A resulting `.str` can look perfectly
ordinary when opened in an editor and still contain bytes that the game
was never meant to read.

So if localized strings have been rewritten programmatically, check the
bytes before committing them. For the retail character set, characters
such as `é` should still have their CP1252 representation. The visual
appearance of the file is not enough to establish that.
