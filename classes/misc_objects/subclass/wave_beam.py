from classes.misc_objects.subclass.object import Object

import os
import pygame

base_path = os.path.dirname(os.path.abspath(__file__))

image_path_1 = os.path.join(base_path, "../../../sprites/enemy/boss/boss_beam1.png")
image_path_2 = os.path.join(base_path, "../../../sprites/enemy/boss/boss_beam2.png")
image_path_3 = os.path.join(base_path, "../../../sprites/enemy/boss/boss_beam3.png")

wave_beam = [pygame.image.load(image_path_1),
            pygame.image.load(image_path_2),
            pygame.image.load(image_path_3)]

wave_beam[0] = pygame.transform.scale(wave_beam[0], (96, 160))
wave_beam[1] = pygame.transform.scale(wave_beam[1], (96, 160))
wave_beam[2] = pygame.transform.scale(wave_beam[2], (96, 160))


class WaveBeam(Object):
    status = ""
    iter = 0
    image_height = 159

    isFullLength = False
    ableToIncrease = False

    prev_draw_time = 0
    wave_duration_time = 0

    canReduceHeight = False
    canIncreaseHeight = False

    def __init__(self, shooter_pos):
        self.set_pos((shooter_pos[0] - 32, shooter_pos[1] + 35))
        self.status = "Beaming"
        super(Object, self).__init__()

    def draw(self, win):
        if self.image_height >= 159 and self.ableToIncrease:
            self.status = "Completed"
        elif self.prev_draw_time == 0 or pygame.time.get_ticks() - self.prev_draw_time > 150:
            self.iter += 1

            if self.iter > 2:
                self.iter = 0
            
            if not self.isFullLength: 
                self.canReduceHeight = True
            elif self.ableToIncrease:
                self.canIncreaseHeight = True

            self.prev_draw_time = pygame.time.get_ticks()

        if self.canReduceHeight:
            self.image_height -= 15.9
            self.canReduceHeight = False
        
        if self.canIncreaseHeight:
            self.image_height += 15.9
            self.canIncreaseHeight = False

        if self.image_height <= 0 and not self.isFullLength:
            self.isFullLength = True
            self.wave_duration_time = pygame.time.get_ticks()

        if pygame.time.get_ticks() - self.wave_duration_time >= 2000:
            self.ableToIncrease = True

        current_image = wave_beam[self.iter]

        if not self.isFullLength or self.ableToIncrease:
            current_image = pygame.transform.rotate(current_image, 180)
            current_image = pygame.transform.chop(current_image, (0, 0, 0, self.image_height))
            current_image = pygame.transform.rotate(current_image, 180)            
        win.blit(current_image, (self.x, self.y))
