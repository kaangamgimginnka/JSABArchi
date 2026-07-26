from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Entrance, Region, ItemClassification, Location, LocationProgressType

from rule_builder.rules import Has, Rule
from rule_builder.field_resolvers import FromOption
from .options import VictoryKeysReq

from .rules import EXTRAS_BP_REQS

from .items import JSABItem

if TYPE_CHECKING:
	from .__init__ import JSABWorld

LOCATION_NAME_TO_ID = {
	"Corrupted": 1,
	"Chronos": 2,
	"Milky Ways": 3,
	"Logic Gatekeeper": 4,
	"Long Live The New Fresh": 5,
	"New Game": 6,
	"The Art of War": 7,
	"Termination Shock": 8,
	"Sevcon": 9,
	"Cascade": 10,
	"Barracuda": 11,
	"Dubwoofer Substep": 12,
	"Cheat Codes": 13,
	"Clash": 14,
	"Lycanthropy": 15,
	"Cool Friends": 16,
	"The Lunar Whale": 17,
	"Spectra": 18,
	"Unlocked": 19,
	"Close To Me": 20,
	"Into The Zone": 21,
	"Vindicate Me": 22,
	"Try This": 23,
	"Final Boss": 24,
	"Annihilate (Original Mix)": 25,
	"Airborne Robots": 26,
	"Interlaced": 27,
	"Last Tile": 28,
	"Born Survivor": 29,
	"Spider Dance": 30,
	"Legacy": 31,
	"Wicked": 32,
	"First Crush": 33,
	"Yokuman Stage": 34,
	"Paper Dolls": 35,
	"Commando Steve": 36,
	"Houston": 37,
	"HYPE": 38,
	"Tokyo Skies": 39,
	"Dance Of The Incognizant": 40,
	"FOX": 41,
	"Core": 42,
	"Crystal Tokyo": 43,
	"On The Run": 44,
	"Mortal Kombat": 45,
	"Creatures ov Deception": 46,
	"Deadlocked": 47,
	"Granite": 48,
	"Lightspeed": 49,
	"Katana Blaster": 50,
	"Strike The Earth!": 51,
	"Flowers of Antimony": 52,
	"La Danse Macabre": 53,
	"In The Halls of The Usurper": 54
}

locationnames = LOCATION_NAME_TO_ID.copy()

currentmax = max(LOCATION_NAME_TO_ID.values())

for i, locname in enumerate(locationnames):
	if locname != "Corrupted":
		LOCATION_NAME_TO_ID[f"{locname} [Hardcore]"] = currentmax + i + 1

currentmax = max(LOCATION_NAME_TO_ID.values())

for i in range(1, 1001):
	LOCATION_NAME_TO_ID[f"Challenge Run Song {i}"] = currentmax + i

currentmax = max(LOCATION_NAME_TO_ID.values())

for i in range(1, 501):
	LOCATION_NAME_TO_ID[f"Challenge Run Boss Song {i}"] = currentmax + i

class JSABLocation(Location):
	game = "Just Shapes and Beats"

def get_location_names_with_ids(location_names: list[str]) -> dict[str, int | None]:
    return {location_name: LOCATION_NAME_TO_ID[location_name] for location_name in location_names}

def create_and_connect_regions(world: JASBWorld) -> None:
    create_all_regions(world)
    connect_regions(world)

def create_all_regions(world: JSABWorld) -> None:
	menu = Region("Menu", world.player, world.multiworld)
	playlist_tutorial = Region("Tutorial", world.player, world.multiworld)
	# we dont need to make a separate region for "Paradise", the only song in it will be bundled into "Tutorial"
	playlist_island = Region("Island", world.player, world.multiworld)
	playlist_volcano = Region("Volcano", world.player, world.multiworld)
	playlist_industry = Region("Industry", world.player, world.multiworld)
	playlist_tower = Region("Tower", world.player, world.multiworld)
	playlist_lostch = Region("Lost Chapter", world.player, world.multiworld)
	challenge_run = Region("Challenge Run", world.player, world.multiworld)
	final_level = Region("Final Level", world.player, world.multiworld)

	regions = [menu, playlist_tutorial, playlist_island, playlist_volcano, playlist_industry, playlist_tower, playlist_lostch, challenge_run, final_level]

	if world.options.playlist_extras_enabled:
		playlist_extras = Region("Extras", world.player, world.multiworld)
		# shovel knight sonsg are counted alongside extras
		regions.append(playlist_extras)

	world.multiworld.regions += regions

def connect_regions(world: JSABWorld) -> None:
	menu = world.get_region("Menu")
	playlist_tutorial = world.get_region("Tutorial")
	playlist_island = world.get_region("Island")
	playlist_volcano = world.get_region("Volcano")
	playlist_industry = world.get_region("Industry")
	playlist_tower = world.get_region("Tower")
	playlist_lostch = world.get_region("Lost Chapter")
	challenge_run = world.get_region("Challenge Run")
	final_level = world.get_region("Final Level")

	menu.connect(playlist_tutorial, "Playlist Tutorial Section")
	menu.connect(playlist_island, "Playlist Island Section")
	menu.connect(playlist_volcano, "Playlist Volcano Section")
	menu.connect(playlist_industry, "Playlist Industry Section")
	menu.connect(playlist_tower, "Playlist Tower Section")
	menu.connect(playlist_lostch, "Playlist Lost Chapter Section")
	menu.connect(challenge_run, "Challenge Run Section")
	menu.connect(final_level, "Final Level Section")

	if world.options.playlist_extras_enabled:
		playlist_extras = world.get_region("Extras")
		menu.connect(playlist_extras, "Playlist Extras Section")

def get_location_names_with_ids(location_names: list[str]) -> dict[str, int | None]:
    return {location_name: LOCATION_NAME_TO_ID[location_name] for location_name in location_names}

def with_hardcore(actually_tho: bool, location_names: list[str]) -> list[str]:
	if not actually_tho:
		return location_names

	new_locs = location_names.copy()

	for i in location_names:
		for ii in LOCATION_NAME_TO_ID.keys():
			if ii.startswith(i) and ii.endswith("[Hardcore]"):
				print(f"Found hardcore version of {i} ({ii})")
				new_locs.append(ii)

	return new_locs

def create_locations(world: JSABWorld) -> None:
	menu = world.get_region("Menu")
	playlist_tutorial = world.get_region("Tutorial")
	playlist_island = world.get_region("Island")
	playlist_volcano = world.get_region("Volcano")
	playlist_industry = world.get_region("Industry")
	playlist_tower = world.get_region("Tower")
	playlist_lostch = world.get_region("Lost Chapter")
	challenge_run = world.get_region("Challenge Run")
	final_level = world.get_region("Final Level")

	tutorial_locs = get_location_names_with_ids(
		with_hardcore(world.options.hardcore_mode, ["Corrupted", "Chronos", "Milky Ways", "Logic Gatekeeper", "Long Live The New Fresh", "New Game"])
	)
	island_locs = get_location_names_with_ids(
		with_hardcore(world.options.hardcore_mode, ["The Art of War", "Termination Shock", "Sevcon", "Cascade", "Barracuda"])
	)
	volcano_locs = get_location_names_with_ids(
		with_hardcore(world.options.hardcore_mode, ["Dubwoofer Substep", "Cheat Codes", "Clash", "Lycanthropy"])
	)
	industry_locs = get_location_names_with_ids(
		with_hardcore(world.options.hardcore_mode, ["Cool Friends", "The Lunar Whale", "Spectra", "Unlocked", "Close To Me"])
	)
	tower_locs = get_location_names_with_ids(
		with_hardcore(world.options.hardcore_mode, ["Into The Zone", "Vindicate Me", "Try This", "Final Boss", "Annihilate (Original Mix)"])
	)
	lostch_locs = get_location_names_with_ids(
		with_hardcore(world.options.hardcore_mode, ["Airborne Robots", "Interlaced", "Last Tile", "Born Survivor", "Spider Dance"])
	)
	extras_locs = get_location_names_with_ids(
		with_hardcore(world.options.hardcore_mode, ["Legacy", "Wicked", "First Crush", "Yokuman Stage", "Paper Dolls",
		"Commando Steve", "Houston", "HYPE", "Tokyo Skies", "Dance Of The Incognizant",
		"FOX", "Core", "Crystal Tokyo", "On The Run", "Mortal Kombat", "Creatures ov Deception",
		"Deadlocked", "Granite", "Lightspeed", "Katana Blaster", "Strike The Earth!",
		"Flowers of Antimony", "La Danse Macabre", "In The Halls of The Usurper"])
	)
	challenge_run_locs = get_location_names_with_ids([f"Challenge Run Song {i}" for i in range(1, world.options.challenge_regular_tickets + 1)])
	challenge_run_boss_locs = get_location_names_with_ids([f"Challenge Run Boss Song {i}" for i in range(1, world.options.challenge_boss_tickets + 1)])

	playlist_tutorial.add_locations(tutorial_locs)
	playlist_island.add_locations(island_locs)
	playlist_volcano.add_locations(volcano_locs)
	playlist_industry.add_locations(industry_locs)
	playlist_tower.add_locations(tower_locs)
	playlist_lostch.add_locations(lostch_locs)
	if world.options.playlist_extras_enabled:
		playlist_extras = world.get_region("Extras")
		playlist_extras.add_locations(extras_locs)

		for i in playlist_extras.locations:
			for ii in EXTRAS_BP_REQS.keys():
				if i.name.startswith(ii):
					if (world.options.beatpoint_amount < EXTRAS_BP_REQS[ii]):
						i.progress_type = LocationProgressType.EXCLUDED
		
	challenge_run.add_locations(challenge_run_locs)
	challenge_run.add_locations(challenge_run_boss_locs)

	final_level.add_event("Till It's Over", "It's Over... for real, really", rule=Has("Victory Key", count=FromOption(VictoryKeysReq)), location_type=JSABLocation, item_type=JSABItem)