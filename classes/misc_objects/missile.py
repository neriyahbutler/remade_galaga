from classes.misc_objects.subclass.object import Object

import pygame

missile = pygame.image.load("C:/Users/neriy/Documents/GitHub Code/remadegalaga/sprites/player/missile.gif")

class Missile(object):
    def __init__(self, gunship_pos):
        self.x = gunship_pos[0]
        self.y = gunship_pos[1]
        self.speed = 10

    def draw(self, win):
        self.y -= self.speed
        win.blit(missile, (self.x, self.y))

    def get_pos(self):
        return (self.x, self.y)