from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Item, ItemClassification

if TYPE_CHECKING:
    from .__init__ import JSABWorld

ITEM_NAME_TO_ID = {
	"Tutorial Key": 1,
	"Island Key": 2,
	"Volcano Key": 3,
	"Industry Key": 4,
	"Tower Key": 5,
	"Lost Chapter Key": 6,
	"Extras Key": 7,
	"Challenge Run Regular Ticket": 8,
	"Challenge Run Boss Ticket": 9,
	"Max HP Up": 10,
	"Up Dash": 11,
	"Up-Right Dash": 12,
	"Right Dash": 13,
	"Down-Right Dash": 14,
	"Down Dash": 15,
	"Down-Left Dash": 16,
	"Left Dash": 17,
	"Up-Left Dash": 18,
	"Brittle Trap": 19,
	"Free Dash": 20,
	"Nothing": 22,
	"Victory Key": 23
}

DEFAULT_ITEM_CLASSIFICATIONS = {
	"Tutorial Key": ItemClassification.progression_skip_balancing,
	"Island Key": ItemClassification.progression_skip_balancing,
	"Volcano Key": ItemClassification.progression_skip_balancing,
	"Industry Key": ItemClassification.progression_skip_balancing,
	"Tower Key": ItemClassification.progression_skip_balancing,
	"Lost Chapter Key": ItemClassification.progression_skip_balancing,
	"Extras Key": ItemClassification.progression_skip_balancing,
	"Challenge Run Regular Ticket": ItemClassification.progression,
	"Challenge Run Boss Ticket": ItemClassification.progression,
	"Max HP Up": ItemClassification.progression | ItemClassification.useful,
	"Up Dash": ItemClassification.progression | ItemClassification.useful,
	"Up-Right Dash": ItemClassification.progression | ItemClassification.useful,
	"Right Dash": ItemClassification.progression | ItemClassification.useful,
	"Down-Right Dash": ItemClassification.progression | ItemClassification.useful,
	"Down Dash": ItemClassification.progression | ItemClassification.useful,
	"Down-Left Dash": ItemClassification.progression | ItemClassification.useful,
	"Left Dash": ItemClassification.progression | ItemClassification.useful,
	"Up-Left Dash": ItemClassification.progression | ItemClassification.useful,
	"Brittle Trap": ItemClassification.trap,
	"Free Dash": ItemClassification.useful,
	"Nothing": ItemClassification.filler,
	"Victory Key": ItemClassification.progression
}

class JSABItem(Item):
	game = "Just Shapes and Beats"

def get_random_filler_item_name(world: JSABWorld) -> str:
	if world.random.randint(0, 99) < world.options.trap_chance:
		return "Brittle Trap"
	return "Nothing"

def create_all_items(world: JSABWorld) -> None:
	itempool: list[Item] = [
		world.create_item("Tutorial Key"),
		world.create_item("Island Key"),
		world.create_item("Volcano Key"),
		world.create_item("Industry Key"),
		world.create_item("Tower Key"),
		world.create_item("Lost Chapter Key"),
	]

	tut_key = itempool[0]

	if world.options.max_hp_count > 0:
		for i in range(0, world.options.max_hp_count):
			itempool.append(world.create_item("Max HP Up"))

	if world.options.free_dash_count > 0 and world.options.rando_dash_dir:
		for i in range(0, world.options.free_dash_count):
			itempool.append(world.create_item("Free Dash"))
		
	if world.options.playlist_extras_enabled:
		itempool.append(world.create_item("Extras Key"))

	if world.options.rando_dash_dir:
		itempool.append(world.create_item("Up Dash"))
		itempool.append(world.create_item("Right Dash"))
		itempool.append(world.create_item("Down Dash"))
		itempool.append(world.create_item("Left Dash"))

		if world.options.rando_dash_count == 1:
			itempool.append(world.create_item("Up-Right Dash"))
			itempool.append(world.create_item("Down-Right Dash"))
			itempool.append(world.create_item("Down-Left Dash"))
			itempool.append(world.create_item("Up-Left Dash"))

	if world.options.challenge_regular_tickets > 0:
		for i in range(0, world.options.challenge_regular_tickets):
			itempool.append(world.create_item("Challenge Run Regular Ticket"))

	if world.options.challenge_boss_tickets > 0:
		for i in range(0, world.options.challenge_boss_tickets):
			itempool.append(world.create_item("Challenge Run Boss Ticket"))

	for i in range(0, world.options.victory_key_requirement):
		itempool.append(world.create_item("Victory Key"))

	num_of_items = len(itempool)
	unfilled_num_of_locs = len(world.multiworld.get_unfilled_locations(world.player))
	num_of_filler_needed = unfilled_num_of_locs - num_of_items

	itempool += [world.create_filler() for _ in range(num_of_filler_needed)]

	world.multiworld.itempool += itempool

	world.push_precollected(tut_key)

	if world.options.rando_dash_dir:
		starting_dash_item = world.random.choice(["Up Dash", "Right Dash", "Down Dash", "Left Dash"])
		for item in itempool:
			if (item.name == starting_dash_item):
				world.push_precollected(item)

