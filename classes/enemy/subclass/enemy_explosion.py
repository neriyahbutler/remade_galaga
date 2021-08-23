from classes.enemy.subclass.object import Object

import pygame

explosions = [pygame.image.load("C:/Users/neriy/Documents/GitHub Code/remadegalaga/sprites/enemy/enemy_death/exp1.gif"),
pygame.image.load("C:/Users/neriy/Documents/GitHub Code/remadegalaga/sprites/enemy/enemy_death/exp2.png"),
pygame.image.load("C:/Users/neriy/Documents/GitHub Code/remadegalaga/sprites/enemy/enemy_death/exp3.png"),
pygame.image.load("C:/Users/neriy/Documents/GitHub Code/remadegalaga/sprites/enemy/enemy_death/exp4.png"),
pygame.image.load("C:/Users/neriy/Documents/GitHub Code/remadegalaga/sprites/enemy/enemy_death/exp5.png")]

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