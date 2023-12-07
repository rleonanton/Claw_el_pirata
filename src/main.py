import pygame, sys, random, time
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
from level_menu import LevelMenu
from especial_items import SpecialItem
from magic_attack import MagicAttack
from timer import Timer
from button import Button
from trampas import Trap
from sqlite import Sqlite
from final_boss import FinalBoss

class Main:
    def __init__(self, last_damage_time, current_time, damage_interval, player_name, run_menu, run, run_puntuaciones, run_game_over, score):

        pygame.init()
        self.screen_dim = pygame.display.Info()
        self.width, self.height = self.screen_dim.current_w, self.screen_dim.current_h
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.background = pygame.image.load("src/claw_images/background27.jpg")
        self.background_width, self.background_height = self.background.get_rect().size
        self.background_2 = pygame.transform.scale(pygame.image.load("src/claw_images/mar_final level.png"), (self.width, 150))
        self.background_2_width, self.background_2_height = self.background_2.get_rect().size
        self.background_bg = pygame.transform.scale(pygame.image.load("src/claw_images/pngwing.com (2).png").convert_alpha(), (self.width, self.height))
        self.background_bg_width, self.background_bg_height = self.background_bg.get_rect().size
        self.last_damage_time = last_damage_time
        self.current_time = current_time
        self.damage_interval = damage_interval
        self.player_name = player_name
        self.run_menu = run_menu
        self.run = run
        self.run_puntuaciones = run_puntuaciones
        self.run_game_over = run_game_over
        self.score = score
        self.level = None

    def init_sounds(self):
        self.sounds = Sounds("src/sounds/main_sound.wav", "src/sounds/running_sound.mp3", "src/sounds/shoot_Sound.mp3", "src/sounds/sword_sound.mp3", "src/sounds/GAME OVEr.mp3", "src/sounds/magic_sound.mp3",\
                            "src/sounds/sonido cañon final boss.mp3", "src/sounds/you win.mp3")
        self.sounds.play_main()
        self.sounds.set_volume(volumen)

    def init_text(self):
        self.text_renderer = TextRenderer(self.screen)
        self.text_pausa = TextRenderer(self.screen)

    def init_timer(self):
        self.timer = Timer(1700, 100, 36, BLANCO, None)

    def init_high_scores(self):
        self.high_scores = HighScores("src/high_score.json", self.width, self.height, "src/claw_images/backgroun_puntajes.jpg", "src/claw_images/pngwing.com (3)/top0.png",\
                                    "src/claw_images/pngwing.com (3)/top1.png", "src/claw_images/pngwing.com (3)/top2.png")

    def init_sqlite(self):
        self.sqlite = Sqlite(self.width, self.height)
        self.sqlite.load_scores_from_json("src/high_score.json")

    def init_sprites(self):

        self.bullet_group = pygame.sprite.Group()
        self.magic_attack_group = pygame.sprite.Group()

    def init_player(self):
        self.claws = pygame.sprite.Group()
        self.claw = Player(alive, jump, flip_claw, pos_x_claw, pos_y_claw, scale_claw, speed_x_claw, speed_y_claw, gravity, in_the_air, sword_attack, shoot, magic_attack, "src/claw_images/claw", qty_idle_images_claw,\
                    qty_running_images_claw, qty_jump_images_claw, qty_sword_attack_images_claw, qty_shoot_images_claw, qty_magic_attack_images, scroll_start, moving_left, moving_right, animation_cooldown_claw)
        self.claws.add(self.claw)

    def init_enemies(self, level):
        self.enemy_group = pygame.sprite.Group()

        for i in range(qty_enemy):
            x = 600 + i * 100
            if level == "NIVEL 3":
                pos_y = pos_y_enemy1  # Solo usa una posición para el NIVEL 3
            else:
                if i < 5:
                    pos_y = pos_y_enemy1
                else:
                    pos_y = pos_y_enemy2

            if level == "NIVEL 1":
                enemy = Enemy(enemy_alive, flip_enemy, random.randint(0, self.width), pos_y, scale_enemy, speed_enemy, speed_enemy, "src/claw_images/enemigos/enemigo_1", moving_left_enemy, moving_right_enemy, gravity, shots_recived,\
                            qty_idle_images_enemy, qty_moving_images_enemy, qty_attack_images_enemy, 0, health_enemy, damage_enemy_1, animation_cooldown_enemy, width_bar_enemy_1,\
                                height_bar_enemy_1, percentage_live_enemy, VIOLETA, CIAN, "LIVE BAR", 10)
                self.enemy_group.add(enemy)

            elif level == "NIVEL 2":
                enemy = Enemy(enemy_alive_2, flip_enemy_2, random.randint(0, self.width), pos_y, scale_enemy_2, speed_enemy_2, speed_enemy_2, "src/claw_images/enemigos/enemigo_2",\
                            moving_left_enemy_2, moving_right_enemy_2, gravity, shots_recived_2, qty_idle_images_enemy_2, qty_moving_images_enemy_2, qty_attack_images_enemy_2, qty_death_images_enemy_2,\
                            health_enemy_2, damage_enemy_2, animation_cooldown_enemy, width_bar_enemy_1, height_bar_enemy_1, percentage_live_enemy, VIOLETA, CIAN, "LIVE BAR", 10)
                self.enemy_group.add(enemy)

            elif level == "NIVEL 3":
                enemy = Enemy(enemy_alive_2, flip_enemy_2, random.randint(600, self.width), pos_y, scale_enemy_2, speed_enemy_2, speed_enemy_2, "src/claw_images/enemigos/enemigo_2",\
                            moving_left_enemy_2, moving_right_enemy_2, gravity, shots_recived_2, qty_idle_images_enemy_2, qty_moving_images_enemy_2, qty_attack_images_enemy_2, qty_death_images_enemy_2,\
                            health_enemy_2, damage_enemy_2, animation_cooldown_enemy, width_bar_enemy_1, height_bar_enemy_1, percentage_live_enemy, VIOLETA, CIAN, "LIVE BAR", 10)
                self.enemy_group.add(enemy)

            else:
                raise ValueError(f"Nivel desconocido: {level}")
            
    def init_final_boss(self):
        self.final_boss = FinalBoss(pos_x_final_boss, pos_y_final_boss, self.width, self.height, "src/claw_images/Imagen2.png", self.screen)

    def init_map(self, level):

        if level == "NIVEL 1":
            self.map_level = Map("src/niveles/nivel1.csv", tile_size, position_x_tile, speed_map)
            for row in range(self.map_level.height):
                for column in range(self.map_level.width):
                    value = self.map_level.get_value(row, column)
                    if value in [9, 18]:
                        self.map_level.create_platform(column * self.map_level.cell_size // 2 + self.map_level.position_x, row * self.map_level.cell_size // 2 + 289, value)
            self.level = level
        elif level == "NIVEL 2":
            self.map_level = Map("src/niveles/nivel2.csv", tile_size, position_x_tile, speed_map)
            for row in range(self.map_level.height):
                for column in range(self.map_level.width):
                    value = self.map_level.get_value(row, column)
                    if value in [1235, 1429]:
                        self.map_level.create_platform(column * self.map_level.cell_size // 2 + self.map_level.position_x, row * self.map_level.cell_size // 2 + 289, value)
            self.level = level
        
        elif level == "NIVEL 3":
            self.map_level = Map("src/niveles/nivel3.csv", tile_size, position_x_tile, speed_map)
            for row in range(self.map_level.height):
                for column in range(self.map_level.width):
                    value = self.map_level.get_value(row, column)
                    if value in [147, 181]:
                        self.map_level.create_platform(column * self.map_level.cell_size // 2 + self.map_level.position_x, row * self.map_level.cell_size // 2 - 100, value)
            self.level = level
        else:
            raise ValueError(f"Nivel desconocido: {level}")

    def init_coins(self):
        self.all_coins = pygame.sprite.Group()
        if self.level == "NIVEL 1" or self.level == "NIVEL 2":
            for _ in range(qty_coins):
                coin_type = random.choice(["coin5", "coin10"])
                if coin_type == "coin5":
                    pos_y = pos_y_coins
                else:
                    pos_y = pos_y_coins - 450
                self.coin = Coin(random.randint(0, self.width), pos_y, coin_type, coin_width, coin_height)
                self.all_coins.add(self.coin)
        
        else:
            for _ in range(qty_coins):
                coin_type = random.choice(["coin5", "coin10"])
                if coin_type == "coin5":
                    pos_y = pos_y_coins_level_3
                else:
                    pos_y = pos_y_coins_level_3
                self.coin = Coin(random.randint(700, self.width), pos_y, coin_type, coin_width, coin_height)
                self.all_coins.add(self.coin)
                print(self.level)

    def init_status_bars(self):
        self.status_bar = StatusBar(pos_x_live_bar, pos_y_live_bar, width_bar, height_bar, VIOLETA, CIAN, percentage_live, "LIVE BAR", 38)
        self.magic_bar = StatusBar(pos_x_magic_bar, pos_y_magic_bar, width_bar, height_bar, CIAN, VIOLETA, percentage_magic, "MAGIC BAR", 38)
        
    def init_especial_items(self):
        self.special_items = pygame.sprite.Group()
        if self.level == "NIVEL 1" or self.level == "NIVEL 2":
            x_life = pos_x_special_item
            x_magic = pos_x_special_item + 200 
            for _ in range(3):  # Crea 3 elementos de cada tipo
                # Vida
                x_life += 100
                special_item = SpecialItem(self.screen, x_life, pos_y_especial_item, "src/claw_images/vida.png", "life", scale_special_items)
                self.special_items.add(special_item)
                # Magia
                x_magic += 250
                special_item = SpecialItem(self.screen, x_magic, pos_y_especial_item, "src/claw_images/magia.png", "magic", scale_special_items)
                self.special_items.add(special_item)
        else:
            x_life = pos_x_special_item_level_3
            x_magic = pos_x_special_item_level_3 + 200 
            for _ in range(3):  # Crea 3 elementos de cada tipo
                # Vida
                x_life += 100
                special_item = SpecialItem(self.screen, x_life, pos_y_especial_item_level_3, "src/claw_images/vida.png", "life", scale_special_items)
                self.special_items.add(special_item)
                # Magia
                x_magic += 250
                special_item = SpecialItem(self.screen, x_magic, pos_y_especial_item_level_3, "src/claw_images/magia.png", "magic", scale_special_items)
                self.special_items.add(special_item)

    def init_traps(self):
        self.traps = pygame.sprite.Group()
        if self.level == "NIVEL 1":
            trap1 = Trap("src/claw_images/spikes.png", 570, 896)
            self.traps.add(trap1)

            trap2 = Trap("src/claw_images/spikes.png", 1170, 910)
            self.traps.add(trap2)

            trap3 = Trap("src/claw_images/spikes.png", 1500, 910)
            self.traps.add(trap3)

            trap4 = Trap("src/claw_images/spikes.png", 400, 387)
            self.traps.add(trap4)

            trap5 = Trap("src/claw_images/spikes.png", 1170, 400)
            self.traps.add(trap5)
        
        elif self.level == "NIVEL 2":
            trap1 = Trap("src/claw_images/spikes.png", 570, 570)
            self.traps.add(trap1)

            trap2 = Trap("src/claw_images/spikes.png", 1170, 570)
            self.traps.add(trap2)

            trap3 = Trap("src/claw_images/spikes.png", 1500, 673)
            self.traps.add(trap3)

            trap4 = Trap("src/claw_images/spikes.png", 670, 867)
            self.traps.add(trap4)

        else:
            print("VINO a parar aqui")
            trap1 = Trap("src/claw_images/spikes.png", 435, 690)
            self.traps.add(trap1)

            trap2 = Trap("src/claw_images/spikes.png", 1170, 455)
            self.traps.add(trap2)

            trap3 = Trap("src/claw_images/spikes.png", 1700, 455)
            self.traps.add(trap3)

    def init_menu(self):
        self.main_menu = MainMenu(self.screen, self.width, self.height,  "src/claw_images/background_menu.jpg", "src/claw_images/otras imagenes/claw_bg.png", "src/claw_images/menu_image.png", menu_option)

    def init_game_over(self):
        self.game_over = GameOver(self.screen, self.width, self.height, "src/claw_images/game over background.png", "src/claw_images/game-over-yellow_60200757f069c.png", self.score)

    def init_win(self):
        self.win = GameOver(self.screen, self.width, self.height, "src/claw_images/game over background.png", "src\claw_images\you win.png", self.score)

    def wait_user(self):

        # Define los botones
        button_return = Button(self.width // 2 - width_button // 2, 100, width_button, height_button, GRIS, NEGRO, "RETURN TO GAME")
        button_return_menu = Button(self.width // 2 - width_button // 2, 200, width_button, height_button, GRIS, NEGRO, "RETURN TO MENU")
        button_config = Button(self.width // 2 - width_button // 2, 300, width_button, height_button, GRIS, NEGRO, "CONFIG")
        button_exit = Button(self.width // 2 - width_button // 2, 400, width_button, height_button, GRIS, NEGRO, "EXIT GAME")

        run_wait_user = True
        while run_wait_user:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit_game()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.exit_game()

                # Verifica si se hizo clic en alguno de los botones
                if button_config.is_clicked(event):
                    self.show_config_screen()
                    print("Botón de configuración presionado")  
                elif button_exit.is_clicked(event):
                    self.exit_game()
                elif button_return_menu.is_clicked(event):
                    self.run_main()
                    print("Boton de regresar al menú presionado")
                    run_wait_user = False
                elif button_return.is_clicked(event):
                    print("Botón de regresar presionado") 
                    self.timer.unpause()
                    run_wait_user = False

            # Dibuja los botones
            button_config.draw(self.screen)
            button_exit.draw(self.screen)
            button_return.draw(self.screen)
            button_return_menu.draw(self.screen)

            pygame.display.flip()  # Actualiza la pantalla
    
    def show_config_screen(self):

        button_sound_down = Button(self.width // 2 - width_button // 2, self.height // 2 - 2 * height_button, width_button, height_button, GRIS, NEGRO, "SONIDO DOWN")  # Ajusta las coordenadas y el tamaño según tus necesidades
        button_sound_on = Button(self.width // 2 - width_button // 2, self.height // 2 - height_button // 2, width_button, height_button, GRIS, NEGRO, "SONIDO ON")
        button_sound_off = Button(self.width // 2 - width_button // 2, self.height // 2 + height_button, width_button, height_button, GRIS, NEGRO, "SONIDO OFF")
        button_back_to_menu = Button(self.width // 2 - width_button // 2, self.height // 2 + 2.5 * height_button, width_button, height_button, GRIS, NEGRO, "REGRESAR")
        button_exit = Button(self.width // 2 - width_button // 2, self.height // 2 + 5 * height_button, width_button, height_button, GRIS, NEGRO, "SALIR DEL JUEGO")

            # button_start_rect = pygame.Rect()
            # button_scores_rect = pygame.Rect(self.width // 2 - width_button // 2, self.height // 2 - height_button // 2, width_button, height_button)
            # button_niveles_rect = pygame.Rect(self.width // 2 - width_button // 2, self.height // 2 + height_button, width_button, height_button)
            # button_configuracion_rect = pygame.Rect(self.width // 2 - width_button // 2, self.height // 2 + 2.5 * height_button, width_button, height_button)
            # button_exit_rect = pygame.Rect(self.width // 2 - width_button // 2, self.height // 2 + 5 * height_button, width_button, height_button)


        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit_game()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return
                elif button_sound_down.is_clicked(event):
                    self.sounds.set_volume(volumen - 0.3)
                elif button_sound_on.is_clicked(event):
                    self.sounds.set_volume(1.0)  # Asume que 'self.sounds' es una instancia de tu clase 'Sounds'
                elif button_sound_off.is_clicked(event):
                    self.sounds.set_volume(0.0)
                elif button_exit.is_clicked(event):
                    self.exit_game()
                elif button_back_to_menu.is_clicked(event):
                    return

            
            button_sound_on.draw(self.screen)
            button_sound_off.draw(self.screen)
            button_sound_down.draw(self.screen)
            button_back_to_menu.draw(self.screen)
            button_exit.draw(self.screen)

            pygame.display.flip()

    def main(self):
        self.clock = pygame.time.Clock()
        self.init_sounds()
        self.init_text()
        self.init_high_scores()
        self.init_sprites()
        self.init_player()
        self.init_status_bars()
        self.init_menu()
        self.init_game_over()
        self.init_win()
        self.init_timer()
        # self.init_final_boss()
        # self.init_sqlite()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit_game()
            # manejo de teclas presionadas
            if event.type == pygame.KEYDOWN:
                self.handle_keydown_events(event)
            # menejo de eventos al dejar de presionar las teclas
            if event.type == pygame.KEYUP:
                self.handle_keyup_events(event)
            # manejo al presionar teclas del mouse
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mousedown_events(event)
            #manejo al soltar las teclas del mouse
            if event.type == pygame.MOUSEBUTTONUP:
                self.handle_mouseup_events(event)

    def handle_keydown_events(self, event):
        if event.key == pygame.K_a and self.claw.alive:
            self.map_level.left_key_pressed = True
            self.claw.moving_left = True
            self.sounds.play_running()

        if event.key == pygame.K_d and self.claw.alive:
            self.map_level.right_key_pressed = True
            self.claw.moving_right = True
            self.sounds.play_running()

        if event.key == pygame.K_w and not self.claw.in_the_air and self.claw.alive:
            self.claw.jump = True
            self.claw.in_the_air = True
            self.claw.speed_y = jump_velocity

        if event.key == pygame.K_p and self.claw.alive:
            self.text_pausa.show_text("Pausa", 100, (self.width // 2, self.height // 2 + 100), MAGENTA)
            self.timer.pause()
            self.wait_user()

    def handle_keyup_events(self, event):
        if event.key == pygame.K_a:
            self.map_level.left_key_pressed = False
            self.claw.moving_left = False

        if event.key == pygame.K_d:
            self.map_level.right_key_pressed = False
            self.claw.moving_right = False

        if event.key == pygame.K_w:
            self.claw.jump = False

        if event.key == pygame.K_ESCAPE:
            self.exit_game()

    def handle_mousedown_events(self, event):
        if event.button == 1 and not (self.claw.moving_left or self.claw.moving_right):
            self.claw.shoot = True
            bullet = Bullet(self.claw.rect.x + x_bullet * self.claw.direction, self.claw.rect.y + y_bullet, self.claw.direction, speed_bullet, "src/claw_images/otras imagenes/bullet.png", self.width, scale_bullet,\
                            self.enemy_group, self.bullet_group, is_hurt_enemy, player_is_hurt)
            self.bullet_group.add(bullet)
            self.sounds.play_shoot()
            print("Presionaste el boton de disparo")

        if event.button == 3 and not (self.claw.moving_left or self.claw.moving_right):
            if self.magic_bar.percentage > 0:
                self.claw.magic_attack = True
                self.magic_bar.percentage -= 25
                self.magic_bar.update_percentage(self.magic_bar.percentage)
                self.sounds.play_magic_attack()
                magic_attack = MagicAttack(self.claw.rect.x + x_bullet * self.claw.direction, self.claw.rect.y + y_bullet, self.claw.direction, speed_magic_attack, self.width, .45,\
                                        self.enemy_group, self.magic_attack_group, 5, qty_magic_attack_power)
                self.magic_attack_group.add(magic_attack)
                print("Presionaste el boton de ataque de espada")
            
    def handle_mouseup_events(self, event):
        if event.button == 1:
            self.claw.shoot = False
        if event.button == 3:
            self.claw.magic_attack = False

    def restart(self):

        #defino las variables de movimiento del jugador principal
        self.sword_attack = False
        self.shoot = False
        self.magic_attack = False
        self.moving_right = False
        self.moving_left = False
        self.jump = False
        self.in_the_air = True
        self.alive = True
        self.flip_claw = False
        self.gravity = 1.25
        self.time_last_shot = 0
        self.shot_interval = 50
        self.jump_velocity = -15
        self.player_is_hurt = False
        self.scale_claw = .45
        self.score = [0]
        self.damage_interval = 1000
        self.last_damage_time = 0
        self.current_time = 0
        self.pos_x_claw = 200
        self.pos_y_claw = 800
        self.speed_x_claw = 4
        self.speed_y_claw = 0

        # variables para las bullet
        self.speed_bullet = 10
        self.scale_bullet = 15
        self.x_bullet = 60
        self.y_bullet = 15

        # defino variables del enemy 1
        self.qty_enemy = 10
        self.enemy_alive = True
        self.flip_enemy = False
        self.moving_left_enemy = False
        self.moving_right_enemy = False
        self.health_enemy = 100
        self.speed_enemy = 1
        self.shots_recived = 0
        self.flee_health = 20
        self.attack_range = 100
        self.scale_enemy = .40
        self.pos_y_enemy1 = 400
        self.pos_y_enemy2 = 800

        #botones menu de inicio
        self.width_menu_screen = 1000
        self.height_menu_screen = 800
        self.width_button = 400
        self.height_button = 70

        # defino un timer
        self.animation_cooldown_claw = 50
        self.animation_cooldown_enemy = 100

        # variables del map
        self.tile_size = 26
        self.position_x_tile = 0
        self.speed_map = 2
        self.multiplier_scroll = 1.68 
        self.scroll_start = False

        # defino variables de los coins
        self.qty_coins = 10
        self.coin_width = 16
        self.coin_height = 16
        self.pos_y_coins = 720

        #-----coordenadas del background
        self.background_x = 0
        self.background_y = 0

        #-----variables del status bar
        self.pos_x_live_bar = 100
        self.pos_y_live_bar = 100
        self.width_bar = 150
        self.height_bar = 25
        self.percentage_live = 100
        self.percentage_magic = 0
        self.pos_x_magic_bar = 100
        self.pos_y_magic_bar = 160
        
        self.enemy_group.empty()
        self.all_coins.empty()
        self.bullet_group.empty()
        self.magic_attack_group.empty()
        self.special_items.empty()

        self.init_coins()
        self.init_enemies("NIVEL 1")
        self.init_map("NIVEL 1")
        self.init_player()
        self.init_sprites()
        self.init_status_bars()
        self.init_especial_items()
        self.init_traps()
        self.init_timer()

    def run_game(self):
        
        # Dibujar el background
        if self.level == "NIVEL 1" or self.level == "NIVEL 2":
            self.screen.blit(self.background, (0,-420))
        elif self.level == "NIVEL 3":
            self.screen.blit(self.background_bg, (0,0))
            self.screen.blit(self.background_2, (0,950))
            # self.sounds.canon_final_boss_sound.play()
            self.final_boss.update(self.sounds)
            self.final_boss.bullet_group.update()

            # Dibuja el jefe final y todas las balas
            self.final_boss.draw(self.screen)
            self.final_boss.bullet_group.draw(self.screen)

            # Verificación de colisiones con el jefe final
            collisions = pygame.sprite.groupcollide(self.final_boss.bullet_group, self.claws, True, False)
            for bullet in collisions:
                for claw in collisions[bullet]:
                    self.status_bar.percentage -= 100
                    self.status_bar.update_percentage(self.status_bar.percentage)
                    if self.status_bar.percentage == 0:
                        self.high_scores.update_high_scores(self.player_name, score[0])
                        self.sounds.play_game_over()
                        restart_option = self.game_over.run(self.player_name)

                        if restart_option == "REINICIAR":
                            self.restart()
                            self.timer.reset()

            collisions_magic_attacks = pygame.sprite.spritecollide(self.final_boss, self.magic_attack_group, True)
            for magic_attack in collisions_magic_attacks:
                self.final_boss.health -= 10  # Los ataques mágicos reducen la salud del jefe final en un 10%
                self.final_boss.health_bar.update_percentage(self.final_boss.health)
                if self.final_boss.health <= 0:
                    score[0] += 1000
                    self.high_scores.update_high_scores(self.player_name, score[0])
                    self.sounds.play_win()
                    restart_option = self.win.run(self.player_name)

                    if restart_option == "REINICIAR":
                        self.restart()
                        self.timer.reset()
                        score[0] = 0
            

            # Verificación de colisiones con el jefe final
            collisions_bullets = pygame.sprite.spritecollide(self.final_boss, self.bullet_group, True)
            for bullet in collisions_bullets:
                self.final_boss.health -= 5  # Las balas reducen la salud del jefe final en un 5%
                self.final_boss.health_bar.update_percentage(self.final_boss.health)
                if self.final_boss.health <= 0:
                    score[0] += 1000
                    self.high_scores.update_high_scores(self.player_name, score[0])
                    self.sounds.play_win()
                    restart_option = self.win.run(self.player_name)

                    if restart_option == "REINICIAR":
                        self.restart()
                        self.timer.reset()
                        score[0] = 0
                        
        # dibujo y actualizo las bullets
        self.bullet_group.update()
        self.bullet_group.draw(self.screen)

        self.status_bar.draw_bar(self.screen)
        self.magic_bar.draw_bar(self.screen)
        self.special_items.draw(self.screen)
        # dibujo y actualizo las trampas
        self.traps.draw(self.screen)
        #dibujo las plataformas
        for platform in self.map_level.platforms_group:
            self.screen.blit(platform.image, (platform.rect.x + self.map_level.position_x, platform.rect.y))

        for magic_attack in self.magic_attack_group:
            magic_attack.update()
            magic_attack.draw(self.screen)


        # dibujo y actualizo al personaje principal y el enemigo_1
        self.claw.update_animation()
        self.claw.draw(self.screen)
        self.claw.move(self.map_level.platforms_group, self.map_level, self.width)
        
        # actualizo constantemente la posicion de claw
        self.claw.player_pos = (self.claw.rect.x, self.claw.rect.y)


        self.all_coins.update()  # Actualizar la animación de las monedas
        self.all_coins.draw(self.screen)  # Dibujar las monedas en la pantalla

        # verificacion de colisiones con las trampas
        collisions_traps = pygame.sprite.groupcollide(self.claws, self.traps, True, False)

        # Verificación de colisiones con las trampas
        for player, traps_hit in collisions_traps.items():
            for trap in traps_hit:
                self.claw.alive = False
                self.claw.kill()
                self.status_bar.percentage = 0
                self.status_bar.update_percentage(self.status_bar.percentage)
                # Llenar la pantalla con el color de fondo
                self.screen.fill((0, 0, 0))  # Asume que el color de fondo es negro
                deaht = pygame.transform.scale(pygame.image.load("src/claw_images/claw/fall/3.png"),(150, 150))
                self.screen.blit(deaht, (self.claw.rect.x, self.claw.rect.y))

                # Crear una instancia de TextRenderer y mostrar el texto
                text_renderer = TextRenderer(self.screen)
                text_renderer.show_text("Has muerto", 250, (self.width // 2, self.height // 2), RED)  # Asume que el color rojo es (255, 0, 0)
                
                pygame.display.flip()
                self.sounds.play_game_over()
                time.sleep(2)
                restart_option = self.game_over.run(self.player_name)
                if restart_option == "REINICIAR":
                    self.restart()
                    score[0] = 0
                print("El jugador chocó con una trampa")

        # verificacion de bullets y enemigos
        for enemy in self.enemy_group:

            enemy.ai(self.claw, self.map_level.platforms_group, self.width, self.map_level)
            collisions = pygame.sprite.groupcollide(self.bullet_group, self.enemy_group, True, False)
            self.current_time = pygame.time.get_ticks()

            if self.current_time - self.last_damage_time >= self.damage_interval:
                if pygame.sprite.collide_rect(self.claw, enemy):
                    self.status_bar.percentage -= enemy.damage
                    self.status_bar.update_percentage(self.status_bar.percentage)
                    self.last_damage_time = self.current_time
                    
                    if self.status_bar.percentage == 0:
                        self.high_scores.update_high_scores(self.player_name, score[0])
                        self.high_scores.save_high_score(self.player_name, score[0])
                        self.sounds.play_game_over()
                        restart_option = self.game_over.run(self.player_name)

                        if restart_option == "REINICIAR":
                            self.restart()
                            self.timer.reset()
                            score[0] = 0

            for bullet in collisions:
                for enemy in collisions[bullet]:
                    enemy.health_bar.percentage -= 25  # Reduce la salud del enemigo
                    enemy.percentage_live -= 25  # Reduce la salud del enemigo
                    if enemy.percentage_live <= 0:  # Si la salud del enemigo es 0 o menos, lo elimina
                        print("¡Enemigo eliminado!")
                        score[0] += 25
                        self.enemy_group.remove(enemy)

            enemy.update_animation()
            enemy.draw(self.screen)
            enemy.health_bar.draw_bar(self.screen)

        for enemy in self.enemy_group:
            enemy.ai(self.claw, self.map_level.platforms_group, self.width, self.map_level)
            collisions = pygame.sprite.groupcollide(self.magic_attack_group, self.enemy_group, True, False)
            self.current_time = pygame.time.get_ticks()

            if self.current_time - self.last_damage_time >= self.damage_interval:
                if pygame.sprite.collide_rect(self.claw, enemy):
                    self.status_bar.percentage -= enemy.damage
                    self.status_bar.update_percentage(self.status_bar.percentage)
                    self.last_damage_time = self.current_time

                    if self.status_bar.percentage == 0:
                        self.high_scores.update_high_scores(self.player_name, score[0])
                        self.sounds.play_game_over()
                        restart_option = self.game_over.run(self.player_name)

                        if restart_option == "REINICIAR":
                            self.restart()
                            self.timer.reset()

            for magic_attack in collisions:
                for enemy in collisions[magic_attack]:
                    enemy.health_bar.percentage -= 200  # Reduce la salud del enemigo
                    enemy.percentage_live -= 200  # Reduce la salud del enemigo
                    if enemy.health_bar.percentage <= 0:  # Si la salud del enemigo es 0 o menos, lo elimina
                        print("¡Enemigo eliminado!")
                        score[0] += 25
                        self.enemy_group.remove(enemy)
                        self.timer.reset()

            enemy.update_animation()
            enemy.draw(self.screen)


        # Detección de colisiones
        collisions = pygame.sprite.groupcollide(self.claws, self.all_coins, False, True)

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

        # Detección de colisiones con los elementos especiales
        collisions_special_items = pygame.sprite.groupcollide(self.claws, self.special_items, False, True)

        # Manejar las colisiones
        for player, special_items in collisions_special_items.items():
            for special_item in special_items:
                if special_item.type == "life" and self.status_bar.percentage < 100: 
                    self.status_bar.percentage += 10
                    print("¡El jugador recogió un elemento de vida!")
                elif special_item.type == "magic" and self.magic_bar.percentage < 100:
                    self.magic_bar.percentage += 25
                    print("¡El jugador recogió un elemento de magia!")

        game_over = self.timer.draw(self.screen)

        if game_over:
            self.high_scores.update_high_scores(self.player_name, score[0])
            self.sounds.play_game_over()
            self.restart()
            self.timer.reset()
            restart_option = self.game_over.run(self.player_name)
            score[0] = 0

        if self.claw.alive:
            
            if self.claw.magic_attack and self.claw.direction == 1:
                self.claw.update_action(5) # 5 es ataque magico
            if self.claw.magic_attack and self.claw.direction == -1:
                self.claw.update_action(5) # 5 es ataque magico
            elif self.claw.shoot and self.claw.direction == 1:
                self.claw.update_action(4) # 4 es disparo
            elif self.claw.shoot and self.claw.direction == -1:
                self.claw.update_action(4) # 4 es disparo
            elif self.claw.sword_attack:
                self.claw.update_action(3) # 3 es taque de espada
            elif self.claw.in_the_air:
                self.claw.update_action(2) # 2 es saltar
            elif self.claw.moving_left or self.claw.moving_right:
                self.claw.update_action(1) # 1 es correr
            else:
                self.claw.update_action(0) # 0 es idle
        self.clock.tick(FPS)
        
        self.text_renderer.show_text(f"Score: {score[0]}     Player: {self.player_name}", 45, (self.width // 2, 100), VIOLETA)
        # Actualizo la pantalla
        pygame.display.flip()

    def run_main(self):

        while self.run_menu:
            menu_option = self.main_menu.run()
            self.timer.pause()

            if menu_option == "INICIAR JUEGO":

                self.map_level = "NIVEL 1" # Guarda el nivel seleccionado en self.map_level
                self.init_map(self.map_level)
                self.init_enemies("NIVEL 1")  # Inicializa los enemigos para el nivel seleccionado
                self.main_menu.menu_option = None
                self.run_level_1 = True
                username_screen = UsernameScreen(self.screen, self.width, self.height)
                self.player_name = username_screen.run()
                self.init_especial_items()
                self.init_traps()
                self.init_coins()
                self.timer.reset()

                while self.run_level_1:  
                    self.handle_events()
                    self.run_game()
                    if len(self.enemy_group) == 0:
                        self.map_level = "NIVEL 2"
                        self.init_map(self.map_level)
                        self.init_enemies("NIVEL 2")
                        self.init_coins()
                        self.init_especial_items()
                        self.init_traps()
                        self.timer.reset()
                        self.run_level_1 = False
                        self.run_level_2 = True
                        self.claw.rect.x = 200
                        self.claw.rect.y = 800
                        while self.run_level_2:
                            self.handle_events()
                            self.run_game()
                            if len(self.enemy_group) == 0:
                                self.map_level = "NIVEL 3"
                                self.init_map(self.map_level)
                                self.init_enemies("NIVEL 3")
                                self.init_final_boss()
                                self.init_coins()
                                self.init_especial_items()
                                self.init_traps()
                                self.timer.reset()
                                self.run_level_2 = False
                                self.run_level_3 = True
                                self.claw.rect.x = 200
                                self.claw.rect.y = 800
                                while self.run_level_3:
                                    self.handle_events()
                                    self.run_game()
                                    if len(self.enemy_group) == 0:
                                        self.high_scores.update_high_scores(self.player_name, score[0])
                                        self.sounds.play_game_over()
                                        self.restart()
                                        self.timer.reset()
                                        score[0] = 0
                                        self.run = False
                                        self.run_menu = True
                                        self.run_main()
                                        self.timer.reset()
                                        self.high_scores.update_high_scores(self.player_name, score[0])
                                        break
                                break
                        break



            if menu_option == "VER PUNTUACIONES":
                # self.main_menu.menu_option = None
                # top_scores = self.sqlite.get_top_scores()
                # self.sqlite.game_loop(top_scores)

                self.main_menu.menu_option = None
                self.run_puntuaciones = True
                self.run_menu = False

                while self.run_puntuaciones:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            self.exit_game()
                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            x, y = pygame.mouse.get_pos()
                            if button_start_rect.collidepoint(x, y):
                                self.run_puntuaciones = False
                                self.run_menu = True
                                
                    self.screen.fill(NEGRO)

                    self.high_scores.show_high_scores(self.screen, NEGRO)
                    # Dibuja un botón para volver al menú principal
                    button_start_rect = pygame.Rect(self.width // 2 - width_button // 2, self.height // 2 + height_button, width_button, height_button)
                    
                    # Aplica la misma lógica de interacción con el ratón
                    if button_start_rect.collidepoint(pygame.mouse.get_pos()):
                        pygame.draw.rect(self.screen, AZUL, button_start_rect, border_radius=25)
                    else:
                        pygame.draw.rect(self.screen, VERDE, button_start_rect, border_radius=25)
                    
                    font = pygame.font.Font(None, 36)
                    text_surface = font.render("Volver al menú", True, BLANCO)
                    text_rect = text_surface.get_rect(center=button_start_rect.center)
                    self.screen.blit(text_surface, text_rect.topleft)

                    pygame.display.update()
            
            if menu_option == "NIVELES":

                level_menu = LevelMenu(self.screen, self.width, self.height, "src/claw_images/background_menu.jpg")
                level_option = level_menu.run()
                
                if level_option == "REGRESAR":
                    self.main_menu.menu_option = None
                    self.run_menu = True

                elif level_option in ["NIVEL 1", "NIVEL 2", "NIVEL 3"]:
                    self.map_level = level_option  # Guarda el nivel seleccionado en self.map_level
                    self.init_map(self.map_level)
                    self.init_enemies(level_option)  # Inicializa los enemigos para el nivel seleccionado
                    self.main_menu.menu_option = None
                    self.run = True
                    username_screen = UsernameScreen(self.screen, self.width, self.height)
                    self.player_name = username_screen.run()
                    self.init_especial_items()
                    self.init_traps()
                    self.init_coins()
                    self.timer.reset()
                    
                    while self.run:  
                        self.handle_events()
                        self.run_game()
                    
            if menu_option == "CONFIGURACIÓN":
                self.main_menu.menu_option = None
                self.show_config_screen()
                self.run_menu = True

            if menu_option == "SALIR":
                self.exit_game()
                self.timer.reset()

    def exit_game(self):
        self.run_menu = False
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Main(last_damage_time, current_time, damage_interval, player_name, run_menu, run, run_puntuaciones, run_game_over, score)
    game.main() 
    game.run_main()


# modularizar run_game()
# modularizar run_main()
