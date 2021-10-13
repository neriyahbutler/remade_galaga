import os

from classes.enemy.subclass.enemy_explosion import Explosion
from math import exp
from classes.enemy.enemy import Enemy

import pygame
import random

base_path = os.path.dirname(os.path.abspath(__file__))

image_path_1 = os.path.join(base_path, "..\..\sprites/enemy/bee/bee1.png")
image_path_2 = os.path.join(base_path, "..\..\sprites/enemy/bee/bee2.png")

bee = [
        pygame.image.load(image_path_1), 
        pygame.image.load(image_path_2)
    ]

bee[0] = pygame.transform.scale(bee[0], (30, 30))
bee[1] = pygame.transform.scale(bee[1], (30, 30))

sfx_path = os.path.join(base_path, "..\..\galaga_sfx/wav/05 Zako Stricken.wav")

bee_sfx1 = pygame.mixer.Sound(sfx_path)

class Bee(Enemy):
    def fire(self, target):
        super(Bee, self).fire(target)

    def draw(self, win, pauseGame):
        for obj in self.missile_buffer:
            obj.draw(win, pauseGame)
            if obj.y > 500:
                self.missile_buffer.pop(self.missile_buffer.index(obj))
        if self.health > 0:
            if self.prev_draw_time == 0 or pygame.time.get_ticks() - self.prev_draw_time > 500:
                if self.iter < 1:
                    self.iter += 1
                else:
                    self.iter = 0
                self.prev_draw_time = pygame.time.get_ticks()
            win.blit(bee[self.iter], (self.x, self.y))

    def dive(self, win, target_pos = None):       
        self.adjust_position()
        if self.y > 500:
            self.x = self.init_pos[0]
            self.y = self.init_pos[1] - 200
            self.moving_to_init_pos = True
        if self.moving_to_init_pos:
            self.move_to_init_pos()
            if self.x == self.init_pos[0] and self.y == self.init_pos[1]:
                self.moving_to_init_pos = False
                self.status = ""
            
    def lower_health(self):
        Enemy.lower_health(self)
        if self.health == 0:
            bee_sfx1.play()
