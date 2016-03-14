# -*- coding: utf-8 -*-
#Wizards Magic
#Copyright (C) 2011-2014  https://code.google.com/p/wizards-magic/
#This program is free software; you can redistribute it and/or
#modify it under the terms of the GNU General Public License
#as published by the Free Software Foundation; either version 2
#of the License, or (at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program; if not, write to the Free Software
#Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
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
