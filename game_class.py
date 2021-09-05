import os

from math import exp

from classes.enemy.subclass.enemy_explosion import Explosion
from classes.misc_objects.explosion import PlayerExplosion
from classes.player.player import PlayerClass
from setup_game import *

# TODO: Fix the delay for the bosses getting hit and turning purple

player = Gunship()
player_one = PlayerClass()
game_bool = True
godMode = False

# Variables for setting up enemies
enemies_setup = True
isFleetGenerated = False

# Variables for handling the menu
inGameStartMenu = True
cursorDisplay = False
cursor_y_pos = 262

cursor_choice_1 = 262
cursor_choice_2 = 285

galaga_logo_iter = 0

# Variables for handling the gameplay/levels
base_path = os.path.dirname(os.path.abspath(__file__))
level_sfx_path = os.path.join(base_path, "galaga_sfx/02 Start Music.mp3")

level_sfx1 = pygame.mixer.Sound(level_sfx_path)

gameStart = True
level_intro_done = False

level_intro_time = 0
level_counter = 1

enemies_entering = False
diving_sequence = False

prev_entry_time = 0
score_menu_y_pos = 510
entry_index = 0

boss_capture_iter = -1

# Variables for handling diving sequence
enemy_status_reset = False

returningBoolean = False
deathBoolean = False
captureBoolean = False

firstDiveDone = False
secondDiveDone = False
secondDiveReady = False

prevDiveTime = 0
mixed_count = 0
mixed_type_used_index = []

live_count = 3

while game_bool:
    win.fill((0))
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_bool = False
    
    keys = pygame.key.get_pressed()
    clock.tick(60)
    
    display_stars()
    score_menu(score_menu_y_pos, player_one.get_score())
    
    if inGameStartMenu:
        game_start_menu(score_menu_y_pos, galaga_logo_iter)
        if galaga_logo_iter > 2:
            galaga_logo_iter = 0

        if cursorDisplay:
            win.blit(cursor_logo, (180 , cursor_y_pos))
            if keys[pygame.K_SPACE]:
                cursorDisplay = False
                inGameStartMenu = False
            if keys[pygame.K_UP]:
                cursor_y_pos = cursor_choice_1
            if keys[pygame.K_DOWN]:
                cursor_y_pos = cursor_choice_2
    elif gameStart:
        if not level_intro_done:
            level_intro(level_counter)
            if level_intro_time == 0:
                level_intro_time = pygame.time.get_ticks()
                level_sfx1.play()
            if pygame.time.get_ticks() - level_intro_time > 6500:
                level_intro_done = True
        if not isFleetGenerated and level_intro_done:
            game_start()
            setup_init_fleet_dive()
            generate_init_curves()
            isFleetGenerated = True
            enemies_entering = True

        elif enemies_entering:
            for entry in init_fleet_dive:
                if init_fleet_dive.index(entry) == entry_index:
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
                                            # if type == "bee":
                                                # print("Status of", obj_index, "of type", type, "set to", fleet[type][obj_index].status)
                                        else:
                                            if (type + str(obj_index)) not in mixed_type_used_index:
                                                mixed_type_used_index.append((type + str(obj_index)))
                                                mixed_count += 1
                                        if count == len(entry[type]) and init_fleet_dive.index(entry) != 2:
                                            entry[type] = []
                                            entry_index += 1
                                            # print("Diving complete", type)
                                            if entry_index > 5:
                                                enemies_entering = False
                                                diving_sequence = True
                                        elif mixed_count == 8 and init_fleet_dive.index(entry) == 2:
                                            entry["boss"] = []
                                            entry["butterfly"] = []
                                            entry_index += 1
                                            # print("Diving complete for boss and butterfly")
                                    else:
                                        fleet[type][obj_index].move_to_init_pos()
        elif diving_sequence:
            if not enemy_status_reset:
                for fleet_type in fleet.keys():
                    for i in range(len(fleet[fleet_type])):
                        fleet[fleet_type][i].status = ""
                enemy_status_reset = True
                
            if not deathBoolean and not captureBoolean and not returningBoolean:
                if not firstDiveDone or not secondDiveDone:
                    if prevDiveTime == 0:
                        prevDiveTime = pygame.time.get_ticks()
                    else:
                        if firstDiveDone:
                            if pygame.time.get_ticks() - prevDiveTime > 500:
                                secondDiveReady = True
                        if pygame.time.get_ticks() - prevDiveTime > 2000 or (not firstDiveDone and not secondDiveReady):
                            if not firstDiveDone:
                                dive_sfx.play()
                                boss_it = living_fleet_idx["boss"][random.randint(0, len(living_fleet_idx["boss"]) - 1)]
                                generate_boss_curves(fleet["boss"][boss_it], player)
                                fleet["boss"][boss_it].status = "Diving"
                                fleet["boss"][boss_it].fire(player)

                                firstDiveDone = True
                                prevDiveTime = pygame.time.get_ticks()
                            else:
                                dive_sfx.play()
                                bee_it = living_fleet_idx["bee"][random.randint(0, len(living_fleet_idx["bee"]) - 1)]
                                generate_bee_curves(fleet["bee"][bee_it], player)
                                fleet["bee"][bee_it].status = "Diving"
                                fleet["bee"][bee_it].fire(player)

                                secondDiveDone = True
                                prevDiveTime = pygame.time.get_ticks()
                else:
                    if (pygame.time.get_ticks() - prevDiveTime) > 3000:
                        x = random.randint(0, 4)

                        if (x == 0 or x == 3) and len(living_fleet_idx["bee"]) > 0:
                            dive_sfx.play()
                            bee_it = living_fleet_idx["bee"][random.randint(0, len(living_fleet_idx["bee"]) - 1)]
                            generate_bee_curves(fleet["bee"][bee_it], player)
                            fleet["bee"][bee_it].status = "Diving"
                            fleet["bee"][bee_it].fire(player)

                            prevDiveTime = pygame.time.get_ticks()

                        elif (x == 1 or x == 4) and len(living_fleet_idx["butterfly"]) > 0:
                            dive_sfx.play()
                            butterfly_it = living_fleet_idx["butterfly"][random.randint(0, len(living_fleet_idx["butterfly"]) - 1)]
                            generate_butterfly_curves(fleet["butterfly"][butterfly_it], player)
                            fleet["butterfly"][butterfly_it].status = "Diving"
                            fleet["butterfly"][butterfly_it].fire(player)


                            prevDiveTime = pygame.time.get_ticks()

                        if x == 2 and len(living_fleet_idx["boss"]) > 0:
                            dive_sfx.play()
                            boss_it = living_fleet_idx["boss"][random.randint(0, len(living_fleet_idx["boss"]) - 1)]
                            generate_boss_curves(fleet["boss"][boss_it], player)
                            fleet["boss"][boss_it].status = "Diving"
                            fleet["boss"][boss_it].fire(player)


                            prevDiveTime = pygame.time.get_ticks()

        enemy_cnt = 0
        for enemy_type in fleet.keys():
            if enemy_type != "gunship":
                for obj in fleet[enemy_type]:
                    if obj.status == "Diving" and enemies_entering == False:
                        if enemy_type == "boss" and obj.y > 300 and not obj.capture_checked:
                            # capture_choice = random.randint(0, 10) % 2
                            if 0 == 0 and boss_capture_iter == -1:
                                obj.fire_wave_beam()
                                boss_capture_iter = fleet["boss"].index(obj)
                            obj.capture_checked = True
                            # Seems like the curve queue ends up being empty after completing the wave beam
                        obj.dive(win, player_one)
                    if obj.status == "Beaming" and enemies_entering == False and len(obj.wave_beam_buffer) == 0:
                        obj.status = "Diving"
                    if not obj.getDead() and obj.x != 0 and obj.y != 0:
                        obj.draw(win)
                        display_enemy_details(obj, win)
                    if obj.getDead():
                        enemy_cnt += 1
                    for missile in obj.missile_buffer:
                        if captureBoolean or returningBoolean:
                            obj.missile_buffer = []
                        if is_collision(missile, player_one) and not godMode:
                            obj.missile_buffer.pop(obj.missile_buffer.index(missile))
                            player_death_sfx.play()
                            deathBoolean = True
                            for obj in player_one.gunship_buffer:
                                player_explosion_buffer.append(PlayerExplosion(obj.get_pos()))
                            player_one.decrease_lives()
                            death_timer = pygame.time.get_ticks()

        if pygame.time.get_ticks() - death_timer > 3000 and player_one.lives >= 0:
            deathBoolean = False
            
        if pygame.time.get_ticks() - capture_timer > 4000 and player_one.lives >= 0 and captureBoolean == True:
            captureBoolean = False
            player_one.decrease_lives()
            player_one.gunship_buffer = [Gunship()]
            player_one.set_state("")

        if pygame.time.get_ticks() - return_timer > 1500 and return_timer != 0:
            fleet["gunship"][0].set_state("Returning_2")
            return_timer = 0

        if enemy_cnt == 40:
            level_intro_done = False
            isFleetGenerated = False
            enemies_entering = False
            diving_sequence = False

            level_intro_time = 0
            level_counter += 1

            fleet["bee"] = []
            fleet["butterfly"] = []
            fleet["boss"] = []

        if len(player_one.gunship_buffer) > 0:
            if player_one.gunship_buffer[0].state == "Capturing":
                captureBoolean = True
                player_one.draw(win, True, fleet["boss"][boss_capture_iter].get_pos())
            elif player_one.gunship_buffer[0].state == "Captured":
                captureBoolean = True
                player_one.draw(win, True, fleet["boss"][boss_capture_iter].get_pos())
            elif not deathBoolean:
                player_one.draw(win)
            elif deathBoolean:
                player_one.draw(win, False)

            display_gunship_details(player_one, win)

        try:
            if len(fleet["gunship"]) > 0:
                # if fleet["gunship"][0].get_state() == "Returning_1":
                #     fleet["gunship"][0].draw(win)
                if fleet["gunship"][0].get_state() == "Returning_2":
                    if fleet["gunship"][0].y == player_one.gunship_buffer[0].y:
                        rescue_sfx1.stop()
                        player_one.gunship_buffer = [Gunship(220), Gunship()]
                        returningBoolean = False
                        captureBoolean = False
                        fleet["gunship"] = []
                    move_gunships_to_init_pos(player_one.gunship_buffer[0], fleet["gunship"][0])
                    fleet["gunship"][0].draw(win)
                else:
                    fleet["gunship"][0].draw(win, fleet["boss"][boss_capture_iter].get_pos())
        except:
            print("Boss doesn't exist")

        if len(fleet["boss"]) > 0:
            for obj in fleet["boss"][boss_capture_iter].wave_beam_buffer:
                for gunship_obj in player_one.gunship_buffer:
                    if is_collision_wave_beam(gunship_obj, obj) and (player_one.get_state() != "Capturing" and player_one.get_state() != "Captured"):
                        fleet["boss"][boss_capture_iter].captured_ship()
                        player_one.set_state("Capturing")
                        deathBoolean = True
                        capture_timer = pygame.time.get_ticks()

        # Why is the y value in the negatives?
        if len(fleet["boss"]) > 0 and len(player_one.gunship_buffer) > 0:
            if fleet["boss"][boss_capture_iter].x == fleet["boss"][boss_capture_iter].init_pos[0] and player_one.gunship_buffer[0].state == "Captured":
                fleet["gunship"].append(player_one.gunship_buffer.pop())
                # print("Gunship popped out of buffer")
            # elif player_one.gunship_buffer[0].state == "Captured":
                # print("Boss's init pos:", fleet["boss"][boss_capture_iter].init_pos)
                # print("Boss's curr pos:", fleet["boss"][boss_capture_iter].get_pos())

        for obj in explosion_buffer:
            if obj.index < 5:
                obj.draw(win)
            else:
                explosion_buffer.pop(explosion_buffer.index(obj))

        for obj in player_explosion_buffer:
            if obj.index < 16:
                obj.draw(win)
            else:
                player_explosion_buffer.pop(player_explosion_buffer.index(obj))

        for missile in player.missile_buffer:
            for enemy_type in fleet.keys():
                for enemy in fleet[enemy_type]:
                    try:
                        if is_collision(missile, enemy) and not enemy.getDead():
                            enemy.lower_health()
                            if enemy.health == 0:
                                if enemy_type == "boss" and fleet["boss"].index(enemy) == boss_capture_iter:
                                    rescue_sfx1.play()
                                    fleet["gunship"][0].set_state("Returning_1")
                                    returningBoolean = True
                                    return_timer = pygame.time.get_ticks()
                                # player_one.set_score(player_one.get_score() + 100)
                                living_enemy_index = living_fleet_idx[enemy_type].index(fleet[enemy_type].index(enemy))
                                living_fleet_idx[enemy_type].pop(living_enemy_index)
                                enemy.setDead()
                                explosion_buffer.append(Explosion(enemy.get_pos()))
                            player.missile_buffer.pop(player.missile_buffer.index(missile))
                    except Exception as e:
                        print(e)

        
        if not deathBoolean and not captureBoolean and not returningBoolean:
            if keys[pygame.K_LEFT]:
                player_one.move_left()
            if keys[pygame.K_RIGHT]:
                player_one.move_right()
            if keys[pygame.K_SPACE]:
                player_one.fire_missile()

    if score_menu_y_pos >= 10:
        score_menu_y_pos -= 2
    else:
        cursorDisplay = True

    pygame.display.update()


pygame.quit()
