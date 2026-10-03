# Heatmaps

A heatmap tells the bots where the fights are on a map. It is built from
recordings of real matches: where players spent their time, where they
died, where the killers stood, and where an enemy was when somebody first
saw it. A bot uses it the way a player who knows the map does. Its eyes go
now and then to where enemies usually show up, and when it hunts it
leans toward where the fights usually are. A map without a heatmap plays
just as it did before, so a missing file is never an error.

The format and the way the client uses it are described in IW4x's
`libiw4x/libiw4x/bot/heatmap.hxx`. This document covers the part that
lives here: which files we ship, where they are installed, and how they
are produced.

## Files

There are two kinds of file, both in `heatmaps/`:

```
<map>-<gametype>.iw4heat     one map in one mode, say mp_rust-war.iw4heat
<map>.iw4heat                one map in every mode, say mp_rust.iw4heat
```

Where the fights are depends on what is fought over. Search and Destroy
gathers around the bomb sites, while Team Deathmatch spreads over the
whole map. So the client prefers the mode's own heatmap. The one covering
every mode stands in for a mode that has none, which is how a mode with
too few recordings of its own still gets something reasonable. When a
mode has too few matches to say anything, it is better to leave its file
out than to ship a noisy one.

Each file is a few tens of kilobytes.

## Installation

The files are installed as they are into:

```
main/iw4x/x64/heatmaps/
```

That is the directory where IW4x keeps its other loose files. Unlike
everything else here, a heatmap is not put into a fastfile. The client
reads it directly from disk when a map loads, and it never goes through
the engine's asset database, so a zone would add nothing.

The client looks in the player's own `players/heatmaps/` first and only
then in the installed directory. A heatmap a developer builds in the game
with `bot_heatmap build` therefore takes precedence over the one we ship,
which is what one wants while working on one.

## Producing them

The heatmaps are built from the recordings that hosts' games upload to
the IW4x platform. Recordings made by a development build, which keeps
everything in a `local/` directory on the developer's machine, are never
uploaded, and the tool below leaves out any it is given from such a
directory.

The tool is `recording-heatmap`, a probe in IW4x's client package. From a
configured IW4x build:

```
b libiw4x/probe/exe{recording-heatmap}
```

The client compresses a recording with zstd before uploading it, so the
platform holds `.iw4rec.zst` files. Decompress them first:

```
zstd -d --output-dir-flat recordings/ uploads/*.iw4rec.zst
```

Leave out the recordings of a developer's own host. They are uploaded like
anybody's, but they are test sessions rather than play. Then give the tool
the options we ship with, an output directory and the recordings:

```
recording-heatmap --humans --min-minutes 30 out/ recordings/*.iw4rec
```

`--humans` folds in only the humans' play. A hosted match is mostly bots,
often ten of them to one human, so a heatmap of everybody's play would
mostly record the bots' own habits, and bots leaning on it would only
play more of them. What a bot should learn from a heatmap is where human
players go, die, kill and show up.

`--min-minutes` leaves out a heatmap of fewer minutes of matches than
that. The mode then falls back to the map's heatmap of every mode, or the
map has none at all. Half an hour of matches is a judgment call. Even
with every match of a map, the humans' play is noisy: split the humans'
matches of a map in two, and the halves disagree almost as much as the
humans and the bots do. A heatmap of much less play says little more than
which matches happened to be recorded.

For every map it writes the heatmap of each mode it saw and the one of
every mode, together with a picture of each layer seen from above
(`<name>-<layer>.ppm`). The pictures are for review and are not shipped.
Look at them before committing anything: a heatmap that puts the fights
somewhere nobody plays usually means a recording that does not belong
(a bots-only match, say, or a custom game).

Copy the `.iw4heat` files into `heatmaps/` and commit them. The next
release then carries them, and nothing else needs to change. To retire a
heatmap, delete its file.

Note that the client reads only format versions it knows about. A
heatmap written by a newer tool than the IW4x release it ships with is
refused with a line in the log, and its map plays as if it had none. So
build them with the tool from the release they are meant for.

## The current set

The heatmaps checked in were built from the 214 recordings uploaded up to
30 September 2026, less the 30 of a developer's host: 184 matches by 27 hosts,
almost all Team Deathmatch with one human and ten or eleven bots. With the
options above that gives sixteen maps a heatmap of every mode, thirteen of
them a Team Deathmatch one, and mp_highrise a Free-for-All one as well.
mp_complex and mp_crash had under ten minutes each and have none.
