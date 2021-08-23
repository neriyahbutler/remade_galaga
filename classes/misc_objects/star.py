import random

import pygame

class Star(object):
    colors = ["red", "green", "blue", "white"]

    def __init__(self, layer, width, height):
        self.timer = 0

        self.visible = False
        self.scroll = True

        self.width = width
        self.height = height

        self.prevFlickerTime = 0
        self.flickerCooldown = 300
        self.flickerSpeed = 0.15 * (random.randint(0, 1000) / 10000) * 0.45

        self.color = (0, 0, 0)

        self.scrollSpeed = 2

        if layer == 0:
            self.color = (255, 255, 255)
        if layer == 1:
            self.color = (255, 0, 0)
        if layer == 2:
            self.color = (0, 0, 255)
        if layer == 3:
            self.color = (0, 255, 0)

        self.x = random.randint(1, 100000) % self.width
        self.y = random.randint(1, 100000) % self.height

        self.y_max = 200

    def draw(self, win):
        if random.randint(1, 10) % 2:
            self.visible = True
        else:
            self.visible = False
            self.prevFlickerTime = pygame.time.get_ticks()

        if self.y > self.height:
            self.y = 0
            self.x = random.randint(1, 100000) % self.width

        if self.visible:
            win.set_at((self.x, self.y), self.color)

        if self.scroll:
            self.y += self.scrollSpeed
