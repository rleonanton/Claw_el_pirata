import pygame, sys, random, os
from config import *
from claw import Player
from enemy import Enemy
from bullet import Bullet
from maps import Map
from coins import Coin
from status_bar import StatusBar
from text_render import TextRenderer
from menu import MainMenu
from username import UsernameScreen
from sounds import Sounds
from archivos import HighScores
from game_over import GameOver
from game import Game


class Main:
    def __init__(self):

        pygame.init()
        self.clock = pygame.time.Clock()

        screen_dim = pygame.display.Info()
        self.width, self.height = screen_dim.current_w, screen_dim.current_h
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.background = pygame.image.load("src/claw_images/background27.jpg")
        self.background_width, self.background_height = self.background.get_rect().size

        self.sounds = Sounds("src/sounds/main_sound.wav", "src/sounds/running_sound.mp3", "src/sounds/shoot_Sound.mp3", "src/sounds/sword_sound.mp3", "src/sounds/GAME OVEr.mp3")
        self.sounds.play_main()
        self.sounds.set_volume(0.3)

        self.text_renderer = TextRenderer(self.screen)
        self.text_pausa = TextRenderer(self.screen)

        self.high_scores = HighScores("src/high_score.json", self.width, self.height)

        self.claws = pygame.sprite.Group()
        self.claw = Player(alive, self.jump, self.flip_claw, self.pos_x_claw, self.pos_y_claw, self.scale_claw, self.speed_x_claw, self.speed_y_claw, self.gravity, self.in_the_air, self.sword_attack, self.shoot, self.magic_attack, "src/claw_images/claw", self.qty_idle_images_claw,\
                    self.qty_running_images_claw, self.qty_jump_images_claw, self.qty_sword_attack_images_claw, self.qty_shoot_images_claw, self.scroll_start)
        self.claws.add(self.claw)

        self.bullet_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()

        for i in range(self.qty_enemy):
            x = 600 + i * 100
            if i < 5:
                pos_y = self.pos_y_enemy1
            else:
                pos_y = self.pos_y_enemy2
            enemy = Enemy(self.enemy_alive, self.flip_enemy, random.randint(0, self.width), pos_y, self.scale_enemy, self.speed_enemy, self.speed_enemy, "src/claw_images/enemigos/enemigo_1", self.moving_left_enemy, self.moving_right_enemy, self.gravity, self.shots_recived,\
                        self.qty_idle_images_enemy, self.qty_walking_images_enemy, self.qty_attack_images_enemy, self.health_enemy, self.animation_cooldown_enemy)
            self.enemy_group.add(enemy)

        self.map_level_1 = Map("src/niveles/nivel1.csv", self.tile_size, self.position_x_tile, self.speed_map)

        for row in range(self.map_level_1.height):
            for column in range(self.map_level_1.width):
                value = self.map_level_1.get_value(row, column)
                if value in [9, 18]:
                    self.map_level_1.create_platform(column * self.map_level_1.cell_size // 2 + self.map_level_1.position_x, row * self.map_level_1.cell_size // 2 + 289, value)

        self.all_coins = pygame.sprite.Group()

        for _ in range(self.qty_coins):
            coin_type = random.choice(["coin5", "coin10"])
            if coin_type == "coin5":
                pos_y = self.pos_y_coins
            else:
                pos_y = self.pos_y_coins - 450
            coin = Coin(random.randint(0, self.width), pos_y, coin_type, self.coin_width, self.coin_height)
            self.all_coins.add(coin)

        self.status_bar = StatusBar(self.pos_x_live_bar, self.pos_y_live_bar, self.width_bar, self.height_bar, self.VIOLETA, self.CIAN, self.percentage_live, "LIVE BAR")
        self.magic_bar = StatusBar(self.pos_x_magic_bar, self.pos_y_magic_bar, self.width_bar, self.height_bar, self.CIAN, self.VIOLETA, self.percentage_magic, "MAGIC BAR")

        self.main_menu = MainMenu(self.screen, self.width, self.height,  "src/claw_images/background_menu.jpg", "src/claw_images/otras imagenes/claw_bg.png", "src/claw_images/claw/idle/0.png", self.menu_option)

        self.game_over = GameOver(self.screen, self.width, self.height, "src/claw_images/game over background.png", "src/claw_images/game-over-yellow_60200757f069c.png", self.score)



    def run(self):

        while self.run_menu:
            menu_option = self.main_menu.run()

            if menu_option == "INICIAR JUEGO":
                username_screen = UsernameScreen(self.screen, self.width, self.height)
                player_name = username_screen.run()
                self.main_menu.menu_option = None
                self.run = True

                while self.run:  
                        
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            self.exit_game()
                        
                        # manejo de teclas presionadas
                        if event.type == pygame.KEYDOWN:
                            
                            if event.key == pygame.K_a and self.claw.alive:
                                self.map_level_1.left_key_pressed = True
                                self.moving_left = True
                                self.sounds.play_running()

                            if event.key == pygame.K_d and self.claw.alive:
                                self.map_level_1.right_key_pressed = True
                                self.moving_right = True
                                self.sounds.play_running()

                            if event.key == pygame.K_w and not self.claw.in_the_air and self.claw.alive:
                                self.claw.jump = True
                                self.claw.in_the_air = True
                                self.claw.speed_y = self.jump_velocity
                            
                            if event.key == pygame.K_p and self.claw.alive:
                                self.text_pausa.show_text("Pausa", 100, (self.width // 2, self.height // 2), self.MAGENTA)
                                self.wait_user()

                        # menejo de eventos al dejar de presionar las teclas
                        if event.type == pygame.KEYUP:
                            if event.key == pygame.K_a:
                                self.map_level_1.left_key_pressed = False
                                self.moving_left = False
                                
                            if event.key == pygame.K_d:
                                self.map_level_1.right_key_pressed = False
                                self.moving_right = False
                            
                            if event.key == pygame.K_w:
                                self.claw.jump = False

                            if event.key == pygame.K_ESCAPE:
                                self.exit_game()

                        # manejo al presionar teclas del mouse
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if event.button == 1 and not (self.moving_left or self.moving_right):
                                self.claw.shoot = True
                                bullet = Bullet(self.claw.rect.x + self.x_bullet * self.claw.direction, self.claw.rect.y + self.y_bullet, self.claw.direction, self.speed_bullet, "src/claw_images/otras imagenes/bullet.png", self.width, self.scale_bullet,\
                                            self.enemy, self.bullet_group, self.is_hurt_enemy, self.player_is_hurt)
                                self.bullet_group.add(bullet)
                                self.sounds.play_shoot()
                                print("Presionaste el botón de disparo")

                            if event.button == 3 and not (self.moving_left or self.moving_right):
                                self.claw.sword_attack = True
                                print("Presionaste el botón de ataque de espada")
                                self.sounds.play_sword()

                        # manejo al soltar las teclas del mouse
                        if event.type == pygame.MOUSEBUTTONUP:
                            if event.button == 1:
                                self.claw.shoot = False
                            if event.button == 3:
                                self.claw.sword_attack = False

            # Resto del código para mostrar puntuaciones


                # Dibujar el background
                screen.blit(background, (0,-420))
                status_bar.draw_bar(screen)
                magic_bar.draw_bar(screen)
                    
                #dibujo las plataformas
                for platform in map_level_1.platforms_group:
                    screen.blit(platform.image, (platform.rect.x + map_level_1.position_x, platform.rect.y))

                # dibujo y actualizo al personaje principal y el enemigo_1
                claw.update_animation(animation_cooldown_claw)
                claw.draw(screen)
                claw.move(moving_left, moving_right, map_level_1.platforms_group, map_level_1, width)
                
                # actualizo constantemente la posicion de claw
                player_pos = (claw.rect.x, claw.rect.y)

                all_coins.update()  # Actualizar la animación de las monedas
                all_coins.draw(screen)  # Dibujar las monedas en la pantalla

                # dibujo y actualizo las bullets
                bullet_group.update()
                bullet_group.draw(screen)
                
                # verificacion de bullets y enemigos
                for enemy in enemy_group:
                    enemy.ai(claw, map_level_1.platforms_group, width, map_level_1)
                    collisions = pygame.sprite.groupcollide(bullet_group, enemy_group, True, False)
                    current_time = pygame.time.get_ticks()
                    if current_time - last_damage_time >= damage_interval:
                        if pygame.sprite.collide_rect(claw, enemy):
                            percentage_live -= 10
                            status_bar.update_percentage(percentage_live)
                            last_damage_time = current_time
                            if percentage_live == 0:
                                high_scores.update_high_scores(player_name, score[0])
                                high_scores.save_high_score(player_name, score[0])
                                sounds.play_game_over()
                                restart_option = game_over.run(player_name)
                                if restart_option == "REINICIAR":
                                    restart()

                    for bullet in collisions:
                        for enemy in collisions[bullet]:
                            enemy.shots_recived += 1
                            if enemy.shots_recived >= 2:
                                print("¡Enemigo eliminado!")
                                score[0] += 25
                                enemy_group.remove(enemy)
                    enemy.update_animation()
                    enemy.draw(screen)

                # Detección de colisiones
                collisions = pygame.sprite.groupcollide(claws, all_coins, False, True)

                # Manejar las colisiones
                for player, coins in collisions.items():
                    for coin in coins:
                        if coin.coin_type == "coin5":
                            # Manejar colisión con moneda de 5 unidades
                            score[0] += 5
                            print("El jugador chocó con una moneda de 5 unidades")
                        elif coin.coin_type == "coin10":
                            # Manejar colisión con moneda de 10 unidades
                            score[0] += 10
                            print("El jugador chocó con una moneda de 10 unidades")

                # verifico que esta haciendo (la accion) mi personajea
                if claw.alive:
                    if claw.shoot and claw.direction == 1:
                        claw.update_action(4) # 4 es disparo
                    elif claw.shoot and claw.direction == -1:
                        claw.update_action(4) # 4 es disparo
                    elif claw.sword_attack:
                        claw.update_action(3) # 3 es taque de espada
                    elif claw.in_the_air:
                        claw.update_action(2) # 2 es saltar
                    elif moving_left or moving_right:
                        claw.update_action(1) # 1 es correr
                    else:
                        claw.update_action(0) # 0 es idle
                clock.tick(FPS)
                
                text_renderer.show_text(f"Score: {score[0]}     Player: {player_name}", 45, (width // 2, 100), VIOLETA)
                # Actualizo la pantalla
                pygame.display.flip()
                
        elif menu_option == "VER PUNTUACIONES":
            self.main_menu.menu_option = None
            run_puntuaciones = True
            self.run_menu = False

            while run_puntuaciones:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.exit_game()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        x, y = pygame.mouse.get_pos()
                        if button_start_rect.collidepoint(x, y):
                            run_puntuaciones = False
                            run_menu = True
                            
                screen.fill(NEGRO)

                high_scores.show_high_scores(screen, RED)
                # Dibuja un botón para volver al menú principal
                button_start_rect = pygame.Rect(width // 2 - width_button // 2, height // 2 + height_button, width_button, height_button)
                
                # Aplica la misma lógica de interacción con el ratón
                if button_start_rect.collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.rect(screen, AZUL, button_start_rect, border_radius=25)
                else:
                    pygame.draw.rect(screen, VERDE, button_start_rect, border_radius=25)
                
                font = pygame.font.Font(None, 36)
                text_surface = font.render("Volver al menú", True, BLANCO)
                text_rect = text_surface.get_rect(center=button_start_rect.center)
                screen.blit(text_surface, text_rect.topleft)

                pygame.display.update()



def exit_game(self):
    pygame.quit()
    sys.exit()
