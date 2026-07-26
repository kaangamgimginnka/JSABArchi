from dataclasses import dataclass

from Options import Choice, OptionGroup, PerGameCommonOptions, Range, DeathLink, Toggle

class HardcoreMode(Toggle):
	"""
	Enables Hardcore clears to give items as well.
	(Makes it so that )
	"""

	display_name = "Hardcore Mode"

class HardLocations(Toggle):
	"""
	Enables more lenient rules that allow for locations to become a lot harder.
	"""

	display_name = "Hard Locations"

class PlayerShape(Choice):
	"""
	The shape that the player will play as.
	Square is Cyan, Triangle (P2) is Yellow, Pentagon (P3) is Green, Circle (P4) is Orange
	This is purely cosmetic and won't change anything in any Challenge Run that isn't in a Local Couch lobby.
	"""

	display_name = "Player Shape"

	option_square = 0
	option_triangle = 1
	option_pentagon = 2
	option_circle = 3

	default = option_square

	alias_cyan = option_square
	alias_yellow = option_triangle
	alias_green = option_pentagon
	alias_lime = option_pentagon
	alias_orange = option_circle

class StartingMaxHP(Range):
	"""
	Amount of max HP that is available to you at the start of the session.
	Keep in mind max HP is always doubled in boss stages.
	"""

	display_name = "Starting Max HP"

	range_start = 1
	range_end = 20

	default = 3

class MaxHPItemCount(Range):
	"""
	The amount of max HP upgrades to put into the multiworld.
	Keep in mind max HP is always doubled in boss stages.
	"""

	display_name = "Max HP Up Item Count"

	range_start = 0
	range_end = 20

	default = 0

class RandomizeDashDirections(Toggle):
	"""
	Whether to randomize dash directions and make it so that you have to collect them to be able to dash in specific directions.
	"""

	display_name = "Randomize Dash Directions"

class DashDirectionCount(Choice):
	"""
	How many dash directions should you be allowed?
	4 means if you have the Up dash direction and some other dash direction, you can combine both to say, dash up-right or up-left.
	8 means you also have to find dash directions like Up-Right or Down-Left.
	"""

	display_name = "Dash Direction Count"

	option_four = 0
	option_eight = 1

	default = option_four

class ChallengeSongRegularTickets(Range):
	"""
	How many regular song clears from Challenge Runs will be in logic?
	(This will be how many regular songs you'll be able to complete in a challenge run for items.)
	This will also randomize "tickets" that you are required to have to be eligible for an item reward from completing these levels!
	"""

	display_name = "Regular Song Challenge Run Ticket Count"

	range_start = 0
	range_end = 1000

	default = 18

class ChallengeSongBossTickets(Range):
	"""
	How many regular song clears from Challenge Runs will be in logic?
	(This will be how many regular songs you'll be able to complete in a challenge run for items.)

	Ideally, the ratio of boss tickets to regular tickets should be 1:2.

	This will also randomize "tickets" that you are required to have to be eligible for an item reward from completing these levels!
	"""

	display_name = "Regular Song Challenge Run Ticket Count"

	range_start = 0
	range_end = 500

	default = 9

class PlaylistEnableExtras(Toggle):
	"""
	Whether to include the Extras tab.
	You may want to disable this if you have barely done any challenge runs previously, as some of the Extra songs require you to complete challenge runs. (50 required for all "Complete X Challenge Runs", dashing 5000 times in total required and rescuing 100 players in total)

	If you enable this, make sure to also change the amount of Beatpoints you actually have in game so you're able to play the song you actually have unlocked.
	"""

	display_name = "Enable Extras songs"

class AmountOfBeatpoints(Range):
	"""
	How many Beatpoints you actually have in your save.
	This is only for generation, and will make the generation automatically exclude locations that are not unlocked in your main save.
	"""

	display_name = "Beatpoint amount"

	range_start = 0
	range_end = 1000000

	default = 0

class TrapChance(Range):
	"""
	Chance for a trap to be replaced with a random filler item.
	"""

	display_name = "Trap chance"

	range_start = 0
	range_end = 99

	default = 5

class FreeDashItemCount(Range):
	"""
	Amount of free dash items that will give that amount of free dashes you can use to dash in any direction.
	This will apply per-stage, and won't be used up.

	This is particularly powerful, and is only there to act as "useful filler" for players to find instead of Nothing.
	"""

	display_name = "Free dash count"

	range_start = 0
	range_end = 1000
	
	default = 1

class VictoryKeysReq(Range):
	"""
	Amount of victory keys required.
	"""

	display_name = "Victory Key Count"

	range_start = 1
	range_end = 1000

	default = 3

@dataclass
class JSABOptions(PerGameCommonOptions):
	hardcore_mode: HardcoreMode
	hard_locs: HardLocations
	death_link: DeathLink
	player_shape: PlayerShape
	starting_max_hp: StartingMaxHP
	max_hp_count: MaxHPItemCount
	rando_dash_dir: RandomizeDashDirections
	rando_dash_count: DashDirectionCount
	free_dash_count: FreeDashItemCount
	trap_chance: TrapChance
	challenge_regular_tickets: ChallengeSongRegularTickets
	challenge_boss_tickets: ChallengeSongBossTickets
	victory_key_requirement: VictoryKeysReq
	playlist_extras_enabled: PlaylistEnableExtras
	beatpoint_amount: AmountOfBeatpoints