class Tile:
	def __init__(self):
		self.has_block = False
		self.type = 0
		self.has_color = False
		self.color = 0
		self.has_wall = False
		self.wall_type = 0
		self.has_wall_color = False
		self.wall_color = 0
		self.has_liquid = False
		self.liquid_amount = 0
		self.is_lava = False
		self.is_honey = False
		self.is_shimmer = False
		self.has_red_wire = False
		self.has_green_wire = False
		self.has_blue_wire = False
		self.has_yellow_wire = False
		self.slope = 0
		self.has_actuator = False
		self.is_inactive = False
		self.texture_u = 0
		self.texture_v = 0
	def __eq__(self, other):
		if self is other:
			return True
		if self.has_block != other.has_block or self.has_wall != other.has_wall or self.has_liquid != other.has_liquid:
			return False
		if self.has_red_wire != other.has_red_wire or self.has_green_wire != other.has_green_wire or self.has_blue_wire != other.has_blue_wire or self.has_yellow_wire != other.has_yellow_wire or self.has_actuator != other.has_actuator:
			return False
		if self.has_block:
			if self.type != other.type or self.has_color != other.has_color or self.slope != other.slope or self.is_inactive != other.is_inactive or self.texture_u != other.texture_u or self.texture_v != other.texture_v:
				return False
			if self.has_color:
				if self.color != other.color:
					return False
		if self.has_wall:
			if self.wall_type != other.wall_type or self.has_wall_color != other.has_wall_color:
				return False
			if self.has_wall_color:
				if self.wall_color != other.wall_color:
					return False
		if self.has_liquid:
			if self.liquid_amount != other.liquid_amount or self.is_shimmer != other.is_shimmer:
				return False
			if not self.is_shimmer:
				if self.is_honey != other.is_honey:
					return False
				if not self.is_honey:
					if self.is_lava != other.is_lava:
						return False
		return True
	def __str__(self):
		if self.has_block:
			return self.type
		if self.has_liquid:
			if self.is_shimmer:
				return "Shimmer"
			if self.is_honey:
				return "Honey"
			if self.is_lava:
				return "Lava"
			return "Water"
		return "Air"

"""
Tile field depedency structure:

has_block
	type
	slope
	is_inactive
	texture_u
	texture_v
	has_color
		color
has_wall
	wall_type
	has_wall_color
		wall_color
has_liquid
	liquid_amount
	!is_shimmer
		!is_honey
			is_lava
has_red_wire
has_green_wire
has_blue_wire
has_yellow_wire
has_actuator
"""

class TileData:
	def __init__(self):
		self.num = None
		self.name = None
		self.color = None
		self.pil_color = None
		self.is_solid = None
		self.subtiles = []
class SubTileData:
	def __init__(self):
		self.name = None
		self.color = None
		self.pil_color = None
		self.u = None
		self.v = None
		self.minu = None
		self.minv = None
		self.maxu = None
		self.maxv = None
class Item:
	def __init__(self, id:int=None, prefix:int=None, count:int=None):
		self.id = id
		self.prefix = prefix
		self.count = count
class Chest:
	def __init__(self, x:int=None, y:int=None, name:str=None):
		self.x = x
		self.y = y
		self.name = name
		self.items = []
class Sign:
	def __init__(self, x:int=None, y:int=None, text:str=None):
		self.x = x
		self.y = y
		self.text = text
class Npc:
	def __init__(self, id:int=None, x:float=None, y:float=None, is_homeless:bool=None, home_x:int=None, home_y:int=None):
		self.sprite_id = id
		self.x = x
		self.y = y
		self.is_homeless = is_homeless
		self.home_x = home_x
		self.home_y = home_y
		self.variation_index = None
		self.is_shimmered = False
		self.is_pillar = False
class TileEntity:
	def __init__(self, type:int=None, id:int=None, x:int=None, y:int=None):
		self.type = type
		self.id = id
		self.x = x
		self.y = y
		self.data = {}
class World:
	def __init__(self):
		self.name = ""
		self.id = b""
		self.version = 0
		self.format = b""
		self.file_type = 0
		self.revision = 0
		self.is_favorite = 0
		self.importance = []
		self.header = {}
		self.width = 0
		self.height = 0
		self.tiles = []
		self.chests = []
		self.signs = []
		self.npcs = []
		self.tile_entities = []
		self.weighted_pressure_plates = []
		self.npc_rooms = []
		self.bestiary_kills = {}
		self.bestiary_sights = []
		self.bestiary_chats = []
		self.creative_powers = {}
		