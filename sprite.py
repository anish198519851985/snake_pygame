import pygame
import copy
from pygame.locals import *

class segment(pygame.sprite.Sprite):
  def __init__(self, color, rect, sprite=None):
    super().__init__()
    self.image = pygame.Surface([rect.width, rect.height])
    self.image.fill(color)
    self.rect = rect
    self.nextsprite = sprite
    self.prev_rect = None

  def move(self, dx, dy, direction=None):
    if self.nextsprite != None:
      self.prev_rect = self.rect
      self.rect = self.nextsprite.prev_rect
    else:
      self.prev_rect = self.rect		
      if direction == K_UP:	
        self.rect = self.rect.move(0, -self.rect.width)
      elif direction == K_DOWN:		
        self.rect = self.rect.move(0, self.rect.width)
      elif direction == K_LEFT:
        self.rect = self.rect.move(-self.rect.width, 0)
      elif direction == K_RIGHT:
        self.rect = self.rect.move(self.rect.width, 0)

  def update(self, *args):
    self.rect = self.rect
		
class food_segment(segment):
  def move(self, dimension):
    self.rect = dimension
