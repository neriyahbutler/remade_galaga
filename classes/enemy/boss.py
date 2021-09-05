import os

from classes.enemy.enemy import Enemy
from misc_objects.subclass.wave_beam import WaveBeam

import pygame
import random

base_path = os.path.dirname(os.path.abspath(__file__))

image_path_1 = os.path.join(base_path, "../../sprites/enemy/boss/b1.png")
image_path_2 = os.path.join(base_path, "../../sprites/enemy/boss/b2.png")
image_path_3 = os.path.join(base_path, "../../sprites/enemy/boss/b2_1.png")
image_path_4 = os.path.join(base_path, "../../sprites/enemy/boss/b2_2.png")

boss_galaga = [pygame.image.load(image_path_1),
               pygame.image.load(image_path_2),
               pygame.image.load(image_path_3),
               pygame.image.load(image_path_4)]

boss_galaga[0] = pygame.transform.scale(boss_galaga[0], (30, 30))
boss_galaga[1] = pygame.transform.scale(boss_galaga[1], (30, 30))
boss_galaga[2] = pygame.transform.scale(boss_galaga[2], (30, 30))
boss_galaga[3] = pygame.transform.scale(boss_galaga[3], (30, 30))

sfx_path_1 = os.path.join(base_path, "../../galaga_sfx/07 Boss Stricken#1.mp3")
sfx_path_2 = os.path.join(base_path, "../../galaga_sfx/08 Boss Stricken#2.mp3")
sfx_path_3 = os.path.join(base_path, "../../galaga_sfx/10 Tractor Beam Shot.mp3")
sfx_path_4 = os.path.join(base_path, "../../galaga_sfx/11 Tractor Beam Capture.mp3")
sfx_path_5 = os.path.join(base_path, "../../galaga_sfx/12 Capture Music.mp3")

boss_sfx1 = pygame.mixer.Sound(sfx_path_1)
boss_sfx2 = pygame.mixer.Sound(sfx_path_2)
boss_sfx3 = pygame.mixer.Sound(sfx_path_3)
boss_sfx4 = pygame.mixer.Sound(sfx_path_4)
boss_sfx5 = pygame.mixer.Sound(sfx_path_5)

class Boss(Enemy):
    wave_beam_buffer = []
    captured_gunship = None
    isDead = False
    capture_checked = False

    gunship_captured = False
    capture_theme_played = False

    wave_complete = False

    def __init__(self):
        self.health = 2
        super(Enemy, self).__init__()

    def draw(self, win):
        ## Handles the positioning of the captured gunship caught by the "wave beam"

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
            if obj.y > 500:
                self.missile_buffer.pop(self.missile_buffer.index(obj))
        ## Handles the increase of the "wave beam"'s "height" for when it stretches out and retracts
        for obj in self.wave_beam_buffer:
            if obj.image_height >= 159 and obj.ableToIncrease:
                self.set_status("Diving")
                self.wave_beam_buffer.pop()
            else:
                obj.draw(win)

        win.blit(boss_galaga[self.iter], (self.x, self.y))

    def dive(self, win, target_pos = None):
        if self.gunship_captured and not self.capture_theme_played:
            boss_sfx4.stop()
            boss_sfx5.play()
            self.capture_theme_played = True
        self.adjust_position()
        # if self.wave_complete:
        #     self.y += 1
        if self.y > 500:
            self.x = self.init_pos[0]
            self.y = self.init_pos[1] - 200
            self.moving_to_init_pos = True
            # if self.wave_complete: self.wave_complete = False
        if self.moving_to_init_pos:
            self.move_to_init_pos()
            if self.x == self.init_pos[0] and self.y == self.init_pos[1]:
                self.moving_to_init_pos = False
                if self.capture_theme_played:
                    boss_sfx5.stop()

    def fire_wave_beam(self):
        boss_sfx3.play()
        self.wave_beam_buffer.append(WaveBeam(self.get_pos()))
        self.status = "Beaming"

    def capture_gunship(self, gunship):
        self.captured_gunship = gunship

    def captured_ship(self):
        boss_sfx3.stop()
        boss_sfx4.play()
        self.gunship_captured = True

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

    def set_state(self):
        return self.state