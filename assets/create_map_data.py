import json

global this_map
global spritesheets
spritesheets = {}


def Constraint(TYPE,max_bias,max_force,*args):
    return {
        "type":TYPE,
        "max_bias":max_bias,
        "max_force":max_force,
        "args":args
            }
    

def Object(TYPE,pos,_dir,txr,anchored,col=(20,20,20),ct=-1,mass=-1,shape={"shape":"rectangle","size":(30,20),"friction":0.1},constraints=[],ID=-1):
    global this_map
    parent = this_map["Objects"]
    parent.append({
            "type":TYPE,
            "ID":ID,
            "position": pos,
            "direction": _dir,
            "mass":mass,
            "color": col,
            "texture": txr,
            "anchored": anchored,
            "collision_type":ct,
            "shape":shape,
            "constraints":constraints
            })

def SpriteSheet(name,sprite_sheet_file):
    global spritesheets
    spritesheets[name] = sprite_sheet_file
    

def Texture(name,location,ss):
    global this_map
    parent = this_map["Textures"]
    parent[name] = (ss,location)

def TexturePack(name,info,ss):
    sx,sy,w,h,col,row = info
    global this_map
    parent = this_map["Texture Packs"]
    _textures = []
    for i in range(col):
        for j in range(row):
            _textures.append((sx+i*w,sy+j*h))
    parent[name] = (ss,(w,h),_textures)

def NewMap(name,NMP,all_maps,game_mode):
    all_maps.append({"Map Name":name,
            "No Moving Parts":True,
            "Thumbnail":None,
            "Game Mode": game_mode,
            "Textures":{},
            "Objects":[],
            "Texture Packs":{}
            })
    global this_map
    this_map = all_maps[-1]

def maps(all_maps):
    global spritesheets
    maps_data = {}
    maps_data["Spritesheets"] = spritesheets
    for _map in all_maps:
        maps_data[_map["Map Name"]] = _map
    _map
    return maps_data


all_maps = []

#Actions here
#Automatically adds objects and textures the the last created map


SpriteSheet("Background","assets\\tank_game_background.png")
SpriteSheet("Sprites","assets\\tank_game_sprites.png")
SpriteSheet("Tanks","assets\\tanks.png")
SpriteSheet("Decors","assets\\decors.png")
SpriteSheet("Projectiles","assets\\projectiles.png")
SpriteSheet("Font","assets\\font.png") #Add font
SpriteSheet("Sandbox1","assets\\sandbox.png")

NewMap("desert1",True,all_maps,1)

Texture("sandbox1",(0,0,34,20),"Sandbox1")
Texture("background_tile", (1408,384,64,64),"Background")

TexturePack("Projectiles", (0,0,19,39,8,1),"Projectiles")
TexturePack("Tanks", (0,40,42,45,9,1),"Tanks")

box_constraints = [
    Constraint("PivotJoint",0,20,(0,0),(0,0)),
    Constraint("GearJoint" ,0,100, 0, 1)
    ]


ox,oy = 20,220
space = 1
WIDTH,HEIGHT = 1600,900
w,h = 6,6
def copy_4_sides(incx,incy,ox,oy,_dir):
    Object("map_object",[ox+incx,oy+incy],_dir,"sandbox1",False,mass=50,constraints=box_constraints.copy(),shape={"shape":"rectangle","size":(34,30),"friction":0.01},ct=5)
    Object("map_object",[ox+incx,HEIGHT-oy-incy],_dir,"sandbox1",False,mass=50,constraints=box_constraints.copy(),shape={"shape":"rectangle","size":(34,30),"friction":0.01},ct=5)
    Object("map_object",[WIDTH-ox-incx,oy+incy],_dir,"sandbox1",False,mass=50,constraints=box_constraints.copy(),shape={"shape":"rectangle","size":(34,30),"friction":0.01},ct=5)
    Object("map_object",[WIDTH-ox-incx,HEIGHT-oy-incy],_dir,"sandbox1",False,mass=50,constraints=box_constraints.copy(),shape={"shape":"rectangle","size":(34,30),"friction":0.01},ct=5)

for i in range(w):
    copy_4_sides(i*(34+space),0,ox,oy,0)
ox,oy = 216,9
for i in range(h):
    copy_4_sides(0,i*(34+space),ox,oy,90)
ox,oy = 536,9
for i in range(h):
    copy_4_sides(0,i*(34+space),ox,oy,90)
ox,oy = 564, 208
for i in range(4):
    copy_4_sides(i*(34+space),0,ox,oy,0)

Object("player",[  60, 60],0,"Tanks",False,mass=100,shape={"shape":"circle","radius":21},ID=1,ct=11)
Object("player",[  60,740],0,"Tanks",False,mass=100,shape={"shape":"circle","radius":21},ID=2,ct=12)
Object("player",[1340, 60],0,"Tanks",False,mass=100,shape={"shape":"circle","radius":21},ID=3,ct=13)
Object("player",[1340,740],0,"Tanks",False,mass=100,shape={"shape":"circle","radius":21},ID=4,ct=14)
Object("player",[ 700, 60],0,"Tanks",False,mass=100,shape={"shape":"circle","radius":21},ID=5,ct=15)
Object("player",[ 700,740],0,"Tanks",False,mass=100,shape={"shape":"circle","radius":21},ID=6,ct=16)

#Map Info ends


json_string = json.dumps(maps(all_maps))

with open("maps.json","w") as output_file:
    output_file.write(json_string)
