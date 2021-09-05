from classes.misc_objects.subclass.object import Object

import sys

import os

from os.path import dirname, abspath
d = dirname(dirname(dirname(abspath(__file__))))
sys.path.append(d)

base_path = os.path.dirname(os.path.abspath(__file__))

import pygame

image_path_1 = os.path.join(base_path, "../../sprites/player/death/1.png")
image_path_2 = os.path.join(base_path, "../../sprites/player/death/2.png")
image_path_3 = os.path.join(base_path, "../../sprites/player/death/3.png")
image_path_4 = os.path.join(base_path, "../../sprites/player/death/4.png")

explosions = [
pygame.image.load(image_path_1),
pygame.image.load(image_path_1),
pygame.image.load(image_path_1),
pygame.image.load(image_path_1),

pygame.image.load(image_path_2),
pygame.image.load(image_path_2),
pygame.image.load(image_path_2),
pygame.image.load(image_path_2),

pygame.image.load(image_path_3),
pygame.image.load(image_path_3),
pygame.image.load(image_path_3),
pygame.image.load(image_path_3),

pygame.image.load(image_path_4),
pygame.image.load(image_path_4),
pygame.image.load(image_path_4),
pygame.image.load(image_path_4)]

explosions[0] = pygame.transform.scale(explosions[0], (30, 30))
explosions[1] = pygame.transform.scale(explosions[1], (30, 30))
explosions[2] = pygame.transform.scale(explosions[2], (30, 30))
explosions[3] = pygame.transform.scale(explosions[3], (30, 30))
explosions[4] = pygame.transform.scale(explosions[4], (30, 30))
explosions[5] = pygame.transform.scale(explosions[5], (30, 30))
explosions[6] = pygame.transform.scale(explosions[6], (30, 30))
explosions[7] = pygame.transform.scale(explosions[7], (30, 30))
explosions[8] = pygame.transform.scale(explosions[8], (30, 30))
explosions[9] = pygame.transform.scale(explosions[9], (30, 30))
explosions[10] = pygame.transform.scale(explosions[10], (30, 30))
explosions[11] = pygame.transform.scale(explosions[11], (30, 30))
explosions[12] = pygame.transform.scale(explosions[12], (30, 30))
explosions[13] = pygame.transform.scale(explosions[13], (30, 30))
explosions[14] = pygame.transform.scale(explosions[14], (30, 30))
explosions[15] = pygame.transform.scale(explosions[15], (30, 30))


class PlayerExplosion(Object):
    index = 0

    def __init__(self, enemy_pos):
        self.x = enemy_pos[0]
        self.y = enemy_pos[1]

    def get_index(self):
        return self.index

    def draw(self, win):
        if self.index < 16:
            win.blit(explosions[self.index], (self.x, self.y))
            self.index += 1