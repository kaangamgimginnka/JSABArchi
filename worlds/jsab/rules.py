from __future__ import annotations

from typing import TYPE_CHECKING

from rule_builder.options import OptionFilter
from rule_builder.rules import Has, HasAll, HasAny, True_, Rule
from rule_builder.field_resolvers import FromOption
from rule_builder.options import OptionFilter

EXTRAS_BP_REQS = {
	"Hype": 1000,
	"Tokyo Skies": 2000,
	"Dance of the Incognizant": 2500,
	"Fox": 5000,
	"Core": 7500,
	"Crystal Tokyo": 10000,
	"On The Run": 12500,
	"Mortal Kombat": 15000,
	"Katana Blaster": 17500,
	"Strike The Earth!": 1200,
	"Flowers of Antimony": 1400,
	"La Danse Macabre": 1600,
	"In The Halls of The Usurper": 1800
}

from .options import HardcoreMode, ChallengeSongRegularTickets, ChallengeSongBossTickets, StartingMaxHP, MaxHPItemCount, RandomizeDashDirections, DashDirectionCount, PlaylistEnableExtras, AmountOfBeatpoints, VictoryKeysReq

if TYPE_CHECKING:
	from .__init__ import JSABWorld

def set_all_rules(world: JSABWorld) -> None:
	set_all_entrance_rules(world)
	set_all_location_rules(world)
	set_completion_condition(world)

def set_all_entrance_rules(world: JSABWorld) -> None:
	sect_tutorial = world.get_entrance("Playlist Tutorial Section")
	sect_island = world.get_entrance("Playlist Island Section")
	sect_volcano = world.get_entrance("Playlist Volcano Section")
	sect_industry = world.get_entrance("Playlist Industry Section")
	sect_tower = world.get_entrance("Playlist Tower Section")
	sect_lostch = world.get_entrance("Playlist Lost Chapter Section")
	sect_finallvl = world.get_entrance("Final Level Section")

	world.set_rule(sect_finallvl, Has("Victory Key", count=FromOption(VictoryKeysReq)))
	world.set_rule(sect_tutorial, Has("Tutorial Key"))
	world.set_rule(sect_island, Has("Island Key"))
	world.set_rule(sect_volcano, Has("Volcano Key"))
	world.set_rule(sect_industry, Has("Industry Key"))
	world.set_rule(sect_tower, Has("Tower Key"))
	world.set_rule(sect_lostch, Has("Lost Chapter Key"))

	if world.options.playlist_extras_enabled:
		sect_extras = world.get_entrance("Playlist Extras Section")
		world.set_rule(sect_extras, Has("Extras Key"))

def has_enough_hp(req_hp: int, world: JSABWorld) -> Rule:
	startinghp = world.options.starting_max_hp.value
	if startinghp >= req_hp:
		return True_()
	return Has("Max HP Up", count=(req_hp - startinghp))

def hard_clear(normal: int, hard: int, world: JSABWorld) -> int:
	if world.options.hard_locs:
		return hard
	return normal

def set_all_location_rules(world: JSABWorld) -> None:
	if world.options.rando_dash_dir:
		# todo: add "has_x_dash_hard" (without the hard check)
		# todo: add option filter that makes these false when on hard locs

		has_up_dash = Has("Up Dash")
		has_upright_dash = Has("Up-Right Dash")
		has_right_dash = Has("Right Dash")
		has_downright_dash = Has("Down-Right Dash")
		has_down_dash = Has("Down Dash")
		has_downleft_dash = Has("Down-Left Dash")
		has_left_dash = Has("Left Dash")
		has_upleft_dash = Has("Up-Left Dash")

		has_any_dash = HasAny("Up Dash", "Up-Right Dash", "Right Dash", "Down-Right Dash", "Down Dash", "Down-Left Dash", "Left Dash", "Up-Left Dash")

		# TODO: Implement hardcore variants

		# Tutorial
		longlivefresh = world.get_location("Long Live The New Fresh")
		# Corrupted is possibe hitless
		# Chronos is possible hitless
		world.set_rule(longlivefresh, has_enough_hp(hard_clear(4, 3, world), world) | has_any_dash)

		# Tutorial (Hardcore)
		longlivefresh_hc = world.get_location("Long Live The New Fresh")
		world.set_rule(longlivefresh_hc, has_enough_hp(5, world) | has_any_dash)

		# Island
		sevcon = world.get_location("Sevcon")
		world.set_rule(sevcon, has_enough_hp(hard_clear(2, 1, world), world) | (has_up_dash | has_down_dash))

		# Island (Hardcore)
		#if world.options.hardcore_mode:
			#sevcon_hc = world.get_location("Sevcon [Hardcore]")
			#world.set_rule(sevcon_hc, has_enough_hp(hard_clear(4, 2, world), world) | (has_up_dash | has_down_dash))

		# Extras
		if world.options.playlist_extras_enabled:
			bp_maps: dict[str, int] = {}

			for loc in world.get_locations():
				if loc in EXTRAS_BP_REQS.keys():
					bp_maps[loc] = EXTRAS_BP_REQS[loc]

			leg = world.get_location("Legacy")
			world.set_rule(leg, has_enough_hp(10, world) | (has_right_dash))
			wick = world.get_location("Wicked")
			fircr = world.get_location("First Crush")
			yokstg = world.get_location("Yokuman Stage")
			dolls = world.get_location("Paper Dolls")
			cmdstv = world.get_location("Commando Steve")
			house = world.get_location("Houston")
			hype = world.get_location("HYPE")
			tokyo = world.get_location("Tokyo Skies")
			incog = world.get_location("Dance Of The Incognizant")

	else:
		# Extras
		if world.options.playlist_extras_enabled:
			for loc in world.get_locations():
				for loci in EXTRAS_BP_REQS.keys():
					if loci.startswith(loc.name):
						actloc = world.get_location(loc)
						world.set_rule(actloc, True_(options=[OptionFilter(AmountOfBeatpoints, EXTRAS_BP_REQS[loci], operator="ge")], filtered_resolution=False))

	# Challenge Run

	for i in range(1, world.options.challenge_regular_tickets + 1):
		chall = world.get_location(f"Challenge Run Song {i}")
		world.set_rule(chall, Has("Challenge Run Regular Ticket", count=i))

	for i in range(1, world.options.challenge_boss_tickets + 1):
		chall = world.get_location(f"Challenge Run Boss Song {i}")
		world.set_rule(chall, Has("Challenge Run Boss Ticket", count=i))

def set_completion_condition(world: JSABWorld) -> None:
	world.set_completion_rule(Has("It's Over... for real, really"))
