from classes.enemy.enemy import Enemy

import pygame
import random

butterfly = [
    pygame.image.load("C:/Users/neriy/Documents/GitHub Code/remadegalaga/sprites/enemy/butterfly/b1.png"),
    pygame.image.load("C:/Users/neriy/Documents/GitHub Code/remadegalaga/sprites/enemy/butterfly/b2.png")
    ]

butterfly[0] = pygame.transform.scale(butterfly[0], (30, 30))
butterfly[1] = pygame.transform.scale(butterfly[1], (30, 30))

butterfly_sfx1 = pygame.mixer.Sound("C:/Users/neriy/Documents/GitHub Code/remadegalaga/galaga_sfx/06 Goei Stricken.mp3")

class Butterfly(Enemy):
    def draw(self, win):
        for obj in self.missile_buffer:
            obj.draw(win)
        if self.prev_draw_time == 0 or pygame.time.get_ticks() - self.prev_draw_time > 500:
            if self.iter < 1:
                self.iter += 1
            else:
                self.iter = 0            
            self.prev_draw_time = pygame.time.get_ticks()
        win.blit(butterfly[self.iter], (self.x, self.y))

    def dive(self, win):
        # random_int = random.randint(1, 11)
        # choice = random_int % 2
        # prev_x = self.x
        # prev_y = self.y
        # if not self.initial_dive:
        #     self.generate_butterfly_curves(choice, gunship)
        self.adjust_position()

    def lower_health(self):
        Enemy.lower_health(self)
        if self.health == 0:
            butterfly_sfx1.play()