from math import exp
from classes.enemy.subclass.enemy_explosion import Explosion
from setup_game import *

# TODO: Fix the delay for the bosses getting hit and turning purple

enemy_boss = Boss()
enemy_boss.set_pos((250,300))

player = Gunship()

game_bool = True
fired = False
enemies_setup = False
isFleetGenerated = False

# Variables for handling diving sequence
deathBoolean = False
firstDiveDone = False
secondDiveDone = False
secondDiveReady = False
prevDiveTime = 0

inGameStartMenu = False
gameStart = True
enemies_entering = False
diving_sequence = False

score_menu_y_pos = 510
galaga_logo_iter = 0
prev_entry_time = 0

entry_index = 0

mixed_count = 0
mixed_type_used_index = []

while game_bool:
    win.fill((0))
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_bool = False
    
    keys = pygame.key.get_pressed()
    clock.tick(60)
    
    display_stars()
    score_menu(score_menu_y_pos)
    
    if inGameStartMenu:
        game_start_menu(score_menu_y_pos, galaga_logo_iter)
        if galaga_logo_iter > 2:
            galaga_logo_iter = 0
    elif gameStart:
        if not isFleetGenerated:
            game_start()
            setup_init_fleet_dive()
            generate_init_curves()
            isFleetGenerated = True
            enemies_entering = True

        if enemies_entering:
            for entry in init_fleet_dive:
                if init_fleet_dive.index(entry) == entry_index:
                    if init_fleet_dive.index(entry) == 5: print(entry)
                    for type in entry.keys():
                        count = 0
                        for i in range(len(entry[type])):
                            obj_index = entry[type][i]
                            if fleet[type][obj_index].status != "Diving":
                                if i == 0:
                                    fleet[type][obj_index].status = "Diving"
                                    fleet[type][obj_index].dive(win)
                                    prev_entry_time = pygame.time.get_ticks()
                                else:
                                    if pygame.time.get_ticks() - prev_entry_time > 100:
                                        fleet[type][obj_index].status = "Diving"
                                        fleet[type][obj_index].dive(win)
                                        prev_entry_time = pygame.time.get_ticks()
                            else:
                                if len(fleet[type][obj_index].curve_queue) > 0:
                                    fleet[type][obj_index].dive(win)
                                else:
                                    if fleet[type][obj_index].x == fleet[type][obj_index].init_pos[0] and fleet[type][obj_index].y == fleet[type][obj_index].init_pos[1]:
                                        if init_fleet_dive.index(entry) != 2:
                                            count += 1
                                            if type == "bee":
                                                print("Status of", obj_index, "of type", type, "set to", fleet[type][obj_index].status)
                                        else:
                                            if (type + str(obj_index)) not in mixed_type_used_index:
                                                mixed_type_used_index.append((type + str(obj_index)))
                                                mixed_count += 1
                                        if count == len(entry[type]) and init_fleet_dive.index(entry) != 2:
                                            entry[type] = []
                                            entry_index += 1
                                            print("Diving complete", type)
                                            if entry_index > 5:
                                                enemies_entering = False
                                                diving_sequence = True
                                        elif mixed_count == 8 and init_fleet_dive.index(entry) == 2:
                                            entry["boss"] = []
                                            entry["butterfly"] = []
                                            entry_index += 1
                                            print("Diving complete for boss and butterfly")
                                    else:
                                        fleet[type][obj_index].move_to_init_pos()
        elif diving_sequence:
            if not deathBoolean:
                if not firstDiveDone or not secondDiveDone:
                    if prevDiveTime == 0:
                        prevDiveTime = pygame.time.get_ticks()
                    else:
                        if firstDiveDone:
                            if pygame.time.get_ticks() - prevDiveTime > 500:
                                secondDiveReady = True
                        if pygame.time.get_ticks() - prevDiveTime > 2000 or (not firstDiveDone and secondDiveReady):
                            if not firstDiveDone:
                                boss_it = random.randint(0, len(fleet["boss"]) - 1)
                                generate_boss_curves(fleet["boss"][boss_it], player)
                                fleet["boss"][boss_it].status = "Diving"
                                prevDiveTime = pygame.time.get_ticks()

        for enemy_type in fleet.keys():
            for obj in fleet[enemy_type]:
                if obj.status == "Diving" and not enemies_entering:
                    obj.dive(win)
                if not obj.getDead() and obj.x != 0 and obj.y != 0:
                    obj.draw(win)

        if player.get_state() == "Capturing":
            player.draw(enemy_boss.get_pos())
        elif player.get_state == "Captured":
            enemy_boss.capture_gunship(player)
        else:
            player.draw(win)

        for obj in wave_beam_buffer:
            if is_collision_wave_beam(player, obj):
                player.set_state("Capturing")

        for obj in explosion_buffer:
            if obj.index < 5:
                obj.draw(win)
            else:
                explosion_buffer.pop(explosion_buffer.index(obj))

        for missile in player.missile_buffer:
            for enemy_type in fleet.keys():
                for enemy in fleet[enemy_type]:
                    try:
                        if is_collision(missile, enemy) and not enemy.getDead():
                            enemy.lower_health()
                            if enemy.health == 0:
                                enemy.setDead()
                                explosion_buffer.append(Explosion(enemy.get_pos()))
                            player.missile_buffer.pop(player.missile_buffer.index(missile))
                    except Exception as e:
                        print(e)


        if keys[pygame.K_LEFT]:
            player.move_left()
        if keys[pygame.K_RIGHT]:
            player.move_right()
        if keys[pygame.K_SPACE]:
            player.fire_missile()

    if score_menu_y_pos >= 10:
        score_menu_y_pos -= 2

    pygame.display.update()


pygame.quit()
