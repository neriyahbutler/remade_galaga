from classes.enemy.subclass.bezier_curve import BezierCurve
from classes.enemy.boss import Boss
from classes.enemy.bee import Bee
from classes.enemy.butterfly import Butterfly
from classes.player.gunship import Gunship
from classes.misc_objects.star import Star

import pygame
import math
import random
import copy

pygame.init()

font = pygame.font.Font("C:/Users/neriy/Documents/GitHub Code/remadegalaga/font/Joystix.ttf", 15)

galaga_logo = [pygame.image.load("C:/Users/neriy/Documents/GitHub Code/remadegalaga/sprites/logo/galaga_1.png"),
pygame.image.load("C:/Users/neriy/Documents/GitHub Code/remadegalaga/sprites/logo/galaga_2.png"),
pygame.image.load("C:/Users/neriy/Documents/GitHub Code/remadegalaga/sprites/logo/galaga_3.png")]

galaga_logo[0] = pygame.transform.scale(galaga_logo[0], (179, 90))
galaga_logo[1] = pygame.transform.scale(galaga_logo[1], (179, 90))
galaga_logo[2] = pygame.transform.scale(galaga_logo[2], (179, 90))


width = 500
height = 500

clock = pygame.time.Clock()
win = pygame.display.set_mode((width, height))

wave_beam_buffer = []
explosion_buffer = []
stars_buffer = []
curve_array = []

fleet = {"boss" : [], "butterfly" : [], "bee" : []}
init_fleet_dive = [
    {"boss" : [], "butterfly" : [], "bee" : []},
    {"boss" : [], "butterfly" : [], "bee" : []},
    {"boss" : [], "butterfly" : [], "bee" : []},
    {"boss" : [], "butterfly" : [], "bee" : []},
    {"boss" : [], "butterfly" : [], "bee" : []},
    {"boss" : [], "butterfly" : [], "bee" : []}
]

def is_collision_wave_beam(target, wave_beam):
    if (wave_beam.x) <= target.x < (wave_beam.x + 96) and (wave_beam.y) <= target.y <= (wave_beam.y + 160 - wave_beam.image_height):
        return True
    return False

def is_collision(obj1, obj2):
    obj1_pos = obj1.get_pos()
    obj2_pos = obj2.get_pos()

    distance = math.sqrt(math.pow(obj1_pos[0] - obj2_pos[0], 2) + math.pow((obj1_pos[1] - obj2_pos[1]), 2))
    if distance < 30:
        return True
    return False


def create_fleet(fleet, boss_cnt = 4, butterfly_cnt = 16, bee_cnt = 20):
    for i in range(boss_cnt):
        fleet["boss"].append(Boss())
    for i in range(bee_cnt):
        fleet["bee"].append(Bee())
    for i in range(butterfly_cnt):
        fleet["butterfly"].append(Butterfly())

def set_init_pos(fleet):
    set_init_pos_bee(fleet)
    set_init_pos_boss(fleet)
    set_init_pos_butterfly(fleet)

def set_init_pos_boss(fleet):
    y_cor = 40
    x_cor = 200
    x_increment = 30
    
    for boss in fleet["boss"]:
        boss.set_pos((x_cor, y_cor))
        boss.set_init_pos((x_cor, y_cor))
        x_cor += x_increment

def set_init_pos_bee(fleet):
    y_cor = 130
    x_cor = 85
    x_increment = 35
    counter = 0

    new_row = False
    
    for bee in fleet["bee"]:
        if counter > 9 and not new_row:
            y_cor = 160
            x_cor = 85
            new_row = True
        bee.set_pos((x_cor, y_cor))
        bee.set_init_pos((x_cor, y_cor))
        x_cor += x_increment
        counter += 1

def set_init_pos_butterfly(fleet):
    y_cor = 70
    x_cor = 140
    x_increment = 30
    counter = 0

    new_row = False
    
    for butterfly in fleet["butterfly"]:
        if counter > 7 and not new_row:
            y_cor = 100
            x_cor = 140
            new_row = True
        butterfly.set_pos((x_cor, y_cor))
        butterfly.set_init_pos((x_cor, y_cor))
        x_cor += x_increment
        counter += 1


def setup_init_fleet_dive():
    for type in fleet.keys():
        index = 0
        basic_iter = 0
        even_ptr = 1
        odd_ptr = 0
        for obj in fleet[type]:
            if type == "butterfly":
                if index in [3, 4, 11, 12]:
                    init_fleet_dive[1][type].insert(odd_ptr, fleet[type].index(obj))
                    odd_ptr += 2
                    print(index)
                if index in [2, 5, 10, 13]:
                    init_fleet_dive[2][type].insert(even_ptr, fleet[type].index(obj))
                    even_ptr += 2
                if index in [0, 1, 6, 7, 8, 9, 14, 15]:
                    init_fleet_dive[3][type].insert(basic_iter, fleet[type].index(obj))
            if type == "bee":
                if index in [4, 5, 14, 15]:
                    init_fleet_dive[0][type].insert(even_ptr, fleet[type].index(obj))
                    even_ptr += 2
                if index in [0, 1, 8, 9, 10, 11, 18, 19]:
                    init_fleet_dive[5][type].insert(basic_iter, fleet[type].index(obj))
                if index in [2, 3, 6, 7, 12, 13, 16, 17]:
                    init_fleet_dive[4][type].insert(basic_iter, fleet[type].index(obj))
            if type == "boss":
                init_fleet_dive[2][type].insert(odd_ptr, fleet[type].index(obj))
                odd_ptr += 2
            index += 1              


def create_stars(stars_buffer_arg, stars_count, width_arg, height_arg):
    for i in range(stars_count):
        stars_buffer_arg.append(Star(random.randint(0, 4), width_arg, height_arg))

def display_stars():
    for star in stars_buffer:
        star.draw(win)


def score_menu(y_pos, score_1 = 0, hiscore_val = 0, score_2 = 0):
    _1up = font.render("1UP", 1, (202, 0, 42))
    hiscore = font.render("HI-SCORE", 1, (202, 0, 42))
    _2up = font.render("2UP", 1, (202, 0, 42))

    _1up_val =  font.render(str(score_1), 1, (255, 255, 255))
    hiscore_val = font.render(str(hiscore_val), 1, (255, 255, 255))
    _2up_val = font.render(str(score_2), 1, (255, 255, 255))

    win.blit(_1up, (40, y_pos))
    win.blit(hiscore, (190, y_pos))
    win.blit(_2up, (400, y_pos))

    win.blit(_1up_val, (90, y_pos + 15))
    win.blit(hiscore_val, (280, y_pos + 15))
    win.blit(_2up_val, (450, y_pos + 15))

def game_start_menu(y_pos, galaga_logo_iter):
    _1player = font.render("1 PLAYER", 1, (255, 255, 255))
    _2players = font.render("2 PLAYERS", 1, (255, 255, 255))
    credit = font.render("ALL CREDIT GOES TO NAMCO", 1, (255, 255, 255))
    creator_credit = font.render("MADE BY NERIYAHBUTLER", 1, (255, 255, 255))

    win.blit(galaga_logo[galaga_logo_iter], (175, y_pos + 120))

    win.blit(_1player, (200, y_pos + 250))
    win.blit(_2players, (200, y_pos + 275))
    win.blit(credit, (100, y_pos + 425))
    win.blit(creator_credit, (125, y_pos + 450))

def game_start(level = 0):
    create_fleet(fleet)
    set_init_pos(fleet)

def generate_init_curves():
    for i in range(len(init_fleet_dive)):
        if i == 0:
            for obj in init_fleet_dive[i]["bee"]:
                fleet["bee"][obj].x = 0
                fleet["bee"][obj].y = 0
                fleet["bee"][obj].curve_queue = [BezierCurve([fleet["bee"][obj].x + 490, fleet["bee"][obj].y + 484],
                                            [fleet["bee"][obj].x + 133.7, fleet["bee"][obj].y + 450.6],
                                            [fleet["bee"][obj].x + 190, fleet["bee"][obj].y + 400.3],
                                            [fleet["bee"][obj].x + 250, fleet["bee"][obj].y + 190]
                )]
        if i == 1:
            for obj in init_fleet_dive[i]["butterfly"]:
                print("Generating curves for butterfly object at index", str(obj))
                fleet["butterfly"][obj].x = 0
                fleet["butterfly"][obj].y = 0
                fleet["butterfly"][obj].curve_queue = [BezierCurve([fleet["butterfly"][obj].x - 55, fleet["butterfly"][obj].y + 484.5],
                                            [fleet["butterfly"][obj].x + 204, fleet["butterfly"][obj].y + 504],
                                            [fleet["butterfly"][obj].x + 250.4, fleet["butterfly"][obj].y + 50],
                                            [fleet["butterfly"][obj].x + 209, fleet["butterfly"][obj].y + 100]
                )]
        if i == 2:
            for obj in init_fleet_dive[i]["boss"]:
                fleet["boss"][obj].x = 0
                fleet["boss"][obj].y = 0
                fleet["boss"][obj].curve_queue = [BezierCurve([fleet["boss"][obj].x + 40.6, fleet["boss"][obj].y + 400.4],
                                            [fleet["boss"][obj].x + 80, fleet["boss"][obj].y + 450],
                                            [fleet["boss"][obj].x + 250, fleet["boss"][obj].y + 290],
                                            [fleet["boss"][obj].x + 240, fleet["boss"][obj].y + 100]),
                    
                                            BezierCurve([fleet["boss"][obj].x + 80, fleet["boss"][obj].y + 290],
                                            [fleet["boss"][obj].x + 50, fleet["boss"][obj].y + 300],
                                            [fleet["boss"][obj].x + 1.4, fleet["boss"][obj].y + 400],
                                            [fleet["boss"][obj].x + 40.6, fleet["boss"][obj].y + 400.4]
                                            ),

                                            BezierCurve([ fleet["boss"][obj].x + 1,  fleet["boss"][obj].y + 400],
                                            [fleet["boss"][obj].x + 30, fleet["boss"][obj].y + 380.3],
                                            [fleet["boss"][obj].x + 120, fleet["boss"][obj].y + 350],
                                            [fleet["boss"][obj].x + 80, fleet["boss"][obj].y + 290])]
            for obj in init_fleet_dive[i]["butterfly"]:
                fleet["butterfly"][obj].x = 0
                fleet["butterfly"][obj].y = 0
                fleet["butterfly"][obj].curve_queue = [BezierCurve([fleet["butterfly"][obj].x + 40.6, fleet["butterfly"][obj].y + 400.4],
                                            [fleet["butterfly"][obj].x + 80, fleet["butterfly"][obj].y + 450],
                                            [fleet["butterfly"][obj].x + 250, fleet["butterfly"][obj].y + 290],
                                            [fleet["butterfly"][obj].x + 240, fleet["butterfly"][obj].y + 100]),
                    
                                            BezierCurve([fleet["butterfly"][obj].x + 80, fleet["butterfly"][obj].y + 290],
                                            [fleet["butterfly"][obj].x + 50, fleet["butterfly"][obj].y + 300],
                                            [fleet["butterfly"][obj].x + 1.4, fleet["butterfly"][obj].y + 400],
                                            [fleet["butterfly"][obj].x + 40.6, fleet["butterfly"][obj].y + 400.4]
                                            ),

                                            BezierCurve([ fleet["butterfly"][obj].x + 1,  fleet["butterfly"][obj].y + 400],
                                            [fleet["butterfly"][obj].x + 30, fleet["butterfly"][obj].y + 380.3],
                                            [fleet["butterfly"][obj].x + 120, fleet["butterfly"][obj].y + 350],
                                            [fleet["butterfly"][obj].x + 80, fleet["butterfly"][obj].y + 290])]
        if i == 3:
            for obj in init_fleet_dive[i]["butterfly"]:
                fleet["butterfly"][obj].x = 0
                fleet["butterfly"][obj].y = 0
                fleet["butterfly"][obj].curve_queue = [
                    BezierCurve([fleet["butterfly"][obj].x + 400.6, fleet["butterfly"][obj].y + 405],
                    [fleet["butterfly"][obj].x + 340, fleet["butterfly"][obj].y + 380],
                    [fleet["butterfly"][obj].x + 250, fleet["butterfly"][obj].y + 200],
                    [fleet["butterfly"][obj].x + 290.6, fleet["butterfly"][obj].y + 150]
                    ),

                    
                    BezierCurve([fleet["butterfly"][obj].x + 390.4, fleet["butterfly"][obj].y + 250],
                    [fleet["butterfly"][obj].x + 450, fleet["butterfly"][obj].y + 290],
                    [fleet["butterfly"][obj].x + 500, fleet["butterfly"][obj].y + 400],
                    [fleet["butterfly"][obj].x + 400.6, fleet["butterfly"][obj].y + 405]
                    ),
                    
                    
                    BezierCurve([fleet["butterfly"][obj].x + 500, fleet["butterfly"][obj].y + 400],
                    [fleet["butterfly"][obj].x + 450, fleet["butterfly"][obj].y + 380.3],
                    [fleet["butterfly"][obj].x + 361.7, fleet["butterfly"][obj].y + 320],
                    [fleet["butterfly"][obj].x + 390.4, fleet["butterfly"][obj].y + 250])]
        if i == 4:
            for obj in init_fleet_dive[i]["bee"]:
                fleet["bee"][obj].x = 0
                fleet["bee"][obj].y = 0
                fleet["bee"][obj].curve_queue = [BezierCurve([fleet["bee"][obj].x + 490, fleet["bee"][obj].y + 484],
                                            [fleet["bee"][obj].x + 133.7, fleet["bee"][obj].y + 450.6],
                                            [fleet["bee"][obj].x + 190, fleet["bee"][obj].y + 400.3],
                                            [fleet["bee"][obj].x + 250, fleet["bee"][obj].y + 190]
                )]
        if i == 5:
            for obj in init_fleet_dive[i]["bee"]:
                fleet["bee"][obj].x = 0
                fleet["bee"][obj].y = 0
                fleet["bee"][obj].curve_queue = [BezierCurve([fleet["bee"][obj].x - 55, fleet["bee"][obj].y + 484.5],
                                            [fleet["bee"][obj].x + 204, fleet["bee"][obj].y + 504],
                                            [fleet["bee"][obj].x + 250.4, fleet["bee"][obj].y + 50],
                                            [fleet["bee"][obj].x + 209, fleet["bee"][obj].y + 100]
                )]

create_stars(stars_buffer, 80, width, height)

def draw_lines(win, enemy_obj):
    prev_x = enemy_obj.x
    prev_y = enemy_obj.y
    for i in range(len(enemy_obj.curve_queue)):
        enemy_obj_x = enemy_obj.curve_queue[i].calculate_point()[0]
        enemy_obj_y = enemy_obj.curve_queue[i].calculate_point()[1]
        if enemy_obj_x != 0 and enemy_obj_y != 0:
            print("Curr loc:", str(enemy_obj_x), str(enemy_obj_y))
            print("***********************")

            pygame.draw.line(win, (255,0,0), (prev_x, prev_y), (enemy_obj_x, enemy_obj_y))
            prev_x = enemy_obj_x
            prev_y = enemy_obj_y

def generate_bezier_points(bezier_curve):
    global curve_array

    pnt_x = -1
    pnt_y = -1
    bezier_curve_temp = copy.deepcopy(bezier_curve)
    while pnt_x != 0 and pnt_y != 0:
        pos = bezier_curve_temp.calculate_point()
        pnt_x = pos[0]
        pnt_y = pos[1]
        if pnt_x != 0 and pnt_y != 0:
            curve_array.append((pnt_x, pnt_y))

def generate_boss_curves(boss, gunship):
    choice = random.randint(1, 11) % 2
    if choice == 0:
        boss.curve_queue = [BezierCurve([boss.x + 150.7, boss.y + 264], [boss.x + 134.2, boss.y + 321.6],
                                        [boss.x + 0.2, boss.y + 433],
                                        [(gunship.x - random.randint(20, 60)), boss.y + 464]),
                            BezierCurve([boss.x + 0.5, boss.y + 95], [boss.x + 17, boss.y + 152.6],
                                        [boss.x + 155, boss.y + 182], [boss.x + 150.7, boss.y + 264]),
                            BezierCurve([boss.x + 98, boss.y + 96], [boss.x + 106, boss.y + 25],
                                        [boss.x + -1, boss.y + 10.5], [boss.x + 0.5, boss.y + 95]),
                            BezierCurve([boss.x, boss.y], [boss.x - 48, boss.y + 177],
                                        [boss.x + 102, boss.y + 172], [boss.x + 98, boss.y + 96])]
    else:
        boss.curve_queue = [BezierCurve([boss.x - 150.7, boss.y + 264], [boss.x - 134.2, boss.y + 321.6],
                                        [boss.x - 0.2, boss.y + 433],
                                        [(gunship.x + random.randint(20, 60)), boss.y + 464]),
                            BezierCurve([boss.x - 0.5, boss.y + 95], [boss.x - 17, boss.y + 152.6],
                                        [boss.x - 155, boss.y + 182], [boss.x - 150.7, boss.y + 264]),
                            BezierCurve([boss.x - 98, boss.y + 96], [boss.x - 106, boss.y + 25],
                                        [boss.x - -1, boss.y + 10.5], [boss.x - 0.5, boss.y + 95]),
                            BezierCurve([boss.x, boss.y], [boss.x + 48, boss.y + 177],
                                        [boss.x - 102, boss.y + 172], [boss.x - 98, boss.y + 96])]
    # self.initial_dive = True