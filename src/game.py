class Game:
    def __init__(self, run, FPS, scroll_tresh, screen_scroll, background_scroll, player_name, run_menu, ver_puntuacion,
                 sword_attack, shoot, magic_attack, moving_right, moving_left, jump, in_the_air, alive, flip_claw, gravity, time_last_shot, shot_interval, jump_velocity, qty_idle_images_claw, qty_running_images_claw, 
                 qty_jump_images_claw, qty_sword_attack_images_claw, qty_shoot_images_claw, qty_magic_attack_images_claw, qty_fall_images_claw, qty_death_images_claw, player_is_hurt, scale_claw, score, damage_interval, last_damage_time,
                 speed_bullet, scale_bullet, x_bullet, y_bullet,
                 enemy_alive, flip_enemy, moving_left_enemy, moving_right_enemy, qty_idle_images_enemy, qty_walking_images_enemy, qty_attack_images_enemy, health_enemy, is_hurt_enemy, speed_enemy, shots_recived, flee_health, attack_range, scale_enemy, pos_y_enemy1, pos_y_enemy2, qty_enemy,
                 width_menu_screen, height_menu_screen, width_button, height_button,
                 animation_cooldown_claw, animation_cooldown_enemy,
                 tile_size, position_x_tile, speed_map, multiplier_scroll, scroll_start,
                 qty_coins, coin_width, coin_height, pos_y_coins,
                 background_x, background_y,
                 pos_x_live_bar, pos_y_live_bar, width_bar, height_bar, percentage_live, percentage_magic, pos_x_magic_bar, pos_y_magic_bar):
        
        # Inicializa todas las variables y estados del juego
        self.run = run
        self.FPS = FPS
        self.scroll_tresh = scroll_tresh
        self.screen_scroll = screen_scroll
        self.background_scroll = background_scroll
        self.player_name = player_name
        self.run_menu = run_menu
        self.ver_puntuacion = ver_puntuacion

        # Variables de movimiento del jugador principal
        self.sword_attack = sword_attack
        self.shoot = shoot
        self.magic_attack = magic_attack
        self.moving_right = moving_right
        self.moving_left = moving_left
        self.jump = jump
        self.in_the_air = in_the_air
        self.alive = alive
        self.flip_claw = flip_claw
        self.gravity = gravity
        self.time_last_shot = time_last_shot
        self.shot_interval = shot_interval
        self.jump_velocity = jump_velocity
        self.qty_idle_images_claw = qty_idle_images_claw
        self.qty_running_images_claw = qty_running_images_claw 
        self.qty_jump_images_claw = qty_jump_images_claw
        self.qty_sword_attack_images_claw = qty_sword_attack_images_claw
        self.qty_shoot_images_claw = qty_shoot_images_claw
        self.qty_magic_attack_images_claw = qty_magic_attack_images_claw
        self.qty_fall_images_claw = qty_fall_images_claw
        self.qty_death_images_claw = qty_death_images_claw
        self.player_is_hurt = player_is_hurt
        self.scale_claw = scale_claw
        self.score = score
        self.damage_interval = damage_interval
        self.last_damage_time = last_damage_time

        # Variables para las bullet
        self.speed_bullet = speed_bullet
        self.scale_bullet = scale_bullet
        self.x_bullet = x_bullet
        self.y_bullet = y_bullet

        # Variables del enemy 1
        self.enemy_alive = enemy_alive
        self.flip_enemy = flip_enemy
        self.moving_left_enemy = moving_left_enemy
        self.moving_right_enemy = moving_right_enemy
        self.qty_idle_images_enemy = qty_idle_images_enemy
        self.qty_walking_images_enemy = qty_walking_images_enemy
        self.qty_attack_images_enemy = qty_attack_images_enemy
        self.health_enemy = health_enemy
        self.is_hurt_enemy = is_hurt_enemy
        self.speed_enemy = speed_enemy
        self.shots_recived = shots_recived
        self.flee_health = flee_health
        self.attack_range = attack_range
        self.scale_enemy = scale_enemy
        self.pos_y_enemy1 = pos_y_enemy1
        self.pos_y_enemy2 = pos_y_enemy2
        self.qty_enemy = qty_enemy

        # Botones menu de inicio
        self.width_menu_screen = width_menu_screen
        self.height_menu_screen = height_menu_screen
        self.width_button = width_button
        self.height_button = height_button

        # Defino un timer
        self.animation_cooldown_claw = animation_cooldown_claw
        self.animation_cooldown_enemy = animation_cooldown_enemy

        # Variables del map
        self.tile_size = tile_size
        self.position_x_tile = position_x_tile
        self.speed_map = speed_map
        self.multiplier_scroll = multiplier_scroll 
        self.scroll_start = scroll_start

        # Defino variables de los coins
        self.qty_coins = qty_coins
        self.coin_width = coin_width
        self.coin_height = coin_height
        self.pos_y_coins = pos_y_coins

        # Coordenadas del background
        self.background_x = background_x
        self.background_y = background_y

        # Variables del status bar
        self.pos_x_live_bar = pos_x_live_bar
        self.pos_y_live_bar = pos_y_live_bar
        self.width_bar = width_bar
        self.height_bar = height_bar
        self.percentage_live = percentage_live
        self.percentage_magic = percentage_magic
        self.pos_x_magic_bar = pos_x_magic_bar
        self.pos_y_magic_bar = pos_y_magic_bar

    def restart(self):
        # Restablece todas las variables y estados del juego a sus valores iniciales
        print("si arranco")
        self.run = False
        self.FPS = 60
        self.scroll_tresh = 200
        self.screen_scroll = 0
        self.background_scroll = 0
        self.player_name = ""
        self.run_menu = False
        self.ver_puntuacion = False

        # Variables de movimiento del jugador principal
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
        self.qty_idle_images_claw = 8
        self.qty_running_images_claw = 10 
        self.qty_jump_images_claw = 7
        self.qty_sword_attack_images_claw = 6
        self.qty_shoot_images_claw = 5
        self.qty_magic_attack_images_claw = 6
        self.qty_fall_images_claw = 4
        self.qty_death_images_claw = 1
        self.player_is_hurt = False
        self.scale_claw = .45
        self.score = [0]
        self.damage_interval = 1000
        self.last_damage_time = 0

        # Variables para las bullet
        self.speed_bullet = 10
        self.scale_bullet = 15
        self.x_bullet = 60
        self.y_bullet = 15

        # Variables del enemy 1
        self.enemy_alive = True
        self.flip_enemy = False
        self.moving_left_enemy = False
        self.moving_right_enemy = False
        self.qty_idle_images_enemy = 8
        self.qty_walking_images_enemy = 7
        self.qty_attack_images_enemy = 5
        self.health_enemy = 100
        self.is_hurt_enemy = False
        self.speed_enemy = 1
        self.shots_recived = 0
        self.flee_health = 20
        self.attack_range = 100
        self.scale_enemy = .40
        self.pos_y_enemy1 = 400
        self.pos_y_enemy2 = 800
        self.qty_enemy = 10

        # Botones menu de inicio
        self.width_menu_screen = 1000
        self.height_menu_screen = 800
        self.width_button = 400
        self.height_button = 70

        # Defino un timer
        self.animation_cooldown_claw = 50
        self.animation_cooldown_enemy = 100

        # Variables del map
        self.tile_size = 26
        self.position_x_tile = 0
        self.speed_map = 2
        self.multiplier_scroll = 1.68 
        self.scroll_start = False

        # Defino variables de los coins
        self.qty_coins = 10
        self.coin_width = 16
        self.coin_height = 16
        self.pos_y_coins = 720

        # Coordenadas del background
        self.background_x = 0
        self.background_y = 0

        # Variables del status bar
        self.pos_x_live_bar = 100
        self.pos_y_live_bar = 100
        self.width_bar = 150
        self.height_bar = 25
        self.percentage_live = 100
        self.percentage_magic = 0
        self.pos_x_magic_bar = 100
        self.pos_y_magic_bar = 160

        print("si arranco")
# # Luego, puedes acceder y modificar las variables y estados del juego a través de la instancia del juego
# game.run = True
# game.restart()
