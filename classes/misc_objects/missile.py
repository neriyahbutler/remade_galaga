import os

from classes.misc_objects.subclass.object import Object

import pygame

base_path = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(base_path, "../../sprites/player/missile.gif")

missile = pygame.image.load(image_path)

class Missile(Object):
    def __init__(self, gunship_pos):
        self.x = gunship_pos[0]
        self.y = gunship_pos[1]
        self.speed = 10

    def draw(self, win):
        self.y -= self.speed
        win.blit(missile, (self.x, self.y))

    def get_pos(self):
        return (self.x, self.y)