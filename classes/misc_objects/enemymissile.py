from classes.misc_objects.subclass.object import Object

import pygame

enemy_missile = pygame.image.load("C:/Users/neriy/Documents/GitHub Code/remadegalaga/sprites/enemy/enemy_missile/enemy_missile.png")

class EnemyMissile(Object):
    def __init__(self, shooter_pos, slope):
        self.x = shooter_pos[0]
        self.y = shooter_pos[1]

        self.slope = abs(slope)
        self.b = self.y - self.slope * self.x
        print(self.slope)

    def draw(self, win):
        win.blit(enemy_missile, (self.x, self.y))
        if self.slope > 20:
            self.x += 0.2
        elif 10 < self.slope < 20:
            self.x += 1
        elif 5 < self.slope < 10:
            self.x += 1.5
        else:
            self.x += 2
        self.y = self.x * self.slope + self.b