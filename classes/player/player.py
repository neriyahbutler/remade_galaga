import os

base_path = os.path.dirname(os.path.abspath(__file__))

from setup_game import score_menu
from classes.player.gunship import Gunship

import pygame

image_path_1 = os.path.join(base_path, "..\..\sprites\player\gunship.gif")
image_path_2 = os.path.join(base_path, "..\..\sprites\player\gunship_red.gif")

gunship = [
    pygame.image.load(image_path_1),
    pygame.image.load(image_path_2)]

gunship[1] = pygame.transform.scale(gunship[1], (30, 30))

sfx_path = os.path.join(base_path, "..\..\galaga_sfx/13 Fighter Shot1.mp3")
gunship_sfx1 = pygame.mixer.Sound(sfx_path)

class PlayerClass(object):
    life_x = 5
    lives = 0
    score = 0
    death_timer = 0
    prev_missile_time = 0
    gunship_buffer = []
    lives_buffer = []
    missile_ready = True

    state = ""

    x = 0
    y = 0

    def __init__(self):
        self.lives = 3
        self.gunship_buffer.append(Gunship())
        self.x = self.gunship_buffer[0].x
        self.y = self.gunship_buffer[0].y

    def generate_lives(self, win):
        self.life_x = 5
        for i in range(self.lives):
            win.blit(gunship[0], (self.life_x, 465))
            self.life_x += 35
    
    def set_score(self, score):
        self.score = score

    def get_score(self):
        return self.score

    def increase_lives(self):
        self.lives += 1

    def decrease_lives(self):
        self.lives -= 1

    def get_lives_count(self):
        return self.lives

    def set_death_timer(self):
        self.death_timer = pygame.time.get_ticks()

    def get_death_timer(self):
        return self.death_timer

    def move_left(self):
        self.x = self.gunship_buffer[0].x

        for obj in self.gunship_buffer:
            obj.move_left()

    def move_right(self):
        self.x = self.gunship_buffer[0].x
        for obj in self.gunship_buffer:
            obj.move_right()

    def fire_missile(self):
        obj = self.gunship_buffer[0]

        if len(obj.missile_buffer) >= 2:
            self.missile_ready = False

        if not self.missile_ready:
            if pygame.time.get_ticks() - self.prev_missile_time > 70:
                self.missile_ready = True
        if self.fire_missile:
            # for obj in self.gunship_buffer:
            if len(obj.missile_buffer) < 2 and (self.prev_missile_time == 0 or pygame.time.get_ticks() - self.prev_missile_time > 70):
                for obj_gunship in self.gunship_buffer:
                    obj_gunship.fire_missile()

                gunship_sfx1.play()
                self.prev_missile_time = pygame.time.get_ticks()

    def draw(self, win, draw_gunship = True, kidnapper_pos = None):
        self.generate_lives(win)
        if draw_gunship:
            for obj in self.gunship_buffer:
                obj.draw(win, kidnapper_pos)

        for obj in self.lives_buffer:
            obj.draw(win)

    def get_pos(self):
        return (self.x, self.y)

    def get_state(self):
        return self.state

    def set_state(self, state):
        self.state = state
        for obj in self.gunship_buffer:
            obj.set_state(state)