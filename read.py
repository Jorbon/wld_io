from math import ceil
import os
import struct
from structures import *

def read_world_file(name:str) -> World:
	w = World()
	file = open(os.path.expanduser(f"~\\Documents\\My Games\\Terraria\\Worlds\\{name}.wld"), "rb")
	
	def num(n:int) -> int:
		return int.from_bytes(file.read(n), "little")

	def string(sb:int=1) -> str:
		return str(file.read(num(sb)))[2:-1]

	def single() -> float:
		return struct.unpack("<f", file.read(4))[0]

	def double() -> float:
		return struct.unpack("<d", file.read(8))[0]
	
	def check_position(index):
		if positions[index] != file.tell():
			raise RuntimeError(f"Position {index} is off by {abs(file.tell() - positions[index])}! Reader says {hex(file.tell())}, but file data says {hex(positions[index])}")
	
	
	# Pre header
	
	w.version = num(4)
	w.format = file.read(7)
	w.file_type = num(1)
	w.revision = num(4)
	w.is_favorite = num(8)
	positions_len = num(2)
	positions = list(num(4) for i in range(positions_len))
	importance_len = num(2)
	
	n = num(ceil(importance_len / 8))
	for i in range(importance_len):
		w.importance.append(n & 1 == 1)
		n >>= 1
	
	check_position(0)
	
	
	# Header
	print(f"{name}: Reading header")
	
	w.name = string()
	w.header["seed"] = string()
	w.header["world_gen_version"] = num(8)
	w.header["guid"] = file.read(16)
	w.id = file.read(4)
	w.header["left"] = num(4)
	w.header["right"] = num(4)
	w.header["top"] = num(4)
	w.header["bottom"] = num(4)
	w.height = num(4)
	w.width = num(4)
	w.header["gamemode"] = num(4)
	w.header["drunk_world"] = bool(num(1))
	w.header["good_world"] = bool(num(1))
	w.header["tenth_anniversary_world"] = bool(num(1))
	w.header["dont_starve_world"] = bool(num(1))
	w.header["notthebees_world"] = bool(num(1))
	w.header["remix_world"] = bool(num(1))
	w.header["notraps_world"] = bool(num(1))
	w.header["zenith_world"] = bool(num(1))
	w.header["creation_time"] = num(8)
	w.header["moon_type"] = num(1)
	w.header["tree_type_xcoords"] = list(num(4) for i in range(3))
	w.header["tree_styles"] = list(num(4) for i in range(4))
	w.header["cave_bg_xcoords"] = list(num(4) for i in range(3))
	w.header["cave_bg_styles"] = list(num(4) for i in range(4))
	w.header["ice_bg_style"] = num(4)
	w.header["jungle_bg_style"] = num(4)
	w.header["hell_bg_style"] = num(4)
	w.header["spawn_x"] = num(4)
	w.header["spawn_y"] = num(4)
	w.header["world_surface_y"] = double()
	w.header["rock_layer_y"] = double()
	w.header["game_time"] = double()
	w.header["is_day"] = bool(num(1))
	w.header["moon_phase"] = num(4)
	w.header["blood_moon"] = bool(num(1))
	w.header["eclipse"] = bool(num(1))
	w.header["dungeon_x"] = num(4)
	w.header["dungeon_y"] = num(4)
	w.header["crimson_world"] = bool(num(1))
	w.header["killed_eye_of_cthulu"] = bool(num(1))
	w.header["killed_eater_of_worlds"] = bool(num(1))
	w.header["killed_skeletron"] = bool(num(1))
	w.header["killed_queen_bee"] = bool(num(1))
	w.header["killed_the_destroyer"] = bool(num(1))
	w.header["killed_the_twins"] = bool(num(1))
	w.header["killed_skeletron_prime"] = bool(num(1))
	w.header["killed_any_hardmode_boss"] = bool(num(1))
	w.header["killed_plantera"] = bool(num(1))
	w.header["killed_golem"] = bool(num(1))
	w.header["killed_slime_king"] = bool(num(1))
	w.header["saved_goblin_tinkerer"] = bool(num(1))
	w.header["saved_wizard"] = bool(num(1))
	w.header["saved_mechanic"] = bool(num(1))
	w.header["defeated_goblin_invasion"] = bool(num(1))
	w.header["killed_clown"] = bool(num(1))
	w.header["defeated_frost_legion"] = bool(num(1))
	w.header["defeated_pirates"] = bool(num(1))
	w.header["broken_shadow_orb"] = bool(num(1))
	w.header["meteor_spawned"] = bool(num(1))
	w.header["shadow_orbs_broken_mod3"] = num(1)
	w.header["altars_smashed"] = num(4)
	w.header["hard_mode"] = bool(num(1))
	w.header["after_party_of_doom"] = bool(num(1))
	w.header["goblin_invasion_delay"] = num(4)
	w.header["goblin_invasion_size"] = num(4)
	w.header["goblin_invasion_type"] = num(4)
	w.header["goblin_invasion_x"] = double()
	w.header["slime_rain_time"] = double()
	w.header["sundial_cooldown"] = num(1)
	w.header["is_raining"] = num(1)
	w.header["rain_time"] = num(4)
	w.header["max_rain"] = single()
	w.header["tier_1_ore_id"] = num(4)
	w.header["tier_2_ore_id"] = num(4)
	w.header["tier_3_ore_id"] = num(4)
	w.header["tree_style"] = num(1)
	w.header["corruption_style"] = num(1)
	w.header["jungle_style"] = num(1)
	w.header["snow_style"] = num(1)
	w.header["hallow_style"] = num(1)
	w.header["crimson_style"] = num(1)
	w.header["desert_style"] = num(1)
	w.header["ocean_style"] = num(1)
	w.header["cloud_bg"] = num(4)
	w.header["num_clouds"] = num(2)
	w.header["wind_speed"] = single()
	
	w.header["num_angler_finishers"] = num(4)
	w.header["angler_finishers"] = list((string() for i in range(w.header["num_angler_finishers"])))
	w.header["saved_angler"] = bool(num(1))
	w.header["angler_quest"] = num(4)
	w.header["saved_stylist"] = bool(num(1))
	w.header["saved_tax_collector"] = bool(num(1))
	w.header["saved_golfer"] = bool(num(1))
	w.header["invasion_size_start"] = num(4)
	w.header["temp_cultist_delay"] = num(4)
	w.header["num_kill_counts"] = num(2)
	w.header["kill_counts"] = list(num(4) for i in range(w.header["num_kill_counts"]))
	w.header["fast_forward_time"] = bool(num(1))
	w.header["downed_fishron"] = bool(num(1))
	w.header["downed_martians"] = bool(num(1))
	w.header["downed_ancient_cultist"] = bool(num(1))
	w.header["downed_moonlord"] = bool(num(1))
	w.header["downed_halloween_king"] = bool(num(1))
	w.header["downed_halloween_tree"] = bool(num(1))
	w.header["downed_christmas_ice_queen"] = bool(num(1))
	w.header["downed_christmas_santank"] = bool(num(1))
	w.header["downed_christmas_tree"] = bool(num(1))
	w.header["downed_tower_solar"] = bool(num(1))
	w.header["downed_tower_vortex"] = bool(num(1))
	w.header["downed_tower_nebula"] = bool(num(1))
	w.header["downed_tower_stardust"] = bool(num(1))
	w.header["tower_active_solar"] = bool(num(1))
	w.header["tower_active_vortex"] = bool(num(1))
	w.header["tower_active_nebula"] = bool(num(1))
	w.header["tower_active_stardust"] = bool(num(1))
	w.header["lunar_apocalypse_is_up"] = bool(num(1))
	w.header["party_manual"] = bool(num(1))
	w.header["party_genuine"] = bool(num(1))
	w.header["party_cooldown"] = num(4)
	w.header["num_party_celebrating_npcs"] = num(4)
	w.header["party_celebrating_npcs"] = list(num(4) for i in range(w.header["num_party_celebrating_npcs"]))
	w.header["sandstorm_happening"] = bool(num(1))
	w.header["sandstorm_time_left"] = num(4)
	w.header["sandstorm_severity"] = single()
	w.header["sandstorm_intended_severity"] = single()
	w.header["saved_bartender"] = bool(num(1))
	w.header["downed_invasion_tier_1"] = bool(num(1))
	w.header["downed_invasion_tier_2"] = bool(num(1))
	w.header["downed_invasion_tier_3"] = bool(num(1))
	w.header["mushroom_bg_style"] = num(1)
	w.header["underworld_bg_style"] = num(1)
	w.header["tree2_bg_style"] = num(1)
	w.header["tree3_bg_style"] = num(1)
	w.header["tree4_bg_style"] = num(1)
	w.header["combat_book_was_used"] = bool(num(1))
	w.header["lantern_night_stuff"] = num(4)
	w.header["lantern_night_more_stuff"] = list(bool(num(1)) for i in range(3))
	w.header["num_tree_top_stuff"] = num(4)
	w.header["tree_top_stuff"] = list(num(4) for i in range(min(13, w.header["num_tree_top_stuff"])))
	w.header["force_halloween_for_today"] = bool(num(1))
	w.header["force_xmas_for_today"] = bool(num(1))
	w.header["copper_tier"] = num(4)
	w.header["iron_tier"] = num(4)
	w.header["silver_tier"] = num(4)
	w.header["gold_tier"] = num(4)
	w.header["bought_cat"] = bool(num(1))
	w.header["bought_dog"] = bool(num(1))
	w.header["bought_bunny"] = bool(num(1))
	w.header["downed_empress_of_light"] = bool(num(1))
	w.header["downed_queen_slime"] = bool(num(1))
	w.header["downed_deerclops"] = bool(num(1))
	w.header["unlocked_slime_blue_spawn"] = bool(num(1))
	w.header["unlocked_merchant_spawn"] = bool(num(1))
	w.header["unlocked_demolitionist_spawn"] = bool(num(1))
	w.header["unlocked_party_girl_spawn"] = bool(num(1))
	w.header["unlocked_dye_trader_spawn"] = bool(num(1))
	w.header["unlocked_truffle_spawn"] = bool(num(1))
	w.header["unlocked_arms_dealer_spawn"] = bool(num(1))
	w.header["unlocked_nurse_spawn"] = bool(num(1))
	w.header["unlocked_princess_spawn"] = bool(num(1))
	w.header["combat_book_v2_was_used"] = bool(num(1))
	w.header["peddlers_satched_was_used"] = bool(num(1))
	w.header["unlocked_slime_green_spawn"] = bool(num(1))
	w.header["unlocked_slime_old_spawn"] = bool(num(1))
	w.header["unlocked_slime_purple_spawn"] = bool(num(1))
	w.header["unlocked_slime_rainbow_spawn"] = bool(num(1))
	w.header["unlocked_slime_red_spawn"] = bool(num(1))
	w.header["unlocked_slime_yellow_spawn"] = bool(num(1))
	w.header["unlocked_slime_copper_spawn"] = bool(num(1))
	w.header["fast_forward_to_dusk"] = bool(num(1))
	w.header["moondial_cooldown"] = num(1)
	
	check_position(1)
	
	
	# Tiles
	print(f"{name}: Reading tiles...")
	prog = 0
	step = 10
	
	for x in range(w.width):
		p = 100 * x / w.width
		if p >= prog + step:
			prog += step
			print(f"{prog}%")
		
		y = 0
		while y < w.height:
			if file.tell() > 0x7ae0:
				pass
			
			a = num(1)
			b = 0
			c = 0
			tile = Tile()
			
			if a & 1 == 1:
				b = num(1)
			if b & 1 == 1:
				c = num(1)
			if c & 1 == 1:
				raise RuntimeError("c1")
			if b & 128 == 128:
				raise RuntimeError("b7")
			
			if a & 2 == 2:
				tile.has_block = True
				if a & 32 == 32:
					tile.type = num(2)
				else:
					tile.type = num(1)
				
				if w.importance[tile.type]:
					tile.texture_u = num(2)
					tile.texture_v = num(2)
					if tile.type == 144:
						tile.texture_v = 0
				else:
					tile.texture_u = -1
					tile.texture_v = -1
				
				if c & 8 == 8:
					tile.color = num(1)
					tile.has_color = True
			
			if a & 4 == 4:
				tile.has_wall = True
				if c & 64 == 64:
					tile.wall_type = num(2)
				else:
					tile.wall_type = num(1)
				
				if c & 16 == 16:
					tile.has_wall_color = True
					tile.wall_color = num(1)
			
			a43 = (a >> 3) & 3
			if a43 > 0:
				tile.has_liquid = True
				tile.liquid_amount = num(1)
				tile.is_shimmer = c & 128 == 128
				tile.is_lava = a43 == 2
				tile.is_honey = a43 == 3
			
			if b > 1:
				tile.has_red_wire = b & 2 == 2
				tile.has_green_wire = b & 4 == 4
				tile.has_blue_wire = b & 8 == 8
				tile.slope = (b >> 4) & 7
				
				if x == 63 and 760 <= y <= 770:
					pass
			
			if c > 0:
				tile.has_actuator = c & 2 == 2
				tile.is_inactive = c & 4 == 4
				tile.has_yellow_wire = c & 32 == 32
			
			
			a76 = a >> 6
			if a76 == 3:
				raise RuntimeError("a76 is 3")
			k = 0
			if a76 == 1:
				k = num(1)
			elif a76 >= 2:
				k = num(2)
			
			w.tiles.append(tile)
			while k > 0:
				y += 1
				w.tiles.append(tile)
				k -= 1
			y += 1
		
		if y != w.height:
			raise RuntimeError(f"Tiles counted wrong. X: {x}, Height is {w.height}, but {y} blocks in column")
	
	check_position(2)
	
	
	# Chests
	print(f"{name}: Reading chests")
	
	num_chests = num(2)
	
	chest_size = num(2)
	if chest_size != 40:
		raise RuntimeError(f"Chest size is {chest_size}, not 40")
	
	for i in range(num_chests):
		chest = Chest(num(4), num(4), string())
		
		for j in range(40):
			item = Item()
			item.count = num(2)
			if item.count > 0:
				item.id = num(4)
				item.prefix = num(1)
				chest.items.append(item)
		
		w.chests.append(chest)
	
	check_position(3)
	
	
	# Signs
	print(f"{name}: Reading signs")
	
	num_signs = num(2)
	for i in range(num_signs):
		text = string()
		x = num(4)
		y = num(4)
		tile = w.tiles[x*w.height + y]
		if tile.has_block and (tile.type == 55 or tile.type == 85):
			w.signs.append(Sign(x, y, text))
	
	check_position(4)
	
	
	# NPCs
	print(f"{name}: Reading npcs")
	
	num_shimmered = num(4)
	shimmered = list(num(4) for i in range(num_shimmered))
	
	
	flag = bool(num(1))
	while flag:
		npc = Npc()
		npc.sprite_id = num(4)
		npc.name = string()
		npc.x = single()
		npc.y = single()
		npc.is_homeless = bool(num(1))
		npc.home_x = num(4)
		npc.home_y = num(4)
		if bool(num(1)):
			npc.variation_index = num(4)
		w.npcs.append(npc)
		
		flag = bool(num(1))
	
	for i in shimmered:
		w.npcs[i].is_shimmered = True
	
	flag = bool(num(1))
	while flag:
		npc = Npc()
		npc.sprite_id = num(4)
		npc.x = single()
		npc.y = single()
		npc.is_pillar = True
		w.npcs.append(npc)
		
		flag = bool(num(1))
	
	check_position(5)
	
	
	# Tile Entities
	print(f"{name}: Reading misc data")
	
	num_tile_entities = num(4)
	for i in range(num_tile_entities):
		te = TileEntity(num(1), num(4), num(2), num(2))
		
		if te.type == 0: # target dummy
			te.data["dummy_npc"] = num(2)
		elif te.type == 1: # item frame
			te.data["item"] = Item(num(2), num(1), num(2))
		elif te.type == 2: # logic sensor
			te.data["logic_check"] = num(1)
			te.data["on"] = bool(num(1))
		elif te.type == 3: # display doll
			items = []
			dyes = []
			
			item_slots = num(1)
			dye_slots = num(1)
			
			for i in range(8):
				if (item_slots >> i) & 1 == 1:
					items.append(Item(num(2), num(1), num(2)))
				else:
					items.append(Item())
			for i in range(8):
				if (dye_slots >> i) & 1 == 1:
					dyes.append(Item(num(2), num(1), num(2)))
				else:
					dyes.append(Item())
			
			
			te.data["items"] = items
			te.data["dyes"] = dyes
		elif te.type == 4: # weapon rack
			te.data["item"] = Item(num(2), num(1), num(2))
		elif te.type == 5: # hat rack
			te.data["items"] = [Item(), Item()]
			te.data["dyes"] = [Item(), Item()]
			
			slots = num(1)
			if slots & 1 == 1:
				te.data["items"][0] = Item(num(2), num(1), num(2))
			if slots & 2 == 2:
				te.data["items"][1] = Item(num(2), num(1), num(2))
			if slots & 4 == 4:
				te.data["dyes"][0] = Item(num(2), num(1), num(2))
			if slots & 8 == 8:
				te.data["dyes"][1] = Item(num(2), num(1), num(2))
			
		elif te.type == 6: # food platter
			te.data["item"] = Item(num(2), num(1), num(2))
		elif te.type == 7: # pylon
			pass
		
		w.tile_entities.push(te)
	
	check_position(6)
	
	
	# Weighted Pressure Plates
	
	num_plates = num(4)
	for i in range(num_plates):
		w.weighted_pressure_plates.append((num(4), num(4)))
	
	check_position(7)
	
	
	# NPC Rooms
	
	num_rooms = num(4)
	for i in range(num_rooms):
		w.npc_rooms.append((num(4), num(4), num(4)))
	
	check_position(8)
	
	
	# Bestiary
	
	n = num(4)
	for i in range(n):
		s = string()
		w.bestiary_kills[s] = num(4)
	n = num(4)
	for i in range(n):
		w.bestiary_sights.append(string())
	n = num(4)
	for i in range(n):
		w.bestiary_chats.append(string())
	
	check_position(9)
	
	
	# Creative Powers
	
	if file.read(3) != b"\x01\x00\x00":
		raise RuntimeError("Powers num 1 is wrong")
	w.creative_powers["freeze_time"] = bool(num(1))
	if file.read(3) != b"\x01\x08\x00":
		raise RuntimeError("Powers num 2 is wrong")
	w.creative_powers["time_rate"] = single()
	if file.read(3) != b"\x01\x09\x00":
		raise RuntimeError("Powers num 3 is wrong")
	w.creative_powers["freeze_weather"] = bool(num(1))
	if file.read(3) != b"\x01\x0a\x00":
		raise RuntimeError("Powers num 4 is wrong")
	w.creative_powers["freeze_wind"] = bool(num(1))
	if file.read(3) != b"\x01\x0c\x00":
		raise RuntimeError("Powers num 5 is wrong")
	w.creative_powers["difficulty_slider"] = single()
	if file.read(3) != b"\x01\x0d\x00":
		raise RuntimeError("Powers num 6 is wrong")
	w.creative_powers["freeze_spread"] = bool(num(1))
	if file.read(1) != b"\x00":
		raise RuntimeError("Powers byte is wrong")
	
	check_position(10)
	
	
	# Footer
	
	if not bool(num(1)):
		raise RuntimeError("Footer boolean is false")
	
	footer_name = string()
	if footer_name != w.name:
		raise RuntimeError(f"Footer name doesn't match: found '{footer_name}' instead of '{w.name}'")
	footer_id = file.read(4)
	if footer_id != w.id:
		raise RuntimeError(f"Footer id doesn't match: found '{footer_id}' instead of '{w.id}'")
	
	file.close()
	print(f"{name}: Done reading")
	return w