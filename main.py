from structures import *
from read import read_world_file
from write import write_world_file

from PIL import Image, ImageDraw

"""
def intn(num):
	try:
		return int(num)
	except TypeError:
		return num

def getTileInfo(tile):
	if not tile.is_active:
		color = None
		if tile.shimmer:
			color = (245, 235, 255)
		elif tile.is_liquid_honey:
			color = (230, 230, 40)
		elif tile.is_liquid_lava:
			color = (250, 90, 0)
		elif tile.is_liquid_present:
			color = (0, 0, 150)
		return (str(tile), color, False)
	
	td = tiles_data[tile.type]
	name = td.name
	color = td.pil_color
	for st in td.subtiles:
		u = tile.texture_u
		v = tile.texture_v
		if (st.u == None or u == st.u) and (st.minu == None or u >= st.minu) and (st.maxu == None or u <= st.maxu) and (st.v == None or v == st.v) and(st.minv == None or v >= st.minv) and (st.maxv == None or v <= st.maxv):
			if st.name != None:
				name = st.name
			if st.pil_color != None:
				color = st.pil_color
			break
	return (name, color, td.is_solid)
"""

# Read data file
"""
f = open("data.xml")
xml = Soup(f.read(), "xml")
f.close()
tiles_xml = xml.find_all("tile")
tiles_data = []

for t in tiles_xml:
	td = TileData()
	td.num = int(t.get("num"))
	td.name = t.get("name")
	td.color = t.get("color")
	td.is_solid = t.get("solid") == "1"
	
	if (td.color != None):
		td.pil_color = tuple(int(td.color[i:i+2], 16) for i in (1, 3, 5))
	
	subtiles_xml = t.findChildren("var", recursive=False)
	for s in subtiles_xml:
		st = SubTileData()
		st.name = s.get("name")
		st.color = s.get("color")
		st.u = intn(s.get("u"))
		st.v = intn(s.get("v"))
		st.minu = intn(s.get("minu"))
		st.minv = intn(s.get("minv"))
		st.maxu = intn(s.get("maxu"))
		st.maxv = intn(s.get("maxv"))
		scs = s.findChildren("var", recursive=False)
		for sc in scs:
			if (st.u == None):
				st.u = intn(sc.get("u"))
			if (st.v == None):
				st.v = intn(sc.get("v"))
			if (st.minu == None):
				st.minu = intn(sc.get("minu"))
			if (st.minv == None):
				st.minv = intn(sc.get("minv"))
			if (st.maxu == None):
				st.maxu = intn(sc.get("maxu"))
			if (st.maxv == None):
				st.maxv = intn(sc.get("maxv"))
		
		if st.name != None or st.color != None:
			if st.color != None:
				st.pil_color = tuple(int(st.color[i:i+2], 16) for i in (1, 3, 5))
			td.subtiles.append(st)
	tiles_data.append(td)
"""



ws = tuple(read_world_file(str(s)) for s in range(1, 5))
wm = ws[0]

w = World()

w.version = wm.version
w.format = wm.format
w.file_type = wm.file_type
w.revision = wm.revision
w.importance = wm.importance
w.header = wm.header

w.name = "1234_"
w.id = wm.id
w.height = wm.height * 2
w.width = wm.width * 2
w.header["seed"] = "42069"


w.header["tree_type_xcoords"] = [ws[0].header["tree_type_xcoords"][0], wm.width, ws[1].header["tree_type_xcoords"][0] + wm.width]
w.header["tree_styles"] = [ws[0].header["tree_styles"][0], ws[0].header["tree_styles"][1], ws[1].header["tree_styles"][0], ws[1].header["tree_styles"][1]]
w.header["cave_bg_xcoords"] = [ws[0].header["cave_bg_xcoords"][0], wm.width, ws[1].header["cave_bg_xcoords"][0] + wm.width]
w.header["cave_bg_styles"] = [ws[0].header["cave_bg_styles"][0], ws[0].header["cave_bg_styles"][1], ws[1].header["cave_bg_styles"][0], ws[1].header["cave_bg_styles"][1]]

t1 = []
t2 = []
for x in range(wm.width):
	for y in range(wm.height):
		i = x*wm.height + y
		t1.append(ws[0].tiles[i])
		t2.append(ws[1].tiles[i])
	for y in range(wm.height):
		i = x*wm.height + y
		t1.append(ws[2].tiles[i])
		t2.append(ws[3].tiles[i])
w.tiles = t1 + t2


for i in range(len(ws)):
	x = 0
	y = 0
	if i == 1 or i == 3:
		x = wm.width
	if i == 2 or i == 3:
		y = wm.height
	
	for chest in ws[i].chests:
		chest.x += x
		chest.y += y
		w.chests.append(chest)
	for sign in ws[i].signs:
		sign.x += x
		sign.y += y
		w.signs.append(sign)
	for npc in ws[i].npcs:
		npc.x += x * 16
		npc.y += y * 16
		npc.home_x += x
		npc.home_y += y
		w.npcs.append(npc)
	for te in ws[i].tile_entities:
		te.x += x
		te.y += y
		w.tile_entities.append(te)
	for plate in ws[i].weighted_pressure_plates:
		w.weighted_pressure_plates.append((plate[0] + x, plate[1] + y))
	for room in ws[i].npc_rooms:
		w.npc_rooms.append((room[0], room[1] + x, room[2] + y))

w.bestiary_kills = wm.bestiary_kills
w.bestiary_sights = wm.bestiary_sights
w.bestiary_chats = wm.bestiary_chats
w.creative_powers = wm.creative_powers


write_world_file(w.name, w)



"""
image = Image.new("RGB", (width, height))
ctx = ImageDraw.Draw(image)
for x in range(width):
	for y in range(height):
		ctx.point((x, y), getTileInfo(tiles[x*height + y])[1])
image.save("map.png")
"""




