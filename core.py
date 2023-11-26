import sys
import pygame
from pygame.locals import *
from time import time as now

# Mini Games Library
sys.path.append("./mini_games")
from minigame_manager import get_minigame
from load_settings import load_input_mask


pygame.init()
fpsClock = pygame.time.Clock()

# Globals
FPS = 60
BG_COLOR = (40,40,40)
TITLE = "234 player games"
WIDTH, HEIGHT = 1400,800
SCALE_FACTOR = 0.5
screen = pygame.display.set_mode((WIDTH, HEIGHT),RESIZABLE)
pygame.display.set_caption(TITLE)

input_mask = load_input_mask("Q_Keyboard",6)

game = get_minigame(1,2,"assets/maps.json","desert1",screen)

def extract_inputs(pressed):
  input_list = []
  for key in input_mask:
    input_list.append(pressed[key])
  return tuple(input_list)

#DEBUG
import pymunk
do = pymunk.pygame_util.DrawOptions(screen) 

start=now()
# Game loop.
while True:
  SIZE = pygame.display.get_surface().get_size()
  pressed = pygame.key.get_pressed()
  inputs = extract_inputs(pressed)
  screen.fill(BG_COLOR)
  game.run_frame(screen,inputs,(now()-start)*20,SIZE,do=do)
  start=now()
  pygame.display.flip()

  for event in pygame.event.get():
    if event.type == QUIT:
      pygame.quit()
      sys.exit()
    if event.type == "No":
      if event.key == K_a:
        game.editor.place_object(pygame.mouse.get_pos())
      if event.key == K_f:
        game.editor.release()
      if event.key == K_r:
        game.editor.rotate(45)
  game.editor.update(pygame.mouse.get_pos())
  fpsClock.tick(FPS)
