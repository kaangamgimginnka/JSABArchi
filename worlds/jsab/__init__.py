from collections.abc import Mapping
from typing import Any

from worlds.AutoWorld import World, WebWorld

from BaseClasses import Tutorial

from . import items, locations, rules
from . import options as jsab_options

class JSABWebWorld(WebWorld):
	rich_text_options_doc = True

	setup_en = Tutorial(
		"Mod Setup and Use Guide",
		"A guide to playing Just Shapes & Beats with Archipelago",
		"English",
		"setup_en.md",
		"setup/en",
		["kaangamgimginnkagnagnkingmngknag"]
	)

	tutorials = [setup_en]
	game_info_languages = ["en"]

	bug_report_page = "lol"

class JSABWorld(World):
	"""
	Just Shapes & Beats
	"""

	game = "Just Shapes and Beats"
	options_dataclass = jsab_options.JSABOptions
	options: jsab_options.JSABOptions

	location_name_to_id = locations.LOCATION_NAME_TO_ID
	item_name_to_id = items.ITEM_NAME_TO_ID

	origin_region_name = "Menu"

	def create_regions(self) -> None:
		locations.create_and_connect_regions(self)
		locations.create_locations(self)
	
	def set_rules(self) -> None:
		rules.set_all_rules(self)

	def create_items(self) -> None:
		items.create_all_items(self)

	def create_item(self, name: str) -> items.JSABItem:
		return items.JSABItem(name, items.DEFAULT_ITEM_CLASSIFICATIONS[name], items.ITEM_NAME_TO_ID[name], self.player)

	def get_filler_item_name(self) -> str:
		return items.get_random_filler_item_name(self)

	def fill_slot_data(self) -> Mapping[str, Any]:
		return self.options.as_dict(
			"hardcore_mode", "player_shape", "starting_max_hp", "rando_dash_dir", "rando_dash_count"
		)