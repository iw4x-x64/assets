// The objective publisher for the bots.
//
// The flags, bomb sites, bomb, radios and carriers of a game type are
// script state: fields the gametype scripts keep on level and on their
// objective structs. The bots' reasoning lives in C++, and this is how it
// learns what the objectives are doing: every tenth of a second the thread
// below reads the fields the current gametype keeps and hands them over
// through three builtins the client registers (bots_begin, bots_objective,
// bots_end). It publishes data, not decisions: a bot still captures a flag
// by standing in its trigger and plants a bomb by holding use, and the
// gametype decides whether that succeeds.
//
// The same thread watches every player's grenades and reports a smoke's
// detonation through a fourth builtin (bots_smoke): the cloud is a client
// effect the engine keeps no volume for, and the grenade's own "explode"
// notify is the one place its position is told.
//
// Every read is guarded with isDefined, because a gametype that has not
// created an objective yet (or a custom one that names things differently)
// must cost a missing objective, not a script error. Every field read
// below is one the stock script of that gametype (maps/mp/gametypes/*.gsc
// in common_mp.ff, dd.gsc as patch_mp.ff overrides it) sets; the function
// that sets it is named where it is read.

main()
{
	level thread bots_publisher();
}

bots_publisher()
{
	level endon( "game_ended" );

	for ( ;; )
	{
		bots_publish();
		wait 0.1;
	}
}

bots_team_number( team )
{
	if ( !isDefined( team ) )
		return 0;
	if ( team == "axis" )
		return 1;
	if ( team == "allies" )
		return 2;
	return 0;
}

// The engine's twelve gametypes (maps/mp/gametypes/_gametypes.txt), as
// bot/script.cxx numbers them.
//
bots_gametype_number()
{
	gt = level.gametype;

	if ( gt == "dom" )
		return 1;
	if ( gt == "koth" )
		return 2;
	if ( gt == "sd" )
		return 3;
	if ( gt == "sab" )
		return 4;
	if ( gt == "ctf" )
		return 5;
	if ( gt == "dm" )
		return 6;
	if ( gt == "war" )
		return 7;
	if ( gt == "dd" )
		return 8;
	if ( gt == "oneflag" )
		return 9;
	if ( gt == "gtnw" )
		return 10;
	if ( gt == "arena" )
		return 11;
	if ( gt == "vip" )
		return 12;
	return 0;
}

// Who may interact with an object, relative to its owner, as
// _gameobjects::allowUse / allowCarry set interactTeam and
// canInteractWith reads it: none, friendly (the owner's side), enemy (the
// other side), any. Undefined is how a use object is created
// (createUseObject sets "none" itself, so this is only a script that
// never called allowUse) and is read as any.
//
bots_interact_number( obj )
{
	if ( !isDefined( obj.interactTeam ) )
		return 3;
	if ( obj.interactTeam == "none" )
		return 0;
	if ( obj.interactTeam == "friendly" )
		return 1;
	if ( obj.interactTeam == "enemy" )
		return 2;
	return 3;
}

// The site's letter: sd.gsc, dd.gsc and arena.gsc keep
// _gameobjects::getLabel() on obj.label, "_a" / "_b" from the trigger's
// script_label.
//
bots_label_number( obj )
{
	if ( !isDefined( obj.label ) )
		return 0;
	if ( obj.label == "_a" )
		return 1;
	if ( obj.label == "_b" )
		return 2;
	if ( obj.label == "_c" )
		return 3;
	if ( obj.label == "_d" )
		return 4;
	return 0;
}

bots_entity_number( ent )
{
	if ( !isDefined( ent ) )
		return -1;
	return ent getEntityNumber();
}

bots_progress( obj )
{
	if ( !isDefined( obj.curProgress ) || !isDefined( obj.useTime ) || obj.useTime <= 0 )
		return 0;
	return obj.curProgress / obj.useTime;
}

// A use object as the gametypes build them (_gameobjects::createUseObject):
// its trigger, owner, the team working on it and how far along they are.
// Whether the use key has to be held is the trigger's kind (triggerType,
// "use" for a trigger_use_touch, "proximity" for a trigger_radius). The
// trailing arguments are what only some modes have: a destroyed site, the
// one player who alone may use it, and each side's meter.
//
bots_publish_use_object( kind, obj, origin, planted, trigger, destroyed, soleUser, meterAxis, meterAllies )
{
	if ( !isDefined( obj ) )
		return;

	// The entity the use key has to find: the object's trigger, or the one
	// the caller names for a use object it cannot reach (the planted bomb's
	// defuse trigger).
	//
	ent = -1;
	if ( isDefined( trigger ) )
		ent = trigger getEntityNumber();
	else if ( isDefined( obj.trigger ) )
		ent = obj.trigger getEntityNumber();

	if ( !isDefined( origin ) )
	{
		if ( isDefined( obj.curOrigin ) )
			origin = obj.curOrigin;
		else if ( isDefined( obj.trigger ) )
			origin = obj.trigger.origin;
		else
			return;
	}

	owner = 0;
	if ( isDefined( obj.ownerTeam ) )
		owner = bots_team_number( obj.ownerTeam );

	claimant = 0;
	if ( isDefined( obj.claimTeam ) )
		claimant = bots_team_number( obj.claimTeam );

	use = isDefined( obj.triggerType ) && obj.triggerType == "use";

	if ( !isDefined( destroyed ) )
		destroyed = false;
	if ( !isDefined( soleUser ) )
		soleUser = -1;
	if ( !isDefined( meterAxis ) )
		meterAxis = 0;
	if ( !isDefined( meterAllies ) )
		meterAllies = 0;

	bots_objective( kind, ent, origin, owner, claimant, bots_progress( obj ), bots_interact_number( obj ), -1, planted, use, destroyed, bots_label_number( obj ), soleUser, meterAxis, meterAllies );
}

// A carry object (_gameobjects::createCarryObject): where it is and who
// holds it. The progress field carries whether it is away from home, and
// who may pick it up is allowCarry's word (sd: the attackers; sab: anyone,
// nobody once planted; ctf: the other side, anyone once dropped).
//
bots_publish_carry_object( obj, owner )
{
	if ( !isDefined( obj ) || !isDefined( obj.curOrigin ) )
		return;

	ent = -1;
	if ( isDefined( obj.trigger ) )
		ent = obj.trigger getEntityNumber();
	else if ( isDefined( obj.visuals ) && obj.visuals.size > 0 )
		ent = obj.visuals[ 0 ] getEntityNumber();

	if ( !isDefined( owner ) )
	{
		owner = 0;
		if ( isDefined( obj.ownerTeam ) )
			owner = bots_team_number( obj.ownerTeam );
	}

	away = 0;
	if ( !( obj maps\mp\gametypes\_gameobjects::isHome() ) )
		away = 1;

	bots_objective( 3, ent, obj.curOrigin, owner, 0, away, bots_interact_number( obj ), bots_entity_number( obj.carrier ), false, false, false, 0, -1, 0, 0 );
}

// A site is out of the round when the gametype disableObject()'d it:
// _gameobjects::disableObject runs common_scripts\utility::trigger_off on
// its trigger, which sets trigger.trigger_off (trigger_on clears it).
//
bots_site_destroyed( site )
{
	return isDefined( site.trigger ) && isDefined( site.trigger.trigger_off ) && site.trigger.trigger_off;
}

// The bomb sites and the bomb of Search and Destroy and Sabotage. Both
// keep the sites on level.bombZones (sd.gsc bombs(): indexed, owned by
// the defenders; sab.gsc onSpawn(): keyed by the team whose site it is,
// createBombZone(team, ...) making that team the owner).
//
// Where the planted bomb is differs. sd.gsc bombPlanted() keeps the
// defuse object in a local, out of reach, but puts the planted bomb's
// model on level.sdBombModel and moves the site's bombDefuseTrig onto it,
// so the site nearest the model is the planted one and the model's origin
// is where use is held (at the moved trigger). sab.gsc onUse() has no
// model and no defuse object: the site itself is flipped to
// allowUse("friendly") by setUpForDefusing() (resetBombsite() puts
// "enemy" back after a defuse), so the site whose interactTeam is
// "friendly" is the planted one, its own trigger is what use finds, and
// level.sabBomb.curOrigin (the bomb is setDropped() at the planter) is
// where to stand.
//
bots_publish_bombs( gt, planted )
{
	plantedAt = undefined;
	if ( gt == "sd" && planted && isDefined( level.sdBombModel ) )
		plantedAt = level.sdBombModel.origin;

	if ( isDefined( level.bombZones ) )
	{
		keys = getArrayKeys( level.bombZones );
		for ( i = 0; i < keys.size; i++ )
		{
			site = level.bombZones[ keys[ i ] ];
			if ( !isDefined( site ) || !isDefined( site.curOrigin ) )
				continue;

			destroyed = bots_site_destroyed( site );

			if ( gt == "sd" )
			{
				if ( isDefined( plantedAt ) && distanceSquared( plantedAt, site.curOrigin ) < 512 * 512 )
					bots_publish_use_object( 2, site, plantedAt, true, site.bombDefuseTrig, destroyed );
				else
					bots_publish_use_object( 2, site, site.curOrigin, false, undefined, destroyed );
			}
			else
			{
				isPlanted = planted && isDefined( site.interactTeam ) && site.interactTeam == "friendly";

				origin = site.curOrigin;
				if ( isPlanted && isDefined( level.sabBomb ) && isDefined( level.sabBomb.curOrigin ) )
					origin = level.sabBomb.curOrigin;

				bots_publish_use_object( 2, site, origin, isPlanted, undefined, destroyed );
			}
		}
	}

	// sd.gsc bombs(): level.sdBomb, owned by the attackers, only without
	// scr_sd_multibomb (level.multiBomb: everyone plants bare-handed, and
	// there is no bomb to publish). sab.gsc onSpawn(): level.sabBomb,
	// neutral until picked up (onPickup sets the owner, abandonmentThink
	// puts neutral back).
	//
	if ( gt == "sd" && isDefined( level.sdBomb ) )
		bots_publish_carry_object( level.sdBomb, undefined );
	if ( gt == "sab" && isDefined( level.sabBomb ) )
		bots_publish_carry_object( level.sabBomb, undefined );
}

// Demolition's two sites: dd.gsc bombs() keeps them on level.bombZones,
// owned by the defenders, keyObject level.ddBomb which nothing defines,
// so every attacker plants bare-handed. Each site keeps its own state,
// and only that is read: level.bombPlanted is set by bombPlanted() and
// never cleared, level.bombExploded counts the sites destroyed.
//
// - site.bombPlanted: true from bombPlanted(), 0 from bombHandler() on
//   the explosion or the defuse.
// - The planted bomb's model: dropBombModel() spawns it at the planter's
//   feet, inside the site's use volume, on level.ddBombModel[site.label];
//   bombHandler("explode") deletes it. That is where use is held: the
//   defuse is the site's own trigger, flipped to allowUse("friendly") by
//   setUpForDefusing() (the site's bombDefuseTrig is created and moved
//   away and never used).
// - Destroyed: bombHandler("explode") disableObject()s the site, for the
//   rest of the round.
//
bots_publish_demolition()
{
	if ( !isDefined( level.bombZones ) )
		return;

	for ( i = 0; i < level.bombZones.size; i++ )
	{
		site = level.bombZones[ i ];
		if ( !isDefined( site ) || !isDefined( site.curOrigin ) )
			continue;

		destroyed = bots_site_destroyed( site );
		isPlanted = !destroyed && isDefined( site.bombPlanted ) && site.bombPlanted;

		origin = site.curOrigin;
		if ( isPlanted && isDefined( site.label ) && isDefined( level.ddBombModel ) && isDefined( level.ddBombModel[ site.label ] ) )
			origin = level.ddBombModel[ site.label ].origin;

		bots_publish_use_object( 2, site, origin, isPlanted, undefined, destroyed );
	}
}

// Capture the Flag and One Flag: ctf.gsc onSpawn() keeps a flag and a
// capture zone per team on level.teamFlags and level.capZones;
// oneflag.gsc oneflag_ctf() one flag (the defenders') and one zone (the
// attackers'), under the same names. A zone's interactTeam is "friendly"
// while its side's flag is home and "none" while it is away (ctf.gsc
// onPickup() / onReset()), which is why it is read rather than assumed.
//
bots_publish_flags()
{
	if ( isDefined( level.teamFlags ) )
	{
		keys = getArrayKeys( level.teamFlags );
		for ( i = 0; i < keys.size; i++ )
			bots_publish_carry_object( level.teamFlags[ keys[ i ] ], bots_team_number( keys[ i ] ) );
	}

	if ( isDefined( level.capZones ) )
	{
		keys = getArrayKeys( level.capZones );
		for ( i = 0; i < keys.size; i++ )
			bots_publish_use_object( 4, level.capZones[ keys[ i ] ], undefined, false, undefined );
	}
}

// Global Thermonuclear War: gtnw.gsc setupNukeSite() keeps the one zone
// on level.nukeSite, neutral, allowUse("enemy"); scoreCounter() sets its
// owner every second to the side with more players touching ("none" when
// empty) and gives that side a point, and the meter toward the nuke is
// the team score, 0 to 100 (activateNuke at 100). The zone's own
// progress means nothing here (noUseBar): the meters travel with it.
//
bots_publish_nuke()
{
	if ( !isDefined( level.nukeSite ) )
		return;

	meterAxis = 0;
	meterAllies = 0;
	if ( isDefined( game[ "teamScores" ] ) )
	{
		if ( isDefined( game[ "teamScores" ][ "axis" ] ) )
			meterAxis = game[ "teamScores" ][ "axis" ] * 0.01;
		if ( isDefined( game[ "teamScores" ][ "allies" ] ) )
			meterAllies = game[ "teamScores" ][ "allies" ] * 0.01;
	}

	bots_publish_use_object( 1, level.nukeSite, undefined, false, undefined, false, -1, meterAxis, meterAllies );
}

// Arena: arena.gsc arenaFlag() runs only once a side is down to one alive
// or the time is nearly up; until then level.arenaFlag is undefined (or,
// for the length of that function, the flag_arena trigger entity), and
// after it the use object, neutral, allowUse("enemy"), marked isArena.
// Capturing it ends the round.
//
bots_publish_arena()
{
	if ( !isDefined( level.arenaFlag ) || !isDefined( level.arenaFlag.isArena ) || !level.arenaFlag.isArena )
		return;

	bots_publish_use_object( 1, level.arenaFlag, undefined, false, undefined );
}

// VIP: vip.gsc extractionZone() keeps the zone on level.extractionZone
// (the extraction_vip entity array for the length of that function, then
// the use object owned by the defenders, allowUse("friendly"), useTime
// 0); vipSelection() marks one defender player.isVip after the grace
// period, and onUse() acts for that player alone (level.extractionTime
// is defined from then, and the defenders win when it runs out). The
// zone is published as the VIP's capture point with the VIP as its one
// user and the extraction called as its progress.
//
bots_publish_vip()
{
	if ( !isDefined( level.extractionZone ) || !isDefined( level.extractionZone.trigger ) )
		return;

	vip = -1;
	if ( isDefined( level.players ) )
	{
		for ( i = 0; i < level.players.size; i++ )
		{
			player = level.players[ i ];
			if ( isDefined( player ) && isDefined( player.isVip ) && player.isVip )
				vip = player getEntityNumber();
		}
	}

	zone = level.extractionZone;

	origin = undefined;
	if ( isDefined( zone.curOrigin ) )
		origin = zone.curOrigin;
	else
		origin = zone.trigger.origin;

	progress = 0;
	if ( isDefined( level.extractionTime ) )
		progress = 1;

	use = isDefined( zone.triggerType ) && zone.triggerType == "use";

	owner = 0;
	if ( isDefined( zone.ownerTeam ) )
		owner = bots_team_number( zone.ownerTeam );

	bots_objective( 4, zone.trigger getEntityNumber(), origin, owner, 0, progress, bots_interact_number( zone ), -1, false, use, false, 0, vip, 0, 0 );
}

// How long a smoke grenade's cloud stands once the grenade goes off,
// in seconds: the life of the effect the weapon names
// (props/american_smoke_grenade_mp), which fills its spot and thins out
// toward the end. Its fuse is the second before that, which the
// "explode" notify waits through.
//
bots_smoke_seconds()
{
	return 10;
}

// Watch every player for the grenades it throws. Started once per
// player from the publish that first lists it; the mark is a player
// field, so a round restart (which clears the script variables with the
// VM) starts the watch again with the publisher.
//
bots_watch_players()
{
	if ( !isDefined( level.players ) )
		return;

	for ( i = 0; i < level.players.size; i++ )
	{
		player = level.players[ i ];
		if ( !isDefined( player ) || isDefined( player.bots_smoke_watched ) )
			continue;

		player.bots_smoke_watched = true;
		player thread bots_watch_smoke();
	}
}

// _weapons.gsc's beginGrenadeTracking() waits on the same notify: the
// engine raises "grenade_fire" on the thrower with the grenade entity
// and the weapon's name for every offhand thrown. Only the smoke is
// followed; the airdrop markers' signal smoke is no screen.
//
bots_watch_smoke()
{
	self endon( "disconnect" );

	for ( ;; )
	{
		self waittill( "grenade_fire", grenade, weaponName );

		if ( isDefined( grenade ) && isDefined( weaponName ) && weaponName == "smoke_grenade_mp" )
			grenade thread bots_watch_smoke_cloud();
	}
}

// The grenade entity's "explode" notify carries the origin (the same
// one _weapons.gsc's empExplodeWaiter() reads for the EMP grenade); a
// grenade deleted before it goes off takes this thread with it.
//
bots_watch_smoke_cloud()
{
	self waittill( "explode", position );

	bots_smoke( position, bots_smoke_seconds() );
}

bots_publish()
{
	bots_watch_players();

	playing = true;

	if ( isDefined( level.gameEnded ) && level.gameEnded )
		playing = false;
	if ( isDefined( level.inPrematchPeriod ) && level.inPrematchPeriod )
		playing = false;

	attackers = 0;
	defenders = 0;
	if ( isDefined( game[ "attackers" ] ) )
		attackers = bots_team_number( game[ "attackers" ] );
	if ( isDefined( game[ "defenders" ] ) )
		defenders = bots_team_number( game[ "defenders" ] );

	gt = level.gametype;

	// The one bomb's state, with the meaning sd.gsc and sab.gsc give the
	// flags (sab has no bombDefused: its bombPlanted is cleared instead).
	// Demolition's level.bombPlanted is never cleared and its
	// level.bombExploded is a count, so there the sites speak for
	// themselves and only whether any is ticking (level.bombsPlanted) is
	// reported.
	//
	planted = false;
	defused = false;
	exploded = false;

	if ( gt == "sd" || gt == "sab" )
	{
		planted = isDefined( level.bombPlanted ) && level.bombPlanted;
		defused = isDefined( level.bombDefused ) && level.bombDefused;
		exploded = isDefined( level.bombExploded ) && level.bombExploded;
	}
	else if ( gt == "dd" )
	{
		planted = isDefined( level.bombsPlanted ) && level.bombsPlanted > 0;
	}

	bots_begin( bots_gametype_number(), playing, attackers, defenders, planted, defused, exploded );

	if ( gt == "dom" && isDefined( level.flags ) )
	{
		// dom.gsc onSpawn(): each flag is the trigger entity, its use
		// object hung on flag.useObj.
		//
		for ( i = 0; i < level.flags.size; i++ )
		{
			flag = level.flags[ i ];
			if ( isDefined( flag.useObj ) )
				bots_publish_use_object( 1, flag.useObj, flag.origin, false, undefined );
		}
	}
	else if ( gt == "koth" )
	{
		// koth.gsc HQMainLoop(): the active radio's use object is
		// level.radioObject, undefined between radios.
		//
		if ( isDefined( level.radioObject ) )
			bots_publish_use_object( 1, level.radioObject, undefined, false, undefined );
	}
	else if ( gt == "sd" || gt == "sab" )
		bots_publish_bombs( gt, planted && !defused && !exploded );
	else if ( gt == "dd" )
		bots_publish_demolition();
	else if ( gt == "ctf" || gt == "oneflag" )
		bots_publish_flags();
	else if ( gt == "gtnw" )
		bots_publish_nuke();
	else if ( gt == "arena" )
		bots_publish_arena();
	else if ( gt == "vip" )
		bots_publish_vip();

	bots_end();
}
