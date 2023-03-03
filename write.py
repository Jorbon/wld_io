from math import ceil
import os
import struct
from structures import *

def write_world_file(name:str, w:World, ignore_size_limit=False):
	if not ignore_size_limit:
		if w.width > 8401:
			print(f"Warning: World with width {w.width} will only be loadable in other viewers and editors. The max width Terraria can load is 8400 tiles.")
		if w.height > 2400:
			print(f"Warning: World with height {w.height} will only be loadable in other viewers and editors. The max height Terraria can load is 2400 tiles.")
	
	def num(value:int, n:int) -> bytes:
		return value.to_bytes(n, "little")
	
	def string(s:str, sb:int=1) -> bytes:
		return len(s).to_bytes(sb, "little") + bytes(s, "utf")
	
	def single(value:float) -> bytes:
		return struct.pack("<f", value)
	
	def double(value:float) -> bytes:
		return struct.pack("<d", value)
	
	def boolean(value:bool) -> bytes:
		if value:
			return b"\x01"
		return b"\x00"
	
	
	# Pre header
	
	positions = []
	
	prepos = num(w.version, 4) + w.format + num(w.file_type, 1) + num(w.revision, 4) + num(w.is_favorite, 8) + num(11, 2)
	
	n = 0
	place = 1
	for b in w.importance:
		if b:
			n += place
		place <<= 1
	
	importance = num(len(w.importance), 2) + num(n, ceil(len(w.importance) / 8))
	
	positions.append(len(prepos) + 44 + len(importance))
	
	
	# Header
	print(f"{name}: Writing header")
	
	header = b""
	header += string(w.name)
	header += string(w.header["seed"])
	header += num(w.header["world_gen_version"], 8)
	header += w.header["guid"]
	header += w.id
	header += num(0, 4)
	header += num(w.width * 16, 4)
	header += num(0, 4)
	header += num(w.height * 16, 4)
	header += num(w.height, 4)
	header += num(w.width, 4)
	header += num(w.header["gamemode"], 4)
	header += boolean(w.header["drunk_world"])
	header += boolean(w.header["good_world"])
	header += boolean(w.header["tenth_anniversary_world"])
	header += boolean(w.header["dont_starve_world"])
	header += boolean(w.header["notthebees_world"])
	header += boolean(w.header["remix_world"])
	header += boolean(w.header["notraps_world"])
	header += boolean(w.header["zenith_world"])
	header += num(w.header["creation_time"], 8)
	header += num(w.header["moon_type"], 1)
	header += b"".join(tuple(num(n, 4) for n in w.header["tree_type_xcoords"]))
	header += b"".join(tuple(num(n, 4) for n in w.header["tree_styles"]))
	header += b"".join(tuple(num(n, 4) for n in w.header["cave_bg_xcoords"]))
	header += b"".join(tuple(num(n, 4) for n in w.header["cave_bg_styles"]))
	header += num(w.header["ice_bg_style"], 4)
	header += num(w.header["jungle_bg_style"], 4)
	header += num(w.header["hell_bg_style"], 4)
	header += num(w.header["spawn_x"], 4)
	header += num(w.header["spawn_y"], 4)
	header += double(w.header["world_surface_y"])
	header += double(w.header["rock_layer_y"])
	header += double(w.header["game_time"])
	header += boolean(w.header["is_day"])
	header += num(w.header["moon_phase"], 4)
	header += boolean(w.header["blood_moon"])
	header += boolean(w.header["eclipse"])
	header += num(w.header["dungeon_x"], 4)
	header += num(w.header["dungeon_y"], 4)
	header += boolean(w.header["crimson_world"])
	header += boolean(w.header["killed_eye_of_cthulu"])
	header += boolean(w.header["killed_eater_of_worlds"])
	header += boolean(w.header["killed_skeletron"])
	header += boolean(w.header["killed_queen_bee"])
	header += boolean(w.header["killed_the_destroyer"])
	header += boolean(w.header["killed_the_twins"])
	header += boolean(w.header["killed_skeletron_prime"])
	header += boolean(w.header["killed_any_hardmode_boss"])
	header += boolean(w.header["killed_plantera"])
	header += boolean(w.header["killed_golem"])
	header += boolean(w.header["killed_slime_king"])
	header += boolean(w.header["saved_goblin_tinkerer"])
	header += boolean(w.header["saved_wizard"])
	header += boolean(w.header["saved_mechanic"])
	header += boolean(w.header["defeated_goblin_invasion"])
	header += boolean(w.header["killed_clown"])
	header += boolean(w.header["defeated_frost_legion"])
	header += boolean(w.header["defeated_pirates"])
	header += boolean(w.header["broken_shadow_orb"])
	header += boolean(w.header["meteor_spawned"])
	header += num(w.header["shadow_orbs_broken_mod3"], 1)
	header += num(w.header["altars_smashed"], 4)
	header += boolean(w.header["hard_mode"])
	header += boolean(w.header["after_party_of_doom"])
	header += num(w.header["goblin_invasion_delay"], 4)
	header += num(w.header["goblin_invasion_size"], 4)
	header += num(w.header["goblin_invasion_type"], 4)
	header += double(w.header["goblin_invasion_x"])
	header += double(w.header["slime_rain_time"])
	header += num(w.header["sundial_cooldown"], 1)
	header += num(w.header["is_raining"], 1)
	header += num(w.header["rain_time"], 4)
	header += single(w.header["max_rain"])
	header += num(w.header["tier_1_ore_id"], 4)
	header += num(w.header["tier_2_ore_id"], 4)
	header += num(w.header["tier_3_ore_id"], 4)
	header += num(w.header["tree_style"], 1)
	header += num(w.header["corruption_style"], 1)
	header += num(w.header["jungle_style"], 1)
	header += num(w.header["snow_style"], 1)
	header += num(w.header["hallow_style"], 1)
	header += num(w.header["crimson_style"], 1)
	header += num(w.header["desert_style"], 1)
	header += num(w.header["ocean_style"], 1)
	header += num(w.header["cloud_bg"], 4)
	header += num(w.header["num_clouds"], 2)
	header += single(w.header["wind_speed"])

	header += num(len(w.header["angler_finishers"]), 4)
	header += b"".join(tuple(string(n) for n in w.header["angler_finishers"]))
	header += boolean(w.header["saved_angler"])
	header += num(w.header["angler_quest"], 4)
	header += boolean(w.header["saved_stylist"])
	header += boolean(w.header["saved_tax_collector"])
	header += boolean(w.header["saved_golfer"])
	header += num(w.header["invasion_size_start"], 4)
	header += num(w.header["temp_cultist_delay"], 4)
	header += num(len(w.header["kill_counts"]), 2)
	header += b"".join(tuple(num(n, 4) for n in w.header["kill_counts"]))
	header += boolean(w.header["fast_forward_time"])
	header += boolean(w.header["downed_fishron"])
	header += boolean(w.header["downed_martians"])
	header += boolean(w.header["downed_ancient_cultist"])
	header += boolean(w.header["downed_moonlord"])
	header += boolean(w.header["downed_halloween_king"])
	header += boolean(w.header["downed_halloween_tree"])
	header += boolean(w.header["downed_christmas_ice_queen"])
	header += boolean(w.header["downed_christmas_santank"])
	header += boolean(w.header["downed_christmas_tree"])
	header += boolean(w.header["downed_tower_solar"])
	header += boolean(w.header["downed_tower_vortex"])
	header += boolean(w.header["downed_tower_nebula"])
	header += boolean(w.header["downed_tower_stardust"])
	header += boolean(w.header["tower_active_solar"])
	header += boolean(w.header["tower_active_vortex"])
	header += boolean(w.header["tower_active_nebula"])
	header += boolean(w.header["tower_active_stardust"])
	header += boolean(w.header["lunar_apocalypse_is_up"])
	header += boolean(w.header["party_manual"])
	header += boolean(w.header["party_genuine"])
	header += num(w.header["party_cooldown"], 4)
	header += num(len(w.header["party_celebrating_npcs"]), 4)
	header += b"".join(tuple(num(n, 4) for n in w.header["party_celebrating_npcs"]))
	header += boolean(w.header["sandstorm_happening"])
	header += num(w.header["sandstorm_time_left"], 4)
	header += single(w.header["sandstorm_severity"])
	header += single(w.header["sandstorm_intended_severity"])
	header += boolean(w.header["saved_bartender"])
	header += boolean(w.header["downed_invasion_tier_1"])
	header += boolean(w.header["downed_invasion_tier_2"])
	header += boolean(w.header["downed_invasion_tier_3"])
	header += num(w.header["mushroom_bg_style"], 1)
	header += num(w.header["underworld_bg_style"], 1)
	header += num(w.header["tree2_bg_style"], 1)
	header += num(w.header["tree3_bg_style"], 1)
	header += num(w.header["tree4_bg_style"], 1)
	header += boolean(w.header["combat_book_was_used"])
	header += num(w.header["lantern_night_stuff"], 4)
	header += b"".join(tuple(boolean(n) for n in w.header["lantern_night_more_stuff"]))
	header += num(len(w.header["tree_top_stuff"]), 4)
	header += b"".join(tuple(num(n, 4) for n in w.header["tree_top_stuff"]))
	header += boolean(w.header["force_halloween_for_today"])
	header += boolean(w.header["force_xmas_for_today"])
	header += num(w.header["copper_tier"], 4)
	header += num(w.header["iron_tier"], 4)
	header += num(w.header["silver_tier"], 4)
	header += num(w.header["gold_tier"], 4)
	header += boolean(w.header["bought_cat"])
	header += boolean(w.header["bought_dog"])
	header += boolean(w.header["bought_bunny"])
	header += boolean(w.header["downed_empress_of_light"])
	header += boolean(w.header["downed_queen_slime"])
	header += boolean(w.header["downed_deerclops"])
	header += boolean(w.header["unlocked_slime_blue_spawn"])
	header += boolean(w.header["unlocked_merchant_spawn"])
	header += boolean(w.header["unlocked_demolitionist_spawn"])
	header += boolean(w.header["unlocked_party_girl_spawn"])
	header += boolean(w.header["unlocked_dye_trader_spawn"])
	header += boolean(w.header["unlocked_truffle_spawn"])
	header += boolean(w.header["unlocked_arms_dealer_spawn"])
	header += boolean(w.header["unlocked_nurse_spawn"])
	header += boolean(w.header["unlocked_princess_spawn"])
	header += boolean(w.header["combat_book_v2_was_used"])
	header += boolean(w.header["peddlers_satched_was_used"])
	header += boolean(w.header["unlocked_slime_green_spawn"])
	header += boolean(w.header["unlocked_slime_old_spawn"])
	header += boolean(w.header["unlocked_slime_purple_spawn"])
	header += boolean(w.header["unlocked_slime_rainbow_spawn"])
	header += boolean(w.header["unlocked_slime_red_spawn"])
	header += boolean(w.header["unlocked_slime_yellow_spawn"])
	header += boolean(w.header["unlocked_slime_copper_spawn"])
	header += boolean(w.header["fast_forward_to_dusk"])
	header += num(w.header["moondial_cooldown"], 1)
	
	positions.append(positions[-1] + len(header))
	
	
	# Tiles
	print(f"{name}: Writing tiles...")
	prog = 0
	step = 10
	
	
	tiles = []
	i = 0
	while True:
		p = 100 * i / (w.width * w.height)
		if p >= prog + step:
			prog += step
			print(f"{prog}%")
		
		tile = w.tiles[i]
		
		a = 0
		b = 0
		c = 0
		
		type_b = b""
		tex_b = b""
		color_b = b""
		wall_type_b = b""
		wall_color_b = b""
		liquid_amount_b = b""
		k = b""
		
		# scan for copies
		
		copies = 0
		while True:
			i += 1
			if i >= w.width*w.height or tile != w.tiles[i] or i % w.height == 0:
				if copies >= 256:
					a += 128
					k = num(copies, 2)
				elif copies > 0:
					a += 64
					k = num(copies, 1)
				break
			copies += 1
		
		# construct header bytes
		
		use_c = (tile.has_block and (tile.is_inactive or tile.has_color)) or (tile.has_wall and (tile.has_wall_color or tile.wall_type >= 256)) or (tile.has_liquid and tile.is_shimmer) or tile.has_yellow_wire or tile.has_actuator
		use_b = use_c or (tile.has_block and tile.slope > 0) or tile.has_red_wire or tile.has_green_wire or tile.has_blue_wire
		
		
		if tile.has_block:
			a += 2
			if tile.type >= 256:
				a += 32
				type_b = num(tile.type, 2)
			else:
				type_b = num(tile.type, 1)
			
			if w.importance[tile.type]:
				tex_b = num(tile.texture_u, 2) + num(tile.texture_v, 2)
		
		if tile.has_wall:
			a += 4
			if tile.wall_type >= 256:
				wall_type_b = num(tile.wall_type, 2)
			else:
				wall_type_b = num(tile.wall_type, 1)
		
		l = 0
		if tile.has_liquid:
			liquid_amount_b = num(tile.liquid_amount, 1)
			if tile.is_shimmer:
				l = 1
			elif tile.is_honey:
				l = 3
			elif tile.is_lava:
				l = 2
			else:
				l = 1
		a += l << 3
		
		if use_b:
			a += 1
			if tile.has_red_wire:
				b += 2
			if tile.has_green_wire:
				b += 4
			if tile.has_blue_wire:
				b += 8
			if tile.has_block:
				b += (tile.slope & 7) << 4
			
			if use_c:
				b += 1
				if tile.has_actuator:
					c += 2
				if tile.has_yellow_wire:
					c += 32
				if tile.has_liquid and tile.is_shimmer:
					c += 128
				if tile.has_block:
					if tile.is_inactive:
						c += 4
					if tile.has_color:
						c += 8
						color_b = num(tile.color, 1)
				if tile.has_wall:
					if tile.wall_type >= 256:
						c += 64
					if tile.has_wall_color:
						c += 16
						wall_color_b = num(tile.wall_color, 1)
		
		# assemble byte code in order
		
		t = num(a, 1)
		if use_b:
			t += num(b, 1)
		if use_c:
			t += num(c, 1)
		
		t += type_b + tex_b + color_b + wall_type_b + wall_color_b + liquid_amount_b + k
		
		tiles.append(t)
		
		if i >= w.width*w.height:
			break
	
	tiles = b"".join(tiles)
	
	positions.append(positions[-1] + len(tiles))
	
	
	# Chests
	print(f"{name}: Writing chests")
	
	chests = num(len(w.chests), 2) + num(40, 2)
	
	for chest in w.chests:
		chests += num(chest.x, 4) + num(chest.y, 4) + string(chest.name)
		for i in range(40):
			if i < len(chest.items):
				chests += num(chest.items[i].count, 2)
				if chest.items[i].count > 0:
					chests += num(chest.items[i].id, 4) + num(chest.items[i].prefix, 1)
			else:
				chests += num(0, 2)
	
	positions.append(positions[-1] + len(chests))
	
	
	# Signs
	print(f"{name}: Writing signs")
	
	signs = num(len(w.signs), 2)
	
	for sign in w.signs:
		tile = w.tiles[sign.x * w.height + sign.y]
		if tile.has_block and (tile.type == 55 or tile.type == 85):
			signs += string(sign.text) + num(sign.x, 4) + num(sign.y, 4)
	
	positions.append(positions[-1] + len(signs))
	
	
	# NPCs
	print(f"{name}: Writing npcs")
	
	s = []
	for i in range(len(w.npcs)):
		if w.npcs[i].is_shimmered:
			s.append(i)
	
	npcs = num(len(s), 4)
	for n in s:
		npcs += num(n, 4)
	
	for npc in w.npcs:
		if npc.is_pillar:
			continue
		
		npcs += boolean(True) + num(npc.sprite_id, 4) + string(npc.name) + single(npc.x) + single(npc.y) + boolean(npc.is_homeless) + num(npc.home_x, 4) + num(npc.home_y, 4)
		
		if npc.variation_index != None:
			npcs += boolean(True) + num(npc.variation_index, 4)
		else:
			npcs += boolean(False)
	
	npcs += boolean(False)
	
	for npc in w.npcs:
		if not npc.is_pillar:
			continue
		
		npcs += boolean(True) + num(npc.sprite_id, 4) + single(npc.x) + single(npc.y)
	
	npcs += boolean(False)
	
	positions.append(positions[-1] + len(npcs))
	
	
	# Tile Entities
	print(f"{name}: Writing misc data")
	
	end = num(len(w.tile_entities), 4)
	for te in w.tile_entities:
		end += num(te.type, 1) + num(te.id, 4) + num(te.x, 2) + num(te.y, 2)
		
		if te.type == 0: # target dummy
			end += num(te.data["dummy_npc"], 2)
		elif te.type == 1: # item frame
			end += num(te.data["item"].id, 2) + num(te.data["item"].prefix, 1) + num(te.data["item"].count, 2)
		elif te.type == 2: # logic sensor
			te.data["logic_check"] = num(1)
			te.data["on"] = bool(num(1))
		elif te.type == 3: # display doll
			item_slots = 0
			dye_slots = 0
			items_temp = b""
			dyes_temp = b""
			
			for i in range(8):
				if i < len(te.data["items"]):
					if te.data["items"][i].count > 0:
						item_slots += 1 << i
						items_temp += num(te.data["items"][i].id, 2) + num(te.data["items"][i].prefix, 1) + num(te.data["items"][i].count, 2)
				
				if i < len(te.data["dyes"]):
					if te.data["dyes"][i].count > 0:
						dye_slots += 1 << i
						dyes_temp += num(te.data["dyes"][i].id, 2) + num(te.data["dyes"][i].prefix, 1) + num(te.data["dyes"][i].count, 2)
			
			end += num(item_slots, 1) + num(dye_slots, 1) + items_temp + dyes_temp
		elif te.type == 4: # weapon rack
			end += num(te.data["item"].id, 2) + num(te.data["item"].prefix, 1) + num(te.data["item"].count, 2)
		elif te.type == 5: # hat rack
			slots = 0
			slots_temp = b""
			
			if te.data["items"][0].count > 0:
				slots += 1
				slots_temp += num(te.data["items"][0].id, 2) + num(te.data["items"][0].prefix, 1) + num(te.data["items"][0].count, 2)
			if te.data["items"][1].count > 0:
				slots += 2
				slots_temp += num(te.data["items"][1].id, 2) + num(te.data["items"][1].prefix, 1) + num(te.data["items"][1].count, 2)
			if te.data["dyes"][0].count > 0:
				slots += 4
				slots_temp += num(te.data["dyes"][0].id, 2) + num(te.data["dyes"][0].prefix, 1) + num(te.data["dyes"][0].count, 2)
			if te.data["dyes"][1].count > 0:
				slots += 8
				slots_temp += num(te.data["dyes"][1].id, 2) + num(te.data["dyes"][1].prefix, 1) + num(te.data["dyes"][1].count, 2)
			
			end += num(slots, 1) + slots_temp
		elif te.type == 6: # food platter
			end += num(te.data["item"].id, 2) + num(te.data["item"].prefix, 1) + num(te.data["item"].count, 2)
		elif te.type == 7: # pylon
			pass
	
	positions.append(positions[-1] + len(end))
	
	
	# Weighted Pressure Plates
	
	end += num(len(w.weighted_pressure_plates), 4)
	for plate in w.weighted_pressure_plates:
		end += num(plate[0], 4) + num(plate[1], 4)
	
	positions.append(positions[-2] + len(end))
	
	
	# NPC Rooms
	
	end += num(len(w.npc_rooms), 4)
	for room in w.npc_rooms:
		end += num(room[0], 4) + num(room[1], 4) + num(room[2], 4)
	
	positions.append(positions[-3] + len(end))
	
	
	# Bestiary
	
	end += num(len(w.bestiary_kills), 4)
	for s in w.bestiary_kills.keys():
		end += string(s) + num(w.bestiary_kills[s], 4)
	end += num(len(w.bestiary_sights), 4)
	for s in w.bestiary_sights:
		end += string(s)
	end += num(len(w.bestiary_chats), 4)
	for s in w.bestiary_chats:
		end += string(s)
	
	positions.append(positions[-4] + len(end))
	
	
	# Creative Powers
	
	end += b"\x01\x00\x00"
	end += boolean(w.creative_powers["freeze_time"])
	end += b"\x01\x08\x00"
	end += single(w.creative_powers["time_rate"])
	end += b"\x01\x09\x00"
	end += boolean(w.creative_powers["freeze_weather"])
	end += b"\x01\x0a\x00"
	end += boolean(w.creative_powers["freeze_wind"])
	end += b"\x01\x0c\x00"
	end += single(w.creative_powers["difficulty_slider"])
	end += b"\x01\x0d\x00"
	end += boolean(w.creative_powers["freeze_spread"])
	end += b"\x00"
	
	positions.append(positions[-5] + len(end))
	
	
	# Footer
	
	end += boolean(True) + string(w.name) + w.id
	
	print(f"{name}: Saving to file")
	
	file = open(os.path.expanduser(f"~\\Documents\\My Games\\Terraria\\Worlds\\{name}.wld"), "wb")
	file.write(prepos + b"".join(tuple(num(p, 4) for p in positions)) + importance + header + tiles + chests + signs + npcs + end)
	file.close()
	
	print(f"{name}: Done writing")