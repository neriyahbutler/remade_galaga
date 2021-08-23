from classes.enemy.subclass.enemy_explosion import Explosion
from math import exp
from classes.enemy.enemy import Enemy

import pygame
import random

bee = [
        pygame.image.load("C:/Users/neriy/Documents/GitHub Code/remadegalaga/sprites/enemy/bee/bee1.png"), 
        pygame.image.load("C:/Users/neriy/Documents/GitHub Code/remadegalaga/sprites/enemy/bee/bee2.png")
    ]

bee[0] = pygame.transform.scale(bee[0], (30, 30))
bee[1] = pygame.transform.scale(bee[1], (30, 30))

bee_sfx1 = pygame.mixer.Sound("C:/Users/neriy/Documents/GitHub Code/remadegalaga/galaga_sfx/05 Zako Stricken.mp3")

class Bee(Enemy):
    def draw(self, win):
        for obj in self.missile_buffer:
            obj.draw(win)
        if self.health > 0:
            if self.prev_draw_time == 0 or pygame.time.get_ticks() - self.prev_draw_time > 500:
                if self.iter < 1:
                    self.iter += 1
                else:
                    self.iter = 0
                self.prev_draw_time = pygame.time.get_ticks()
            win.blit(bee[self.iter], (self.x, self.y))

    def dive(self, win):
        random_int = random.randint(1, 11)
        choice = random_int % 2

        # if not self.initial_dive:
        #     self.generate_bee_curves(choice, gunship)
        self.adjust_position()

    def lower_health(self):
        Enemy.lower_health(self)
        if self.health == 0:
            bee_sfx1.play()
