import os

from classes.misc_objects.subclass.object import Object
import pygame

base_path = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(base_path, "../../sprites/enemy/enemy_missile/enemy_missile.png")

enemy_missile = pygame.image.load(image_path)

class EnemyMissile(Object):
    def __init__(self, shooter_pos, target):
        self.x = shooter_pos[0]
        self.y = shooter_pos[1]

        self.slope = (target.y - self.y)/(target.x - self.x)
        self.slope = abs(self.slope)
        self.b = self.y - self.slope * self.x

    def draw(self, win):
        if self.slope > 20:
            self.x += 0.01
        elif 10 < self.slope < 20:
            self.x += 0.015
        elif 5 < self.slope < 10:
            self.x += 0.018
        else:
            self.x += 0.02
        self.y += 0.1
        win.blit(enemy_missile, (self.x, self.y))
