from tank_game.loader import Loader
import pygame
import pymunk
import pymunk.pygame_util
from math import floor,ceil

# Game Modes
# 1-> Last one standing
# 2-> Highest kill
# 3-> Capture

global selected
selected = None

class EditorObject:
    def __init__(self,pos,_dir,texture,editor):
        self.pos = pos
        self.dir = _dir
        self.grid = 4
        self.texture = texture
        self.to_grid()
    def to_grid(self):
        x,y = self.pos
        x = round(x/self.grid)*self.grid
        y = round(y/self.grid)*self.grid
        self.pos = (x,y)
    def update(self,pos):
        self.pos = pos
        self.to_grid()
    def render(self,display):
        t = pygame.transform.rotate(self.texture,self.dir)
        rect = t.get_rect(center=self.pos)
        display.blit(t,rect)
    def rotate(self,_dir):
        self.dir += _dir

class MapEditor:
    def __init__(self,Game):
        self.Game = Game
        self.grid_size = 8
        self.selected = None
        self.sandbox = self.Game.textures["sandbox1"]
        self.objects = []
    def place_object(self,pos,_dir=0):
        global selected
        x,y = pos
        selected = EditorObject((x,y),_dir,self.sandbox,self)
    def remove_object():pass
    def rotate(self,_dir):
        global selected
        if selected:
            selected.rotate(_dir)
    def update(self,pos):
        global selected
        if selected:
            selected.update(pos)
    def release(self):
        global selected
        self.objects.insert(0,selected)
        pos,_dir = selected.pos,selected.dir
        print(pos,dir)
        selected = None
        self.place_object(pos,_dir)

class Game():
    def __init__(self,player_count,map_filename,map_name,display):
        self.frame = 0
        self.player_count = player_count
        self.display = display

        self.space = pymunk.Space()
        self.space.sleep_time_threshold = 1
        print(map_name)
        self.Load(map_filename,map_name)

        self.editor = MapEditor(self)
        
    def update(self,inputs,delta):
        for player in self.Players:
            player.update(inputs,delta)
        #self.space.step(delta)
        for obj in self.DynamicObjects:
            obj.update()
        
    def render(self,display):
        display.blit(self.background,(0,0))
        for obj in self.StaticObjects:
            obj.render(display)
        for obj in self.DynamicObjects:
            obj.render(display)
        for player in self.Players:
            player.render(display)
        global selected
        if selected:
            selected.render(display)
        for o in self.editor.objects:
            o.render(display)
        
    def run_frame(self,display,inputs,delta,do=None):
        self.update(inputs,delta)
        self.render(display)
        for _ in range(4):
            self.space.step(0.2)
        #self.space.step(delta)
        #self.space.debug_draw(do) #EMERGENCY DEBUG
        self.frame+=1

    def Load(self,map_filename,map_name):
        l = Loader(self)
        l.load(map_filename,map_name)
        l.destroy()

