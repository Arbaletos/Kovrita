import random, pygame, sys
from pygame.locals import *

pygame.init()

FPS = 30
fpsClock = pygame.time.Clock()


screen = pygame.display.set_mode((800,600))

while True: # the main game loop
  for event in pygame.event.get():
    if event.type == QUIT:
      pygame.quit()
      sys.exit()
  pygame.display.update()
  fpsClock.tick(FPS)
