import pygame, random


class Player(pygame.sprite.Sprite):
    def __init__(self, alive, jump, flip, x, y, scale, speed_x, speed_y, gravity, in_the_air, sword_attack, shoot, magic_attack, folder_path,\
                qty_idle_images, qty_running_images, qty_jump_images, qty_sword_attack_images, qty_shoot_images, qty_magic_attack_images, scroll_start, moving_left, moving_right, animation_cooldown):
        pygame.sprite.Sprite.__init__(self)
        self.alive = alive
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.gravity = gravity
        self.direction = 1 # mira a la derecha mi personaje
        self.jump = jump
        self.in_the_air = in_the_air
        self.sword_attack = sword_attack
        self.shoot = shoot
        self.magic_attack = magic_attack
        self.flip = flip
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        self.folder_path = folder_path
        self.qty_idle_images = qty_idle_images
        self.qty_running_images = qty_running_images
        self.qty_jump_images = qty_jump_images
        self.qty_sword_attack_images = qty_sword_attack_images
        self.qty_shoot_images = qty_shoot_images
        self.qty_magic_attack_images = qty_magic_attack_images
        self.move_counter = 0
        self.idling = False
        self.idling_counter = 0
        self.scroll_start = scroll_start
        self.moving_left = moving_left
        self.moving_right = moving_right
        self.animation_cooldown = animation_cooldown
        self.scale = scale
        self.original_animation_list = []  # nueva lista para guardar las imágenes originales

        animations_info = [(self.qty_idle_images, 'idle'), (self.qty_running_images, 'running'), (self.qty_jump_images, 'jump'), (self.qty_sword_attack_images, 'sword_attack'),\
                            (self.qty_shoot_images, 'shoot'), (self.qty_magic_attack_images, 'magic_attack')]
        
        for num_images, folder in animations_info:
            temp_list = []
            for i in range(num_images):
                image = pygame.image.load(f"{self.folder_path}/{folder}/{i}.png")
                image = pygame.transform.scale(image, (int(image.get_width() * scale), int(image.get_height() * scale)))
                temp_list.append(image)
            self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.mask = pygame.mask.from_surface(self.image)

    def move(self, platforms, map_level, width):

        #reinicio las variables de movimiento
        dir_x = 0
        dir_y = 0

        if self.moving_left:
            dir_x = -self.speed_x
            self.flip = True
            self.direction = -1 # mira a la izquierda mi personaje

        if self.moving_right:
            dir_x = self.speed_x
            self.flip = False
            self.direction = 1 # mira a la derecha mi personaje

        # verifico si salta mi personaje
        if self.jump == True and self.in_the_air == False:
            self.jump = False
            self.in_the_air = True
        
        # aplico gravedad
        self.speed_y += self.gravity
        dir_y += self.speed_y

        for platform_rect in map_level.get_platform_rects():
            if platform_rect.colliderect(self.rect.x + dir_x, self.rect.y, self.rect.width, self.rect.height):
                dir_x = 0

        # actualizo la posición del personaje en el eje x
        self.rect.x += dir_x
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > width:
            self.rect.right = width
            
        # Verifica las colisiones en el eje y
        for platform in platforms:
            if platform.rect.colliderect(self.rect.x, self.rect.y + dir_y, self.rect.width, self.rect.height):
                if self.speed_y > 0:  # Si el personaje se está moviendo hacia abajo
                    self.rect.bottom = platform.rect.top
                    self.in_the_air = False
                    self.speed_y = 0
                elif self.speed_y < 0:  # Si el personaje se está moviendo hacia arriba
                    self.rect.top = platform.rect.bottom
                    self.speed_y = 0
                dir_y = 0

        # Actualiza la posición del rectángulo
        self.rect.y += dir_y

    def update_action(self, new_action):
        #verifico si la accion a producirse es diferente a la anterior
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def update_animation(self):

        # actualizo las imagenes 
        self.image = self.animation_list[self.action][self.frame_index]

        # actualizo la mask de la imagen
        self.mask = pygame.mask.from_surface(self.image)
        
        # verifico el tiempo desde la ultima actualizacion
        if pygame.time.get_ticks() - self.update_time > self.animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1

            if self.frame_index >= len(self.animation_list[self.action]):
                self.frame_index = 0

    def draw(self, screen):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
