import os

from setup_game import *

from classes.enemy.subclass.enemy_explosion import Explosion
from classes.misc_objects.explosion import PlayerExplosion
from classes.player.player import PlayerClass

debug = False

player = Gunship()
player_one = PlayerClass()
game_bool = True
godMode = False

# Variables for setting up enemies
enemies_setup = True
isFleetGenerated = False

# Variables for handling the menu
pauseGame = False

inGameStartMenu = True
cursorDisplay = False
cursor_y_pos = 262

cursor_choice_1 = 262
cursor_choice_2 = 285

galaga_logo_iter = 0

# Variables for handling the gameplay/levels
base_path = os.path.dirname(os.path.abspath(__file__))
level_sfx_path = os.path.join(base_path, "galaga_sfx/wav/02 Start Music.wav")

level_sfx1 = pygame.mixer.Sound(level_sfx_path)

gameStart = True
level_intro_done = False
playerStatsDisplay = False

gameover_time = 0

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

# Loop for handling the game
while game_bool:
    win.fill((0))
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_bool = False
    
    keys = pygame.key.get_pressed()
    clock.tick(60)
    
    display_stars()
    score_menu(score_menu_y_pos, player_one.get_score())
    
    missile_cnt = 0
    enemy_alive_cnt = -1

    # Boolean to handle if the menu should be displayed
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
    # If this boolean is true, then the game will start and the menu will go away
    elif gameStart:
        # For handling the "Level <num here>" +display
        if not level_intro_done:
            level_intro(level_counter)
            if level_intro_time == 0:
                level_intro_time = pygame.time.get_ticks()
                level_sfx1.play()
            if pygame.time.get_ticks() - level_intro_time > 6500:
                level_intro_done = True
        #  Once level intro is completed, set the boolean to handle fleet creation and etc
        if not isFleetGenerated and level_intro_done:
            game_start()
            setup_init_fleet_dive()
            generate_init_curves()
            isFleetGenerated = True
            enemies_entering = True
        # If the boolean is true, then the algo for handling the enemies entering will run
        elif enemies_entering:
            # Loops through all the enemies created and handles each "dive group" entering the screen
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
                                    # Handles enemies with an empty cuve_queue so they can move towards their init pos once the bezier curve complete
                                    if fleet[type][obj_index].x == fleet[type][obj_index].init_pos[0] and fleet[type][obj_index].y == fleet[type][obj_index].init_pos[1]:
                                        if init_fleet_dive.index(entry) != 2:
                                            count += 1
                                        else:
                                            if (type + str(obj_index)) not in mixed_type_used_index:
                                                mixed_type_used_index.append((type + str(obj_index)))
                                                mixed_count += 1
                                        if count == len(entry[type]) and init_fleet_dive.index(entry) != 2:
                                            entry[type] = []
                                            entry_index += 1
                                            if entry_index > 5:
                                                enemies_entering = False
                                                diving_sequence = True
                                        elif mixed_count == 8 and init_fleet_dive.index(entry) == 2:
                                            entry["boss"] = []
                                            entry["butterfly"] = []
                                            entry_index += 1
                                    else:
                                        fleet[type][obj_index].move_to_init_pos()
        # When this boolean is true, starts diving process for enemies
        elif diving_sequence:
            enemy_alive_cnt = 0

            if not enemy_status_reset:
                for fleet_type in fleet.keys():
                    for i in range(len(fleet[fleet_type])):
                        fleet[fleet_type][i].status = ""
                enemy_status_reset = True

            if not deathBoolean and not captureBoolean and not returningBoolean and not pauseGame:
                # If this condition is met, then the static diving sequence for the beginning of the level will take place first
                if not firstDiveDone or not secondDiveDone:
                    if prevDiveTime == 0:
                        prevDiveTime = pygame.time.get_ticks()
                    else:
                        if firstDiveDone:
                            if pygame.time.get_ticks() - prevDiveTime > 500:
                                secondDiveReady = True
                        if pygame.time.get_ticks() - prevDiveTime > 2000 or (not firstDiveDone and not secondDiveReady):
                            if len(living_fleet_idx["boss"]) < 1 or len(living_fleet_idx["bee"]) < 1:
                                firstDiveDone = True
                                secondDiveDone = True
                            else:
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
                # The normal diving algo that runs once the initial diving sequence has been finished/can't run
                else:
                    if (pygame.time.get_ticks() - prevDiveTime) > 3000 - level_counter * (150):
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

        handle_level_logos(win, level_counter)

        enemy_cnt = 0
        # For handling collisions for the enemy's missiles and the boss's wave beam
        for enemy_type in fleet.keys():
            if enemy_type != "gunship":
                for obj in fleet[enemy_type]:
                    if not obj.getDead():

                        enemy_alive_cnt += 1
                        missile_cnt += len(obj.missile_buffer)

                        # if obj.health < 0:
                        #     print("Enemy found that should be dead")

                        if obj.status == "Diving" and enemies_entering == False and not pauseGame:
                            if enemy_type == "boss" and obj.y > 300 and not obj.capture_checked:
                                # capture_choice = random.randint(0, 10) % 2
                                if 0 == 0 and boss_capture_iter == -1:
                                    obj.fire_wave_beam()
                                    boss_capture_iter = fleet["boss"].index(obj)
                                obj.capture_checked = True
                                # Seems like the curve queue ends up being empty after completing the wave beam
                            obj.dive(win, player_one)
                        if obj.status == "Beaming" and enemies_entering == False and len(obj.wave_beam_buffer) == 0 and not pauseGame:
                            obj.status = "Diving"
                            # boss_capture_iter = -1
                        if not obj.getDead() and obj.x != 0 and obj.y != 0:
                            obj.draw(win, pauseGame)
                            if debug:
                                display_enemy_details(obj, win)
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

        if deathBoolean and player_one.lives < 0:
            game_over()
            if gameover_time == 0:
                gameover_time = pygame.time.get_ticks()
            if pygame.time.get_ticks() - gameover_time > 4000:
                gameStart = False
                playerStatsDisplay = True

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

        if enemy_alive_cnt == 0:
            level_intro_done = False
            isFleetGenerated = False
            enemies_entering = False
            diving_sequence = False

            mixed_count = 0
            entry_index = 0
            level_intro_time = 0
            level_counter += 1
            boss_capture_iter = -1

            mixed_type_used_index = []

            fleet["boss"] = []
            fleet["butterfly"] = []
            fleet["bee"] = []

            living_fleet_idx["bee"] = []
            living_fleet_idx["butterfly"] = []
            living_fleet_idx["boss"] = []

            init_fleet_dive[0]["boss"] = []
            init_fleet_dive[0]["butterfly"] = []
            init_fleet_dive[0]["bee"] = []
            
            init_fleet_dive[1]["boss"] = []
            init_fleet_dive[1]["butterfly"] = []
            init_fleet_dive[1]["bee"] = []

            init_fleet_dive[2]["boss"] = []
            init_fleet_dive[2]["butterfly"] = []
            init_fleet_dive[2]["bee"] = []

            init_fleet_dive[3]["boss"] = []
            init_fleet_dive[3]["butterfly"] = []
            init_fleet_dive[3]["bee"] = []


            init_fleet_dive[4]["boss"] = []
            init_fleet_dive[4]["butterfly"] = []
            init_fleet_dive[4]["bee"] = []

            init_fleet_dive[5]["boss"] = []
            init_fleet_dive[5]["butterfly"] = []
            init_fleet_dive[5]["bee"] = []


        if len(player_one.gunship_buffer) > 0:
            if player_one.gunship_buffer[0].state == "Capturing":
                captureBoolean = True
                # print("Capture Boss Iter [CAPTURING]:", boss_capture_iter)
                player_one.draw(win, True, fleet["boss"][boss_capture_iter].get_pos())
            elif player_one.gunship_buffer[0].state == "Captured":
                # print("Capture Boss Iter [CAPTURED]:", boss_capture_iter)
                captureBoolean = True
                player_one.draw(win, True, fleet["boss"][boss_capture_iter].get_pos())
            elif not deathBoolean:
                player_one.draw(win)
            elif deathBoolean:
                player_one.draw(win, False)

            if debug:
                display_gunship_details(player_one, win)
                display_enemy_cnt(enemy_alive_cnt)

        try:
            if len(fleet["gunship"]) > 0:
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

        # For handling drawing the "wavebeam" and the collision with the gunship
        if len(fleet["boss"]) > 0:
            for obj in fleet["boss"][boss_capture_iter].wave_beam_buffer:
                for gunship_obj in player_one.gunship_buffer:
                    if is_collision_wave_beam(gunship_obj, obj) and (player_one.get_state() != "Capturing" and player_one.get_state() != "Captured"):
                        fleet["boss"][boss_capture_iter].captured_ship()
                        player_one.set_state("Capturing")
                        deathBoolean = True
                        capture_timer = pygame.time.get_ticks()
            # if len(fleet["boss"][boss_capture_iter].wave_beam_buffer) == 0:
            #     boss_capture_iter = -1

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
                        if is_collision(missile, enemy) and (not enemy.getDead() or enemy.health <= 0):
                            enemy.lower_health()
                            player_one.increase_shots_hit()
                            if enemy.health == 0 or enemy.health < 0:
                                if enemy.init_pos == [enemy.x, enemy.y]:
                                    if enemy_type == "bee" and not enemy.isDead:
                                        player_one.set_score(player_one.get_score() + 50)
                                    elif enemy_type == "boss" and not enemy.isDead:
                                        player_one.set_score(player_one.get_score() + 150)
                                    else:
                                        if not enemy.isDead: 
                                            player_one.set_score(player_one.get_score() + 80)
                                else:
                                    if enemy_type == "boss" and not enemy.isDead:
                                        player_one.set_score(player_one.get_score() + 400)
                                    elif enemy_type == "bee" and not enemy.isDead:
                                        player_one.set_score(player_one.get_score() + 100)
                                    else:
                                        if not enemy.isDead:
                                            player_one.set_score(player_one.get_score() + 160)
                                if enemy_type == "boss" and fleet["boss"].index(enemy) == boss_capture_iter:
                                    boss_capture_iter = -1
                                    print("Gunship should be freed")
                                    rescue_sfx1.play()
                                    fleet["gunship"][0].set_state("Returning_1")
                                    returningBoolean = True
                                    return_timer = pygame.time.get_ticks()
                                # player_one.set_score(player_one.get_score() + 100)
                                living_enemy_index = living_fleet_idx[enemy_type].index(fleet[enemy_type].index(enemy))
                                living_fleet_idx[enemy_type].pop(living_enemy_index)
                                # enemy.setDead()
                                enemy.isDead = True
                                explosion_buffer.append(Explosion(enemy.get_pos()))
                            player.missile_buffer.pop(player.missile_buffer.index(missile))
                    except Exception as e:
                        print(e)

        if debug:
            display_missile_cnt(missile_cnt)

        if pauseGame:
            paused_game()
        
        if not deathBoolean and not captureBoolean and not returningBoolean and not pauseGame:
            if keys[pygame.K_LEFT]:
                player_one.move_left()
            if keys[pygame.K_RIGHT]:
                player_one.move_right()
            if keys[pygame.K_SPACE]:
                player_one.fire_missile()
        if keys[pygame.K_x]:
            if pauseGame == True:
                pauseGame = False
            else:
                pauseGame = True 
    elif playerStatsDisplay:
        display_player_stats(player_one.shots_fired, player_one.shots_hit)

    if score_menu_y_pos >= 10:
        score_menu_y_pos -= 2
    else:
        cursorDisplay = True

    pygame.display.update()


pygame.quit()