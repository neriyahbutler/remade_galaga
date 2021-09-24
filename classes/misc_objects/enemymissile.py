import os

from classes.misc_objects.subclass.object import Object
import pygame

pygame.init()

base_path = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(base_path, "../../sprites/enemy/enemy_missile/enemy_missile.png")

font_path = os.path.join(base_path, "../../font/Joystix.ttf")
font = pygame.font.Font(font_path, 10)

enemy_missile = pygame.image.load(image_path)

class EnemyMissile(Object):
    def __init__(self, shooter_pos, target):
        self.x = shooter_pos[0]
        self.y = shooter_pos[1]
        self.target = target

        self.slope = (target.y - self.y)/(target.x - self.x)
        self.slope = abs(self.slope)
        self.b = self.y - self.slope * self.x

    def draw(self, win, pauseGame):
        if not pauseGame:
            if self.slope > 20:
                self.x += 0.01 * 40
            elif 10 < self.slope < 20:
                self.x += 0.015 * 40
            elif 5 < self.slope < 10:
                self.x += 0.018 * 40
            else:
                self.x += 0.02 * 40
            self.y += 0.1 * 40
        enemy_details_1 = font.render("Slope: %s"%(str(self.slope)), 1, (255, 255, 255))
        enemy_details_2 = font.render("X: %s"%(str(self.x)), 1, (255, 255, 255))
        enemy_details_3 = font.render("Y: %s"%(str(self.y)), 1, (255, 255, 255))

        win.blit(enemy_details_1, (self.x + 10, self.y - 30))
        win.blit(enemy_details_2, (self.x + 10, self.y - 20))
        win.blit(enemy_details_3, (self.x + 10, self.y - 10))
        win.blit(enemy_missile, (self.x, self.y))

    def get_pos(self):
        return (self.x, self.y)

    def get_target(self):
        return self.target
