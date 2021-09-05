from classes.enemy.subclass.object import Object

import sys
import os

from os.path import dirname, abspath
d = dirname(dirname(dirname(abspath(__file__))))
sys.path.append(d)

import pygame

base_path = os.path.dirname(os.path.abspath(__file__))

image_path_1 = os.path.join(base_path, "../../../sprites/enemy/enemy_death/exp1.png")
image_path_2 = os.path.join(base_path, "../../../sprites/enemy/enemy_death/exp2.png")
image_path_3 = os.path.join(base_path, "../../../sprites/enemy/enemy_death/exp3.png")
image_path_4 = os.path.join(base_path, "../../../sprites/enemy/enemy_death/exp4.png")
image_path_5 = os.path.join(base_path, "../../../sprites/enemy/enemy_death/exp5.png")


explosions = [pygame.image.load(image_path_1),
pygame.image.load(image_path_2),
pygame.image.load(image_path_3),
pygame.image.load(image_path_4),
pygame.image.load(image_path_5)]

explosions[0] = pygame.transform.scale(explosions[0], (30, 30))
explosions[1] = pygame.transform.scale(explosions[1], (30, 30))
explosions[2] = pygame.transform.scale(explosions[2], (30, 30))
explosions[3] = pygame.transform.scale(explosions[3], (30, 30))
explosions[4] = pygame.transform.scale(explosions[4], (30, 30))

class Explosion(Object):
    index = 0

    def __init__(self, enemy_pos):
        self.x = enemy_pos[0]
        self.y = enemy_pos[1]

    def get_index(self):
        return self.index

    def draw(self, win):
        if self.index < 5:
            win.blit(explosions[self.index], (self.x, self.y))
            self.index += 1