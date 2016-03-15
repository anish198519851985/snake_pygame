'''1. Create snake -- extend snake + initial snake creation
2. Update snake position - when key is pressed
3. Collision detection - with self, wall and food
4. create food 
5. key handling with certain key is pressed - reset and quit along with resume
'''

import random
import pygame
import os
import time
import globals
import copy
from pygame.locals import *
import sprite
from random import randint, choice
import threading
current_folder = os.path.dirname(os.path.abspath(__file__))

directions = [KEYDOWN, K_DOWN, K_LEFT, K_RIGHT]

class dimensions:
  def __init__(self, width, height):
    self.width = width
    self.height = height
  
class food_shape(dimensions):
  def __init__(self, color, width, height, position):
    self.color = pygame.Color(color)
    self.position = position
    super().__init__(width, height)

class snake_shape(food_shape):
  def __init__(self, speed, parts, direction, color, width, height, position, part_position):
    self.speed = speed
    self.parts = parts
    self.direction = direction
    self.part_position = part_position
    super().__init__(color, width, height, position)

class snake_game():
  fps = 20
  magic_keys = [K_r, K_q, K_z, K_ESCAPE]
  allowed_direction = [K_LEFT, K_RIGHT, K_UP, K_DOWN]
  allowed_keys = magic_keys + allowed_direction

  #make sure to pass some sensible values here as checking is up to you
  def __init__(self, window, snake, food):
    self.window = window[1]
    self.window_color = pygame.Color(window[0])
    self.reset_game(window, snake, food)
    super().__init__()

  def reset_game(self, window, snake, food):

    self.snake = snake
    self.create_snake()
    self.running = True

    self.food = food
		
    self.surface = pygame.display.set_mode((self.window.width, self.window.height), pygame.HWSURFACE)		
    pygame.display.set_caption('snaking')
    self.background_img = pygame.image.load(os.path.join("images", "background.jpg")).convert()

    self.clock = pygame.time.Clock()
    self.score = 0
    self.font_color = pygame.Color("black")  

  def create_snake(self):
    self.sprites = pygame.sprite.OrderedUpdates()		
    random_snake = self.random_rect(self.snake.width, self.snake.height) 		
    self.snake.part_position.append(sprite.segment(self.snake.color, random_snake, None))
    self.sprites.add(self.snake.part_position[0])
    for i in range(1, self.snake.parts):
      self.snake.part_position.append(sprite.segment(self.snake.color, self.snake.part_position[i-1].rect, self.snake.part_position[i-1]))
      self.snake.part_position[i].rect = self.snake.part_position[i-1].rect.move(-self.snake.width, 0)			
      self.sprites.add(snake.part_position[i])			
			
  def check_wall(self):
    x, y = self.snake.part_position[0].rect.x, self.snake.part_position[0].rect.y
    if x >= self.window.width or y >= self.window.height or x < 0 or y < 0:
      return True
    return False

  def fill_background(self):
    for x in range(0, self.window.width, self.background_img.get_rect().width):
      for y in range(0, self.window.height, self.background_img.get_rect().height):
        self.surface.blit(self.background_img, (x, y))
	
  def on_key_event(self):
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        self.terminate()
      if event.type == KEYDOWN:				
        if event.key == K_r:
          window, snake, food = init_game()
          self.reset_game(window, make_snake(), make_food())
          return event.key
        if event.key == K_q:
          self.terminate()					
        else:
          return event.key if event.key in self.allowed_keys else self.snake.direction
    return self.snake.direction
			
  def create_food(self):
    self.spritefood = pygame.sprite.Group()
    random_food = self.random_rect(self.snake.width, self.snake.height)		
    self.food_sprite = sprite.food_segment(self.food.color, random_food)
    self.spritefood.add(self.food_sprite)

  def random_rect(self, w, h):
    x = random.randint(h, (self.window.width - max(w, h)))
    y = random.randint(0, self.window.height-h)		
    return Rect(x, y, w, h)	

  def allow_direction_change(self, current_direction):
    if self.snake.direction == K_LEFT and current_direction == K_RIGHT:
      return False
    elif self.snake.direction == K_RIGHT and current_direction == K_LEFT:
      return False
    elif self.snake.direction == K_UP and current_direction == K_DOWN:
      return False
    elif self.snake.direction == K_DOWN and current_direction == K_UP:
      return False
    return True
		
  def update_positions(self, current_direction):
    if not self.allow_direction_change(current_direction):
      return
    for i in range(0, self.snake.parts):
      self.snake.part_position[i].move(self.snake.width, self.snake.height, current_direction) 
    if current_direction in self.allowed_direction:
      self.snake.direction = current_direction	

  def check_collision_with_self(self):
    pass

  def check_collision_with_food(self):
    hit = pygame.sprite.spritecollide(self.food_sprite, self.sprites, False)
    if len(hit) >= 1:
      random_food = self.random_rect(self.snake.width, self.snake.height) 
      self.food_sprite.move(random_food)
      self.score += 1
      self.play_music("hisss")
			
  def play_music(self, type):
    globals.set_element_sound(type)
    globals.playmusic()		

  def show_message(self):
    while True:	
      self.surface.fill(pygame.Color("black"))
      message = "press Q:quit"
      message += "press R:restart"
      message_feed = globals.font.render(message, True, self.snake.color)
      self.surface.blit(message_feed, (10, 10))
      pygame.display.update()
      if self.on_key_event() in self.magic_keys:
        break

  def show_score(self):
    text_score = globals.font.render(("Score:"+ str(self.score)), True, self.snake.color)
    self.surface.blit(text_score, (20, 30))
		
  def terminate(self):
    pygame.quit()			
    exit()
		
  def run(self):
    self.create_food()
    self.show_score()
    while self.running:
      self.clock.tick(self.fps)
      self.fill_background()
      direction = self.on_key_event()
      if direction in self.allowed_direction:
        self.update_positions(direction)			
      self.check_collision_with_food()
      self.sprites.update()			
      self.show_score()
      self.sprites.draw(self.surface)
      self.spritefood.draw(self.surface)
      if self.check_wall():
        self.show_message()
      if not pygame.mixer.music.get_busy():
        self.play_music('background')
      pygame.display.update()

def make_snake():
  return snake_shape(1, 5, K_RIGHT, "blue", 10, 10, (0, 0), [])

def make_food():
  return food_shape("red", 10, 10, (0, 0))

def init_game():
  window=("red", dimensions(size[0], size[1]))
  snake = make_snake()
  food = make_food()
  return (window, snake, food)	

pygame.init()
size = (400, 400)
window, snake, food = init_game()
s = snake_game(window, snake, food)
s.run()
