from classes.misc_objects.missile import Missile
import pygame
from classes.misc_objects.subclass.object import Object

gunship = [
    pygame.image.load("C:/Users/neriy/Documents/GitHub Code/remadegalaga/sprites/player/gunship.gif"),
    pygame.image.load("C:/Users/neriy/Documents/GitHub Code/remadegalaga/sprites/player/gunship_red.gif")]

gunship[1] = pygame.transform.scale(gunship[1], (30, 30))

gunship_sfx1 = pygame.mixer.Sound("C:/Users/neriy/Documents/GitHub Code/remadegalaga/galaga_sfx/13 Fighter Shot1.mp3")

class Gunship(Object):
    iter = 0
    angle = 0
    prev_missile_time = 0
    speed = 4

    kidnapper = 0
    kidnap_slope = 0

    missile_buffer = []

    missile_ready = True
    canMove = True

    def __init__(self):
        self.x = 250
        self.y = 450
        super(Object, self).__init__()

    def draw(self, win, kidnapper_pos = None):
        ## For handling the different types of gunships, captured/non-captured
        temp_image = gunship[self.iter]

        ## Loops through the missile buffer to draw/handle deleting the missiles the player fires
        for obj in self.missile_buffer:
            if obj.y < 0:
                self.missile_buffer.pop(self.missile_buffer.index(obj))
            else:
                obj.draw(win)

        ## Handles the capturing process of the boss's "wave beam"
        if self.state == "Capturing":
            self.canMove = False
            self.missile_ready = False
            if self.kidnap_slope == 0:
                self.kidnap_slope = (kidnapper_pos[1] - self.y)/(kidnapper_pos[0] - self.x + 1)
            
            if self.y > kidnapper_pos[1] + 35:
                self.y -= 1
                self.angle += 20
                if self.y < kidnapper_pos[1] + 45:
                    self.iter = 1
            else:
                self.state = "Captured"
                self.angle = 0

            if self.x < kidnapper_pos[0] + 2:
                self.x += 1
            elif self.x > kidnapper_pos[0] + 2:
                self.x -= 1
            temp_image = pygame.transform.rotate(temp_image, self.angle)

        win.blit(temp_image, (self.x, self.y))

    def fire_missile(self):
        if self.missile_ready:
            if len(self.missile_buffer) < 2 and (self.prev_missile_time == 0 or pygame.time.get_ticks() - self.prev_missile_time > 70):
                self.missile_buffer.append(Missile(self.get_pos()))
                self.prev_missile_time = pygame.time.get_ticks()
                gunship_sfx1.play()

    def move_left(self):
        if self.x - self.speed > 0 and self.canMove:
            self.x -= self.speed

    def move_right(self):
        if self.x + self.speed < 470 and self.canMove:
            self.x += self.speed