import sys
import pygame
from pygame.locals import *
from time import time as now

# Mini Games Library
sys.path.append("./mini_games")
from minigame_manager import get_minigame
from load_settings import load_input_mask

class App:
  def __init__(self):
    pygame.init()
    self.fpsClock = pygame.time.Clock()

    # Globals
    self.FPS = 60
    self.BG_COLOR = (40,40,40)
    self.TITLE = "234 player games"
    self.WIDTH, self.HEIGHT = 1400,800
    self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT),RESIZABLE)
    self.frame = 0
    self.running = True
    self.inputs = None
    pygame.display.set_caption(self.TITLE)
    self.input_mask = load_input_mask("Q_Keyboard",6)
    self.tank_game = get_minigame(1,2,"assets/maps.json","desert1",self.screen)

  def extract_inputs(self,pressed):
    input_list = []
    for key in self.input_mask:
      input_list.append(pressed[key])
    self.inputs = tuple(input_list)

  def HandleInputs(self):
    pressed = pygame.key.get_pressed()
    self.extract_inputs(pressed)

  def RenderFrame(self):
    SIZE = pygame.display.get_surface().get_size()
    self.screen.fill(self.BG_COLOR)
    self.tank_game.RunFrame(self.screen,self.inputs,SIZE)
    pygame.display.flip()
    
  def HandleEvents(self):
    for event in pygame.event.get():
      if event.type == QUIT:
        pygame.quit()
        sys.exit()
      if event.type == "No":
        if event.key == K_a:
          self.tank_game.editor.place_object(pygame.mouse.get_pos())
        if event.key == K_f:
          self.tank_game.editor.release()
        if event.key == K_r:
          self.tank_game.editor.rotate(45)

  def Run(self):
    # Game loop.
    while self.running:
      self.HandleInputs()
      self.RenderFrame()
      self.HandleEvents()
      #self.tank_game.editor.update(pygame.mouse.get_pos())
      self.fpsClock.tick(self.FPS)
      self.frame+=1

if __name__ == "__main__":
  ThisApp = App()
  ThisApp.Run()