from tank_game.objects import StaticObject,DynamicObject,Player
import json
import pygame
from math import ceil

def projectile_on_hit(arbiter,space,data):
    s = arbiter.shapes
    ct1,ct2 = s[0].collision_type,s[1].collision_type
    p,hit = s[0].owner,s[1].owner
    if ct1 == ct2 == 6 or hit is p.owner:return #Two projectiles colliding or colliding with shooter
    p.owner.remove_projectile(p)
    if hit.hit(): #Projectile hit a player
        p.owner.kill_counter += 1
    #Explosion animation

class Loader:
    def __init__(self,Game):
        self.Game = Game
    def destroy(self):
        del(self)

    def grab_image(self,sprite_sheet, x, y, width, height):
        image = pygame.Surface((width, height))
        image.blit(sprite_sheet, (-x, -y))
        return image

    def load_spritheets(self):
        ss_dict = {}
        Spritesheets = self.maps["Spritesheets"]
        for ss_name in Spritesheets:
            ss_dict[ss_name] = pygame.image.load(Spritesheets[ss_name])
        self.ss_dict = ss_dict

    def load_textures(self):
        data = self.map_data["Textures"]
        textures = {}
        for name in data.keys():
            print(data[name])
            ss,info = data[name]
            texture = self.grab_image(self.ss_dict[ss],info[0],info[1],info[2],info[3])
            textures[name] = texture
            texture.set_colorkey((0,255,0))
        self.Game.textures = textures

    def load_texturepacks(self):
        data = self.map_data["Texture Packs"]
        self.Game.TexturePacks = {}
        for name in data.keys():
            ss,size,tiles = data[name]
            t_list = []
            for pos in tiles:
                texture = self.grab_image(self.ss_dict[ss],pos[0],pos[1],size[0],size[1])
                texture.set_colorkey((0,255,0))
                t_list.append(texture)
            self.Game.TexturePacks[name] = t_list

    def load_background(self):
        w,h = self.Game.display.get_size()
        bg = pygame.Surface((w,h))
        bg_tile = self.Game.textures["background_tile"]
        tw,th = bg_tile.get_size()
        for i in range(ceil(w/tw)):
            for j in range(ceil(h/th)):
                bg.blit(bg_tile,(i*tw,j*th))
        self.Game.background = bg


    def load_map(self):
        objects_data  = self.map_data["Objects"]

        DynamicObjects= []
        StaticObjects = []
        Players = []
        
        for obj in objects_data:
            if obj["type"] == "player":
                Players.append(Player(obj,self.Game))
            else:
                if obj["anchored"]:
                    StaticObjects.append(StaticObject(obj,self.Game))
                else:
                    DynamicObjects.append(DynamicObject(obj,self.Game))
        self.Game.Players = Players
        self.Game.DynamicObjects = DynamicObjects
        self.Game.StaticObjects = StaticObjects

    def load_file(self,map_file,map_name):
        with open(map_file,"r") as outfile:
            maps = json.load(outfile)
        self.map_data = maps[map_name]
        self.maps = maps
        self.Game.MapName = self.map_data["Map Name"]
        self.Game.Thumbnail = self.map_data["Thumbnail"]
        self.Game.GameMode = self.map_data["Game Mode"]

    def load(self,map_filename,map_name):
        self.load_file(map_filename,map_name)
        self.load_spritheets()
        self.load_textures()
        self.load_texturepacks()
        self.load_background()
        self.load_map()
        self.load_handlers()

    def load_handlers(self):
        self.Game.projectile_handler = self.Game.space.add_wildcard_collision_handler(6)
        self.Game.projectile_handler.post_solve = projectile_on_hit

