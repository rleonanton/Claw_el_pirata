
import pygame, sys, random, os
from config import*
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

# configuracion inicial del juego
pygame.init()
clock = pygame.time.Clock()

screen_dim = pygame.display.Info()
width, height = screen_dim.current_w, screen_dim.current_h
screen = pygame.display.set_mode((width, height))
background = pygame.image.load("src/claw_images/background27.jpg")
background_width, background_height = background.get_rect().size

# creo la instancia de sounds
sounds = Sounds("src/sounds/main_sound.wav", "src/sounds/running_sound.mp3", "src/sounds/shoot_Sound.mp3", "src/sounds/sword_sound.mp3", "src/sounds/GAME OVEr.mp3")
sounds.play_main()
sounds.set_volume(0.3)

#creo el texto de pausa
text_renderer = TextRenderer(screen)
text_pausa = TextRenderer(screen)

#creo la instancia
high_scores = HighScores("src/high_score.json", width, height)

#funcion del extit game
def exit_game():
    run_menu = False
    pygame.quit()
    sys.exit()

claws = pygame.sprite.Group()
# creo la instancia del jugador principal
claw = Player(alive, jump, flip_claw, pos_x_claw, pos_y_claw, scale_claw, speed_x_claw, speed_y_claw, gravity, in_the_air, sword_attack, shoot, magic_attack, "src/claw_images/claw", qty_idle_images_claw,\
              qty_running_images_claw, qty_jump_images_claw, qty_sword_attack_images_claw, qty_shoot_images_claw, scroll_start)
claws.add(claw)

#creo los sprite groups
bullet_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()

# creo la instancia del enemigo 1
for i in range(qty_enemy):
    x = 600 + i * 100
    if i < 5:
        pos_y = pos_y_enemy1
    else:
        pos_y = pos_y_enemy2
    enemy = Enemy(enemy_alive, flip_enemy, random.randint(0, width), pos_y, scale_enemy, speed_enemy, speed_enemy, "src/claw_images/enemigos/enemigo_1", moving_left_enemy, moving_right_enemy, gravity, shots_recived,\
                  qty_idle_images_enemy, qty_walking_images_enemy, qty_attack_images_enemy, health_enemy, animation_cooldown_enemy)
    enemy_group.add(enemy)


#creo el mapa del level 1
file_name = "src/niveles/nivel1.csv"
map_level_1 = Map(file_name, tile_size, position_x_tile, speed_map)

# Crear plataformas
for row in range(map_level_1.height):
    for column in range(map_level_1.width):
        value = map_level_1.get_value(row, column)
        if value in [9, 18]:
            map_level_1.create_platform(column * map_level_1.cell_size // 2 + map_level_1.position_x, row * map_level_1.cell_size // 2 + 289, value)

all_coins = pygame.sprite.Group()

# Crear monedas aleatorias en la pantalla
for _ in range(qty_coins):
    coin_type = random.choice(["coin5", "coin10"])
    if coin_type == "coin5":
        pos_y = pos_y_coins
    else:
        pos_y = pos_y_coins - 450
    coin = Coin(random.randint(0, width), pos_y, coin_type, coin_width, coin_height)
    all_coins.add(coin)

def wait_user():
    """
    Funcion que pausa el juego y espera a que el usuario interactúe con el juego.

    Example:
        wait_user()
    """
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit_game()
                return

#creo la instancia de la barra de vida
status_bar = StatusBar(pos_x_live_bar, pos_y_live_bar, width_bar, height_bar, VIOLETA, CIAN, percentage_live, "LIVE BAR")

magic_bar = StatusBar(pos_x_magic_bar, pos_y_magic_bar, width_bar, height_bar, CIAN, VIOLETA, percentage_magic, "MAGIC BAR")

#creo la instancia de main menu
main_menu = MainMenu(screen, width, height,  "src/claw_images/background_menu.jpg", "src/claw_images/otras imagenes/claw_bg.png", "src/claw_images/claw/idle/0.png", menu_option)

# creo la instancia de la clase game_over

game_over = GameOver(screen, width, height, "src/claw_images/game over background.png", "src/claw_images/game-over-yellow_60200757f069c.png", score)

while run_menu:
        
    menu_option = main_menu.run()

    if menu_option == "INICIAR JUEGO":
        username_screen = UsernameScreen(screen, width, height)
        player_name = username_screen.run()
        main_menu.menu_option = None
        run = True

        while run:  
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game()
                
                # manejo de teclas presionadas
                if event.type == pygame.KEYDOWN:
                    
                    if event.key == pygame.K_a and claw.alive:
                        map_level_1.left_key_pressed = True
                        moving_left = True
                        sounds.play_running()

                    if event.key == pygame.K_d and claw.alive:
                        map_level_1.right_key_pressed = True
                        moving_right = True
                        sounds.play_running()

                    if event.key == pygame.K_w and not claw.in_the_air and claw.alive:
                        claw.jump = True
                        claw.in_the_air = True
                        claw.speed_y = jump_velocity
                    
                    if event.key == pygame.K_p and claw.alive:
                        text_pausa.show_text("Pausa", 100, (width // 2, height // 2), MAGENTA)
                        wait_user()

                # menejo de eventos al dejar de presionar las teclas
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        map_level_1.left_key_pressed = False
                        moving_left = False
                        
                    if event.key == pygame.K_d:
                        map_level_1.right_key_pressed = False
                        moving_right = False
                    
                    if event.key == pygame.K_w:
                        claw.jump = False

                    if event.key == pygame.K_ESCAPE:
                        exit_game()

                # manejo al presionar teclas del mouse
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and not (moving_left or moving_right):
                        claw.shoot = True
                        bullet = Bullet(claw.rect.x + x_bullet * claw.direction, claw.rect.y + y_bullet, claw.direction, speed_bullet, "src/claw_images/otras imagenes/bullet.png", width, scale_bullet,\
                                    enemy, bullet_group, is_hurt_enemy, player_is_hurt)
                        bullet_group.add(bullet)
                        sounds.play_shoot()
                        print("Presionaste el boton de disparo")

                    if event.button == 3 and not (moving_left or moving_right):
                        claw.sword_attack = True
                        print("Presionaste el boton de ataque de espada")
                        sounds.play_sword()

                #manejo al soltar las teclas del mouse
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        claw.shoot = False
                    if event.button == 3:
                        claw.sword_attack = False

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
            
    if menu_option == "VER PUNTUACIONES":

        main_menu.menu_option = None
        run_puntuaciones = True
        run_menu = False

        while run_puntuaciones:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
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

    if menu_option == "SALIR":
        exit_game()

# import pygame, sys, random, os
# from config import*
# from claw import Player
# from enemy import Enemy
# from bullet import Bullet
# from maps import Map
# from coins import Coin
# from status_bar import StatusBar
# from text_render import TextRenderer
# from menu import MainMenu
# from username import UsernameScreen
# from sounds import Sounds
# from archivos import HighScores
# from game_over import GameOver


# class Main:
#     def __init__(self, last_damage_time, current_time, damage_interval, player_name, run_menu, run, run_puntuaciones, run_game_over, score,\
#                 enemy_alive, flip_enemy, moving_left_enemy, moving_right_enemy, qty_idle_images_enemy, qty_walking_images_enemy,\
#                 qty_attack_images_enemy, health_enemy, is_hurt_enemy, speed_enemy, shots_recived, flee_health, attack_range, scale_enemy, pos_y_enemy1, pos_y_enemy2, qty_enemy,\
#                 alive, jump, flip_claw, pos_x_claw, pos_y_claw, scale_claw, speed_x_claw, speed_y_claw, gravity, in_the_air, sword_attack, shoot, magic_attack, qty_idle_images_claw,\
#                 qty_running_images_claw, qty_jump_images_claw, qty_sword_attack_images_claw, qty_shoot_images_claw, scroll_start, moving_left, moving_right, animation_cooldown_claw, animation_cooldown_enemy):
#         pygame.init()
#         self.screen_dim = pygame.display.Info()
#         self.width, self.height = self.screen_dim.current_w, self.screen_dim.current_h
#         self.screen = pygame.display.set_mode((self.width, self.height))
#         self.background = pygame.image.load("src/claw_images/background27.jpg")
#         self.background_width, self.background_height = self.background.get_rect().size
#         self.last_damage_time = last_damage_time
#         self.current_time = current_time
#         self.damage_interval = damage_interval
#         self.player_name = player_name
#         self.run_menu = run_menu
#         self.run = run
#         self.run_puntuaciones = run_puntuaciones
#         self.run_game_over = run_game_over
#         self.score = score

#         #instancio las variables del enemigo
#         self.enemy_alive = enemy_alive
#         self.flip_enemy = flip_enemy
#         self.moving_left_enemy = moving_left_enemy
#         self.moving_right_enemy = moving_right_enemy
#         self.qty_idle_images_enemy = qty_idle_images_enemy
#         self.qty_walking_images_enemy = qty_walking_images_enemy
#         self.qty_attack_images_enemy = qty_attack_images_enemy
#         self.health_enemy = health_enemy
#         self.is_hurt_enemy = is_hurt_enemy
#         self.speed_enemy = speed_enemy
#         self.shots_recived = shots_recived
#         self.flee_health = flee_health
#         self.attack_range = attack_range
#         self.scale_enemy = scale_enemy
#         self.pos_y_enemy1 = pos_y_enemy1
#         self.pos_y_enemy2 = pos_y_enemy2
#         self.qty_enemy = qty_enemy
#         self.animation_cooldown_enemy = animation_cooldown_enemy

#         #instancio las variables del jugador principal
#         self.alive = alive
#         self.jump = jump
#         self.flip_claw = flip_claw
#         self.pos_x_claw = pos_x_claw
#         self.pos_y_claw = pos_y_claw
#         self.scale_claw = scale_claw
#         self.speed_x_claw = speed_x_claw
#         self.speed_y_claw = speed_y_claw
#         self.gravity = gravity
#         self.in_the_air = in_the_air
#         self.sword_attack = sword_attack
#         self.shoot = shoot
#         self.magic_attack = magic_attack
#         self.qty_idle_images_claw = qty_idle_images_claw
#         self.qty_running_images_claw = qty_running_images_claw
#         self.qty_jump_images_claw = qty_jump_images_claw
#         self.qty_sword_attack_images_claw = qty_sword_attack_images_claw
#         self.qty_shoot_images_claw = qty_shoot_images_claw
#         self.scroll_start = scroll_start
#         self.moving_left = moving_left
#         self.moving_right = moving_right
#         self.animation_cooldown_claw = animation_cooldown_claw

#     def init_sounds(self):
#         self.sounds = Sounds("src/sounds/main_sound.wav", "src/sounds/running_sound.mp3", "src/sounds/shoot_Sound.mp3", "src/sounds/sword_sound.mp3", "src/sounds/GAME OVEr.mp3")
#         self.sounds.play_main()
#         self.sounds.set_volume(0.3)

#     def init_text(self):
#         self.text_renderer = TextRenderer(self.screen)
#         self.text_pausa = TextRenderer(self.screen)

#     def init_high_scores(self):
#         self.high_scores = HighScores("src/high_score.json", self.width, self.height)

#     def init_sprites(self):
#         self.claws = pygame.sprite.Group()
#         self.bullet_group = pygame.sprite.Group()
#         self.enemy_group = pygame.sprite.Group()

#     def init_player(self):
#         self.claw = Player(self.alive, self.jump, self.flip_claw, self.pos_x_claw, self.pos_y_claw, self.scale_claw, self.speed_x_claw, self.speed_y_claw, self.gravity, self.in_the_air, self.sword_attack, self.shoot, self.magic_attack, "src/claw_images/claw", self.qty_idle_images_claw,\
#                     self.qty_running_images_claw, self.qty_jump_images_claw, self.qty_sword_attack_images_claw, self.qty_shoot_images_claw, self.scroll_start, self.moving_left, self.moving_right, self.animation_cooldown_claw)
#         self.claws.add(self.claw)

#     def init_enemies(self):
#         for i in range(self.qty_enemy):
#             x = 600 + i * 100
#             if i < 5:
#                 pos_y = self.pos_y_enemy1
#             else:
#                 pos_y = self.pos_y_enemy2
#             self.enemy = Enemy(self.enemy_alive, self.flip_enemy, random.randint(0, self.width), pos_y, self.scale_enemy, self.speed_enemy, self.speed_enemy, "src/claw_images/enemigos/enemigo_1", self.moving_left_enemy, self.moving_right_enemy, self.gravity, self.shots_recived,\
#                         self.qty_idle_images_enemy, self.qty_walking_images_enemy, self.qty_attack_images_enemy, self.health_enemy, self.animation_cooldown_enemy)
#             self.enemy_group.add(self.enemy)

#     def init_map(self):
#         self.map_level_1 = Map("src/niveles/nivel1.csv", tile_size, position_x_tile, speed_map)
#         for row in range(self.map_level_1.height):
#             for column in range(self.map_level_1.width):
#                 value = self.map_level_1.get_value(row, column)
#                 if value in [9, 18]:
#                     self.map_level_1.create_platform(column * self.map_level_1.cell_size // 2 + self.map_level_1.position_x, row * self.map_level_1.cell_size // 2 + 289, value)

#     def init_coins(self):
#         self.all_coins = pygame.sprite.Group()
#         for _ in range(qty_coins):
#             coin_type = random.choice(["coin5", "coin10"])
#             if coin_type == "coin5":
#                 pos_y = pos_y_coins
#             else:
#                 pos_y = pos_y_coins - 450
#             self.coin = Coin(random.randint(0, self.width), pos_y, coin_type, coin_width, coin_height)
#             self.all_coins.add(self.coin)

#     def init_status_bars(self):
#         self.status_bar = StatusBar(pos_x_live_bar, pos_y_live_bar, width_bar, height_bar, VIOLETA, CIAN, percentage_live, "LIVE BAR")
#         self.magic_bar = StatusBar(pos_x_magic_bar, pos_y_magic_bar, width_bar, height_bar, CIAN, VIOLETA, percentage_magic, "MAGIC BAR")

#     def init_menu(self):
#         self.main_menu = MainMenu(self.screen, self.width, self.height,  "src/claw_images/background_menu.jpg", "src/claw_images/otras imagenes/claw_bg.png", "src/claw_images/claw/idle/0.png", menu_option)

#     def init_game_over(self):
#         self.game_over = GameOver(self.screen, self.width, self.height, "src/claw_images/game over background.png", "src/claw_images/game-over-yellow_60200757f069c.png", self.score)

#     def main(self):
#         self.clock = pygame.time.Clock()
#         self.init_sounds()
#         self.init_text()
#         self.init_high_scores()
#         self.init_sprites()
#         self.init_player()
#         self.init_enemies()
#         self.init_map()
#         self.init_coins()
#         self.init_status_bars()
#         self.init_menu()
#         self.init_game_over()

#     def handle_events(self):
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 exit_game()
#             # manejo de teclas presionadas
#             if event.type == pygame.KEYDOWN:
#                 self.handle_keydown_events(event)
#             # menejo de eventos al dejar de presionar las teclas
#             if event.type == pygame.KEYUP:
#                 self.handle_keyup_events(event)
#             # manejo al presionar teclas del mouse
#             if event.type == pygame.MOUSEBUTTONDOWN:
#                 self.handle_mousedown_events(event)
#             #manejo al soltar las teclas del mouse
#             if event.type == pygame.MOUSEBUTTONUP:
#                 self.handle_mouseup_events(event)

#     def handle_keydown_events(self, event):
#         if event.key == pygame.K_a and self.claw.alive:
#             self.map_level_1.left_key_pressed = True
#             self.claw.moving_left = True
#             self.sounds.play_running()

#         if event.key == pygame.K_d and self.claw.alive:
#             self.map_level_1.right_key_pressed = True
#             self.claw.moving_right = True
#             self.sounds.play_running()

#         if event.key == pygame.K_w and not self.claw.in_the_air and self.claw.alive:
#             self.claw.jump = True
#             self.claw.in_the_air = True
#             self.claw.speed_y = jump_velocity

#         if event.key == pygame.K_p and self.claw.alive:
#             self.text_pausa.show_text("Pausa", 100, (self.width // 2, self.height // 2), MAGENTA)
#             self.wait_user()

#     def handle_keyup_events(self, event):
#         if event.key == pygame.K_a:
#             self.map_level_1.left_key_pressed = False
#             self.claw.moving_left = False

#         if event.key == pygame.K_d:
#             self.map_level_1.right_key_pressed = False
#             self.claw.moving_right = False

#         if event.key == pygame.K_w:
#             self.claw.jump = False

#         if event.key == pygame.K_ESCAPE:
#             self.exit_game()

#     def handle_mousedown_events(self, event):
#         if event.button == 1 and not (moving_left or moving_right):
#             self.claw.shoot = True
#             bullet = Bullet(self.claw.rect.x + x_bullet * self.claw.direction, self.claw.rect.y + y_bullet, self.claw.direction, speed_bullet, "src/claw_images/otras imagenes/bullet.png", self.width, scale_bullet,\
#                             self.enemy, self.bullet_group, is_hurt_enemy, player_is_hurt)
#             self.bullet_group.add(bullet)
#             self.sounds.play_shoot()
#             print("Presionaste el boton de disparo")

#         if event.button == 3 and not (moving_left or moving_right):
#             self.claw.sword_attack = True
#             print("Presionaste el boton de ataque de espada")
#             self.sounds.play_sword()

#     def handle_mouseup_events(self, event):
#         if event.button == 1:
#             self.claw.shoot = False
#         if event.button == 3:
#             self.claw.sword_attack = False

#     def restart(self):

#         #defino las variables de movimiento del jugador principal
#         self.sword_attack = False
#         self.shoot = False
#         self.magic_attack = False
#         self.moving_right = False
#         self.moving_left = False
#         self.jump = False
#         self.in_the_air = True
#         self.alive = True
#         self.flip_claw = False
#         self.gravity = 1.25
#         self.time_last_shot = 0
#         self.shot_interval = 50
#         self.jump_velocity = -15
#         self.player_is_hurt = False
#         self.scale_claw = .45
#         self.score = [0]
#         self.damage_interval = 1000
#         self.last_damage_time = 0
#         self.current_time = 0
#         self.pos_x_claw = 200
#         self.pos_y_claw = 800
#         self.speed_x_claw = 4
#         self.speed_y_claw = 0

#         # variables para las bullet
#         self.speed_bullet = 10
#         self.scale_bullet = 15
#         self.x_bullet = 60
#         self.y_bullet = 15

#         # defino variables del enemy 1
#         self.qty_enemy = 10
#         self.enemy_alive = True
#         self.flip_enemy = False
#         self.moving_left_enemy = False
#         self.moving_right_enemy = False
#         self.health_enemy = 100
#         self.speed_enemy = 1
#         self.shots_recived = 0
#         self.flee_health = 20
#         self.attack_range = 100
#         self.scale_enemy = .40
#         self.pos_y_enemy1 = 400
#         self.pos_y_enemy2 = 800

#         #botones menu de inicio
#         self.width_menu_screen = 1000
#         self.height_menu_screen = 800
#         self.width_button = 400
#         self.height_button = 70

#         # defino un timer
#         self.animation_cooldown_claw = 50
#         self.animation_cooldown_enemy = 100

#         # variables del map
#         self.tile_size = 26
#         self.position_x_tile = 0
#         self.speed_map = 2
#         self.multiplier_scroll = 1.68 
#         self.scroll_start = False

#         # defino variables de los coins
#         self.qty_coins = 10
#         self.coin_width = 16
#         self.coin_height = 16
#         self.pos_y_coins = 720

#         #-----coordenadas del background
#         self.background_x = 0
#         self.background_y = 0

#         #-----variables del status bar
#         self.pos_x_live_bar = 100
#         self.pos_y_live_bar = 100
#         self.width_bar = 150
#         self.height_bar = 25
#         self.percentage_live = 100
#         self.percentage_magic = 0
#         self.pos_x_magic_bar = 100
#         self.pos_y_magic_bar = 160

#         self.enemy_group.empty()
#         self.claws.empty()
#         self.init_coins()
#         self.init_enemies()
#         self.init_player()
#         self.init_sprites()
#         self.init_status_bars()

#     def run_game(self):
        
#         # Dibujar el background
#         self.screen.blit(self.background, (0,-420))
#         self.status_bar.draw_bar(self.screen)
#         self.magic_bar.draw_bar(self.screen)
        
#         #dibujo las plataformas
#         for platform in self.map_level_1.platforms_group:
#             self.screen.blit(platform.image, (platform.rect.x + self.map_level_1.position_x, platform.rect.y))

#         # dibujo y actualizo al personaje principal y el enemigo_1
#         self.claw.update_animation()
#         self.claw.draw(self.screen)
#         self.claw.move(self.map_level_1.platforms_group, self.map_level_1, self.width)
        
#         # actualizo constantemente la posicion de claw
#         self.claw.player_pos = (self.claw.rect.x, self.claw.rect.y)

#         self.all_coins.update()  # Actualizar la animación de las monedas
#         self.all_coins.draw(self.screen)  # Dibujar las monedas en la pantalla

#         # dibujo y actualizo las bullets
#         self.bullet_group.update()
#         self.bullet_group.draw(self.screen)
        
#         # verificacion de bullets y enemigos
#         for enemy in self.enemy_group:
#             enemy.ai(self.claw, self.map_level_1.platforms_group, self.width, self.map_level_1)
#             collisions = pygame.sprite.groupcollide(self.bullet_group, self.enemy_group, True, False)
#             self.current_time = pygame.time.get_ticks()
#             if self.current_time - self.last_damage_time >= self.damage_interval:
#                 if pygame.sprite.collide_rect(self.claw, enemy):
#                     self.status_bar.percentage -= 10
#                     self.status_bar.update_percentage(self.status_bar.percentage)
#                     self.last_damage_time = self.current_time
#                     if self.status_bar.percentage == 0:
#                         self.high_scores.update_high_scores(self.player_name, score[0])
#                         self.high_scores.save_high_score(self.player_name, score[0])
#                         self.sounds.play_game_over()
#                         restart_option = self.game_over.run(self.player_name)
#                         if restart_option == "REINICIAR":
#                             self.restart()

#             for bullet in collisions:
#                 for enemy in collisions[bullet]:
#                     enemy.shots_recived += 1
#                     if enemy.shots_recived >= 2:
#                         print("¡Enemigo eliminado!")
#                         score[0] += 25
#                         self.enemy_group.remove(enemy)
#             enemy.update_animation()
#             enemy.draw(self.screen)

#         # Detección de colisiones
#         collisions = pygame.sprite.groupcollide(self.claws, self.all_coins, False, True)

#         # Manejar las colisiones
#         for player, coins in collisions.items():
#             for coin in coins:
#                 if coin.coin_type == "coin5":
#                     # Manejar colisión con moneda de 5 unidades
#                     score[0] += 5
#                     print("El jugador chocó con una moneda de 5 unidades")
#                 elif coin.coin_type == "coin10":
#                     # Manejar colisión con moneda de 10 unidades
#                     score[0] += 10
#                     print("El jugador chocó con una moneda de 10 unidades")

#         if self.claw.alive:
#             if self.claw.shoot and self.claw.direction == 1:
#                 self.claw.update_action(4) # 4 es disparo
#             elif self.claw.shoot and self.claw.direction == -1:
#                 self.claw.update_action(4) # 4 es disparo
#             elif self.claw.sword_attack:
#                 self.claw.update_action(3) # 3 es taque de espada
#             elif self.claw.in_the_air:
#                 self.claw.update_action(2) # 2 es saltar
#             elif self.claw.moving_left or self.claw.moving_right:
#                 self.claw.update_action(1) # 1 es correr
#             else:
#                 self.claw.update_action(0) # 0 es idle
#         self.clock.tick(FPS)
        
#         self.text_renderer.show_text(f"Score: {score[0]}     Player: {self.player_name}", 45, (self.width // 2, 100), VIOLETA)
#         # Actualizo la pantalla
#         pygame.display.flip()

#     def run_main(self):
 
#         while self.run_menu:
#             menu_option = self.main_menu.run()

#             if menu_option == "INICIAR JUEGO":
#                 username_screen = UsernameScreen(self.screen, self.width, self.height)
#                 self.player_name = username_screen.run()
#                 self.main_menu.menu_option = None
#                 self.run = True
                
#                 while self.run:  
#                     self.handle_events()
#                     self.run_game()

#             if menu_option == "VER PUNTUACIONES":

#                 self.main_menu.menu_option = None
#                 self.run_puntuaciones = True
#                 self.run_menu = False

#                 while self.run_puntuaciones:
#                     for event in pygame.event.get():
#                         if event.type == pygame.QUIT:
#                             self.exit_game()
#                         elif event.type == pygame.MOUSEBUTTONDOWN:
#                             x, y = pygame.mouse.get_pos()
#                             if button_start_rect.collidepoint(x, y):
#                                 self.run_puntuaciones = False
#                                 self.run_menu = True
                                
#                     self.screen.fill(NEGRO)

#                     self.high_scores.show_high_scores(self.screen, RED)
#                     # Dibuja un botón para volver al menú principal
#                     button_start_rect = pygame.Rect(self.width // 2 - width_button // 2, self.height // 2 + height_button, width_button, height_button)
                    
#                     # Aplica la misma lógica de interacción con el ratón
#                     if button_start_rect.collidepoint(pygame.mouse.get_pos()):
#                         pygame.draw.rect(self.screen, AZUL, button_start_rect, border_radius=25)
#                     else:
#                         pygame.draw.rect(self.screen, VERDE, button_start_rect, border_radius=25)
                    
#                     font = pygame.font.Font(None, 36)
#                     text_surface = font.render("Volver al menú", True, BLANCO)
#                     text_rect = text_surface.get_rect(center=button_start_rect.center)
#                     self.screen.blit(text_surface, text_rect.topleft)

#                     pygame.display.update()

#             if menu_option == "SALIR":
#                 self.exit_game()

#     def wait_user(self):

#         while True:
#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     self.exit_game()
#                 if event.type == pygame.KEYDOWN:
#                     if event.key == pygame.K_ESCAPE:
#                         self.exit_game()
#                     return

#     def exit_game(self):
#         self.run_menu = False
#         pygame.quit()
#         sys.exit()


# if __name__ == "__main__":
#     game = Main(last_damage_time, current_time, damage_interval, player_name, run_menu, run, run_puntuaciones, run_game_over, score,\
#                 enemy_alive, flip_enemy, moving_left_enemy, moving_right_enemy, qty_idle_images_enemy, qty_walking_images_enemy, qty_attack_images_enemy,\
#                 health_enemy, is_hurt_enemy, speed_enemy, shots_recived, flee_health, attack_range, scale_enemy, pos_y_enemy1, pos_y_enemy2, qty_enemy, \
#                 alive, jump, flip_claw, pos_x_claw, pos_y_claw, scale_claw, speed_x_claw, speed_y_claw, gravity, in_the_air, sword_attack, shoot, magic_attack,\
#                 qty_idle_images_claw, qty_running_images_claw, qty_jump_images_claw, qty_sword_attack_images_claw, qty_shoot_images_claw, scroll_start,\
#                 moving_left, moving_right, animation_cooldown_claw, animation_cooldown_enemy)
#     game.main() 
#     game.run_main()
