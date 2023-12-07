
FPS = 45
scroll_tresh = 200
screen_scroll = 0
background_scroll = 0
player_name = ""
pos_x_special_item = 300
pos_y_especial_item = 573
scale_special_items = (32, 32)
volumen = 0.5

# booleanos para el juego

ver_puntuacion = False
menu_option = None
run = False
run_puntuaciones = False
run_game_over = False
run_menu = True

#defino las variables de movimiento del jugador principal

sword_attack = False
shoot = False
magic_attack = False
moving_right = False
moving_left = False
jump = False
in_the_air = True
alive = True
flip_claw = False
gravity = 1.25
time_last_shot = 0
shot_interval = 50
jump_velocity = -17
qty_idle_images_claw = 8
qty_running_images_claw = 10 
qty_jump_images_claw = 7
qty_sword_attack_images_claw = 6
qty_shoot_images_claw = 5
qty_magic_attack_images = 6
qty_magic_attack_power = 20
speed_magic_attack = 8
qty_fall_images_claw = 4
qty_death_images_claw = 1
player_is_hurt = False
scale_claw_menu = 1.8
scale_claw = .45
score = [0]
damage_interval = 1000
last_damage_time = 0
current_time = 0
pos_x_claw = 200
pos_y_claw = 800
speed_x_claw = 4
speed_y_claw = 0


# variables para las bullet

speed_bullet = 10
scale_bullet = 15
x_bullet = 60
y_bullet = 15

# defino variables del enemy 1

qty_enemy = 10
enemy_alive = True
flip_enemy = False
moving_left_enemy = False
moving_right_enemy = False
qty_idle_images_enemy = 8
qty_moving_images_enemy = 7
qty_attack_images_enemy = 5
health_enemy = 100
is_hurt_enemy = False
speed_enemy = 1
shots_recived = 0
flee_health = 20
attack_range = 100
scale_enemy = .40
pos_y_enemy1 = 400
pos_y_enemy2 = 800
damage_enemy_1 = 10
width_bar_enemy_1 = 50
height_bar_enemy_1 = 10
percentage_live_enemy = 100

# defino variables del enemy 2

qty_enemy_2 = 10
enemy_alive_2 = True
flip_enemy_2 = False
moving_left_enemy_2 = False
moving_right_enemy_2 = False
qty_idle_images_enemy_2 = 9
qty_moving_images_enemy_2 = 6
qty_attack_images_enemy_2 = 12
qty_death_images_enemy_2 = 23
health_enemy_2 = 200
is_hurt_enemy_2 = False
speed_enemy_2 = 3
shots_recived_2 = 0
flee_health_2 = 20
attack_range_2 = 100
scale_enemy_2 = 1.3
pos_y_enemy2_1 = 400
pos_y_enemy2_2 = 800
damage_enemy_2 = 20


#botones menu de inicio

width_menu_screen = 1000
height_menu_screen = 800
width_button = 400
height_button = 70

# defino un timer
animation_cooldown_claw = 50
animation_cooldown_enemy = 100


# variables del map

tile_size = 26
position_x_tile = 0
speed_map = 2
multiplier_scroll = 1.68 
scroll_start = False

# defino variables de los coins

qty_coins = 10
coin_width = 16
coin_height = 16
pos_y_coins = 720

#-----coordenadas del background

background_x = 0
background_y = 0


#-----variables del status bar

pos_x_live_bar = 100
pos_y_live_bar = 100
width_bar = 150
height_bar = 25
percentage_live = 100
percentage_magic = 0
pos_x_magic_bar = 100
pos_y_magic_bar = 160


####------colors

NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
RED = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
AMARILLO = (255, 255, 0)
CIAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
GRIS = (128, 128, 128)
NARANJA = (255, 165, 0)
ROSA = (255, 192, 203)
VIOLETA = (148, 0, 211)
BUTTON_COLOR = (153, 0, 0)