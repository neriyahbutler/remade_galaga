from classes.enemy.enemy import Enemy
from misc_objects.subclass.wave_beam import WaveBeam

import pygame
import random

boss_galaga = [pygame.image.load("C:/Users/neriy/Documents/GitHub Code/remadegalaga/sprites/enemy/boss/b1.png"),
               pygame.image.load("C:/Users/neriy/Documents/GitHub Code/remadegalaga/sprites/enemy/boss/b2.png"),
               pygame.image.load("C:/Users/neriy/Documents/GitHub Code/remadegalaga/sprites/enemy/boss/b2_1.png"),
               pygame.image.load("C:/Users/neriy/Documents/GitHub Code/remadegalaga/sprites/enemy/boss/b2_2.png")]

boss_galaga[0] = pygame.transform.scale(boss_galaga[0], (30, 30))
boss_galaga[1] = pygame.transform.scale(boss_galaga[1], (30, 30))
boss_galaga[2] = pygame.transform.scale(boss_galaga[2], (30, 30))
boss_galaga[3] = pygame.transform.scale(boss_galaga[3], (30, 30))

boss_sfx1 = pygame.mixer.Sound("C:/Users/neriy/Documents/GitHub Code/remadegalaga/galaga_sfx/07 Boss Stricken#1.mp3")
boss_sfx2 = pygame.mixer.Sound("C:/Users/neriy/Documents/GitHub Code/remadegalaga/galaga_sfx/08 Boss Stricken#2.mp3")
boss_sfx3 = pygame.mixer.Sound("C:/Users/neriy/Documents/GitHub Code/remadegalaga/galaga_sfx/10 Tractor Beam Shot.mp3")
boss_sfx4 = pygame.mixer.Sound("C:/Users/neriy/Documents/GitHub Code/remadegalaga/galaga_sfx/11 Tractor Beam Capture.mp3")
boss_sfx5 = pygame.mixer.Sound("C:/Users/neriy/Documents/GitHub Code/remadegalaga/galaga_sfx/12 Capture Music.mp3")

class Boss(Enemy):
    wave_beam_buffer = []
    captured_gunship = None
    isDead = False

    def __init__(self):
        self.health = 2
        super(Enemy, self).__init__()

    def draw(self, win):
        ## Handles the positioning of the captured gunship caught by the "wave beam"
        if self.captured_gunship != None:
            self.captured_gunship.set_pos(self.x, self.y + 35)

        ## Handles the animation of the boss for before it is hit once and after
        if self.prev_draw_time == 0 or pygame.time.get_ticks() - self.prev_draw_time > 500:
            if self.health == 2:
                if self.iter < 1:
                    self.iter += 1
                else:
                    self.iter = 0
            else:
                if self.iter < 3:
                    self.iter += 1
                else:
                    self.iter = 2
            self.prev_draw_time = pygame.time.get_ticks()

        for obj in self.missile_buffer:
            obj.draw(win)

        ## Handles the increase of the "wave beam"'s "height" for when it stretches out and retracts
        for obj in self.wave_beam_buffer:
            if obj.image_height >= 159 and obj.ableToIncrease:
                self.wave_beam_buffer.pop()
            else:
                obj.draw(win)

        win.blit(boss_galaga[self.iter], (self.x, self.y))

    def dive(self, win):
        random_int = random.randint(1, 11)
        choice = random_int % 2

        self.adjust_position()

    def fire_wave_beam(self):
        self.wave_beam_buffer.append(WaveBeam(self.get_pos()))

    def capture_gunship(self, gunship):
        self.captured_gunship = gunship

    def lower_health(self):
        Enemy.lower_health(self)
        if self.health == 0:
            boss_sfx2.play()
        else:
            boss_sfx1.play()
            self.iter = 2

    def setDead(self):
        self.isDead = True
    
    def getDead(self):
        return self.isDead