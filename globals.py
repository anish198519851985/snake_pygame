try: 
    import pygame
    yes_pygame = True
except ImportError:
    yes_pygame = False
import os
from os.path import join
from random import randint, choice

current_folder = os.path.dirname(os.path.abspath(__file__))
if yes_pygame: 
    pygame.font.init()
    font = pygame.font.Font(current_folder+"/misc/Neocyr.ttf", 20)
    font2 = pygame.font.Font(current_folder+"/misc/Domestic_Manners.ttf", 20)

def playmusic():
  pygame.mixer.music.play(0, 0.0)

def set_element_sound(element):
    if element == 'hisss':
      sound = pygame.mixer.Sound('pickup.wav')
      sound.play()

    elif element == 'background':
      musics = os.listdir(current_folder+'/misc/sounds/background')
      music = choice(musics) 
      pygame.mixer.music.load(join(current_folder+'/misc/sounds/background', music))
		
    else:
      print("nothing is implemented for this")
