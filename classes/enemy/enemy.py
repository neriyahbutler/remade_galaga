from classes.enemy.subclass.object import Object
from classes.enemy.subclass.bezier_curve import *
from classes.misc_objects.enemymissile import EnemyMissile
from classes.enemy.subclass.enemy_explosion import Explosion

class Enemy(Object):
    init_pos = []
    curve_queue = []
    missile_buffer = []
    explosion_buffer = []

    type = ""
    status = ""

    health = 0
    prev_draw_time = 0

    is_missile_fired = False
    moving_to_init_pos = False

    initial_dive = False
    canInitialDive = False
    def __init__(self, x = 50, y = 50, type_input = ""):
        self.init_pos = [x, y]
        self.x = x
        self.y = y
        self.type = type_input
        self.isDead = False

        if self.type == "Boss":
            self.health = 2
        else:
            self.health = 1        


    def set_init_pos(self, init_pos):
        self.init_pos = init_pos

    def fire(self, target):
        self.missile_buffer.append(EnemyMissile((self.x, self.y), target))

    def adjust_position(self, gunship = None):
        if len(self.curve_queue) != 0:
            if len(self.curve_queue) == 1:
                self.curve_queue[len(self.curve_queue) - 1].increase_velocity()

            if (self.curve_queue[len(self.curve_queue) - 1].peek_calculated_point()[0]) != 0:
                self.x = self.curve_queue[len(self.curve_queue) - 1].calculate_point()[0]
                self.y = self.curve_queue[len(self.curve_queue) - 1].calculate_point()[1]
            else:
                self.curve_queue.pop()

            # if self.curve_queue[len(self.curve_queue) - 1].t >= 1:
            #     self.curve_queue.pop()
            #     if len(self.curve_queue) == 0 and self.y > self.init_pos[1]:
            #         self.x = self.init_pos[0]
            #         self.y = -1
            #         self.curve_queue = [
            #             BezierCurve([self.x, self.y], [self.x, self.y], [self.x, self.init_pos[1]],
            #                         [self.x, self.init_pos[1]])]
                        
    def lower_health(self):
        self.health -= 1

    def move_to_init_pos(self):
        if self.status == "Returning":
            print("Moving to init", self.init_pos)
        if int(self.x) < int(self.init_pos[0]):
            self.x = int(self.x) + 1
        elif int(self.x) > int(self.init_pos[0]):
            self.x = int(self.x) - 1
        if int(self.y) < int(self.init_pos[1]):
            self.y = int(self.y) + 1
        elif int(self.y) > int(self.init_pos[1]):
            self.y = int(self.y) - 1
    
    def is_in_init_pos(self):
        if self.x == self.init_pos[0] and self.y == self.init_pos[1]:
            return True
        return False

    def setDead(self):
        self.isDead = True

    def getDead(self):
        return self.isDead

    def fire(self, target_pos):
        self.missile_buffer.append(EnemyMissile((self.init_pos[0], self.init_pos[1]), target_pos))

    def set_status(self, status):
        self.status = status