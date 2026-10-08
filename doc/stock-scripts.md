# Stock scripts in iw4x_patch_mp

`zone_raw/iw4x_patch_mp/iw4x/` carries 17 of the game's own multiplayer
scripts under the `iw4x/` prefix, copied unchanged from the game data Steam
and the Microsoft store ship today (x64 zones, built 2026-09-03; the two are
byte-identical). The script compiler takes `iw4x/<name>` over the stock
`<name>` (`libiw4x/libiw4x/zone/engine/override.cxx` in the client), so
every client compiles these copies whatever game data it was installed
from.

## Why

A host migration hands the running match to another client as a save that
stores positions in the old host's compiled scripts as raw offsets. The game
refuses the save when the new host compiled different scripts, and the
match ends. Game data from before Steam's x64 update (x86 zones built
2009/2010, which the client converts on its first launch) carries older
versions of some stock scripts, so without these copies a migration between
a player on old data and one on current data always ends the match.

## The files

| script | zone it differs in | difference |
|---|---|---|
| `common_scripts/_fx.gsc` | `common_mp` | `willNeverChange ()` guarded by `level.createFX_enabled` |
| `common_scripts/utility.gsc` | `common_mp` | the `createFX_enabled` guard, a guarded `wait (timeout)` |
| `maps/mp/gametypes/_globallogic.gsc` | `common_mp` | no `camera_thirdPerson` server info |
| `maps/mp/_animatedmodels.gsc`, `maps/mp/_utility.gsc`, `gametypes/_class.gsc`, `_damage.gsc`, `_missions.gsc`, `_rank.gsc`, `dd.gsc`, `killstreaks/_airdrop.gsc`, `_helicopter.gsc`, `_killstreaks.gsc`, `perks/_perkfunctions.gsc` | `common_mp` | old data's copy is older; both data's `patch_mp` already carry the current one |
| `maps/mp/mp_afghan.gsc`, `mp_derail.gsc`, `mp_rust.gsc` | the map's zone | as above, against `patch_mp` |

The second group is shipped too so that the result does not depend on
which zone's copy the engine resolves to. Every other script of the
multiplayer zones both data sets have is the same apart from line endings
(the old data's are CRLF). The DLC maps exist only in the current data, so
their scripts cannot differ between two clients that can both load the map.

## Redoing the comparison

After an update of the game data, compare again and ship whatever differs
the same way:

1. Unlink the rawfiles of every multiplayer zone (`common_mp`, `patch_mp`,
   `*_mp`, `mp_<map>`, not `*_load`) of both data sets with OpenAssetTools'
   Unlinker: `Unlinker --game IW4MS --include-assets rawfile -o <out> <zone>.ff`
   (old data after the client has converted it).
2. Compare every `.gsc` the two have in common with line endings
   normalized.
3. Copy the current data's version of each differing script here, list it
   in `zone_source/iw4x_patch_mp.zone`, and update the table above.
