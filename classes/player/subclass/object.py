import pygame
pygame.mixer.init()

class Object(object):
    curr_pos = []
    state = ""
    image = ""
    iter = 0

    def __init__(self):
        self.curr_pos = [0, 0]
        self.state = "Idle"
    
    def set_pos(self, pos):
        self.curr_pos = pos

    def get_pos(self):
        return self.curr_pos

    def set_state(self, state):
        self.state = state

    def get_state(self):
        return self.state