import pygame, random

class Enemy(pygame.sprite.Sprite):
    def __init__(self, alive, flip, x, y, scale, speed_x, speed_y, folder_path, moving_left_enemy, moving_right_enemy, gravity, shots_recived, qty_idle_images,\
                qty_moving_images, qty_attack_images, qty_death_images ,health, damage, animations_cooldown):
        pygame.sprite.Sprite.__init__(self)
        self.alive = alive
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.gravity = gravity
        self.action = 0
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.animation_list = []
        self.flip = flip
        self.direction = -1 if flip else 1 
        self.folder_path = folder_path
        self.qty_idle_image = qty_idle_images
        self.qty_moving_images = qty_moving_images
        self.qty_attack_images = qty_attack_images
        self.qty_death_image = qty_death_images
        self.health = health
        self.damage = damage
        self.dying = False
        self.shots_recived = shots_recived
        self.moving_left = moving_left_enemy
        self.moving_right = moving_right_enemy
        self.animation_cooldown = animations_cooldown
        self.move_counter = 0
        self.idling = False
        self.idling_counter = 0
        self.vision = pygame.Rect(0, 0, 50, 20)

        animations_info = [[self.qty_idle_image, "idle"], [self.qty_moving_images, "moving"], [self.qty_attack_images, "attack"], [self.qty_death_image, "death"]]

        for num_images, folder in animations_info:
            temp_list = []
            for i in range(num_images):
                image = pygame.image.load(f"{self.folder_path}/{folder}/{i}.png")
                image = pygame.transform.scale(image, (int(image.get_width() * scale), int(image.get_height() * scale)))
                temp_list.append(image)
            self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.mask = pygame.mask.from_surface(self.image)

    def move(self, moving_left_enemy, moving_right_enemy, platforms, width, map_level):
        #reset movement variables
        dir_x_enemy = 0
        dir_y_enemy = 0

        #assign movement variables if moving left or right
        if moving_left_enemy:
            dir_x_enemy = -self.speed_x
            self.flip = True
            self.direction = -1

        if moving_right_enemy:
            dir_x_enemy = self.speed_x
            self.flip = False
            self.direction = 1

        # aplico gravedad
        self.speed_y += self.gravity
        dir_y_enemy += self.speed_y

        # verifico colision con el piso
        if self.rect.bottom + dir_y_enemy > 1000:
            dir_y_enemy = 840 - self.rect.bottom
            self.in_the_air = False
        
        for platform in platforms:
            offset_x = platform.rect.x - self.rect.x
            offset_y = platform.rect.y - self.rect.y
            if self.mask.overlap(platform.mask, (offset_x, offset_y)):
                self.rect.bottom = platform.rect.top
                self.in_the_air = False
                self.speed_y = 0

        #update rectangle position
        self.rect.x += dir_x_enemy
        self.rect.y += dir_y_enemy

        #verifico los bordes para que no salgan de pantalla los enemigos
        if self.rect.left + dir_x_enemy < 0 or self.rect.right + dir_x_enemy > width:
            self.direction *= -1

        for platform in platforms:
            if platform.rect.colliderect(self.rect.x, self.rect.y + 1, self.rect.width, self.rect.height) and self.speed_y >= 0:
                self.rect.bottom = platform.rect.top
                self.in_the_air = False
                self.speed_y = 0

    def update_action(self, new_action):
        #verifico si la accion a producirse es diferente a la anterior
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def update_animation(self):

        self.image = self.animation_list[self.action][self.frame_index]

        self.mask = pygame.mask.from_surface(self.image)

        if self.dying and self.frame_index == len(self.animation_list[self.action]) - 1:
        # Si este enemigo está muriendo y la animación de muerte ha terminado, lo elimina
            self.kill()

        if pygame.time.get_ticks() - self.update_time > self.animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1

            if self.frame_index >= len(self.animation_list[self.action]):
                self.frame_index = 0

    def ai(self, player, platforms, width, map_level):
        
        if self.alive and player.alive:
            if self.idling == False and random.randint(1, 200) == 1:
                self.update_action(0)#0: idle
                self.idling = True
                self.idling_counter = 100
            
            if self.vision.colliderect(player.rect):
                self.update_action(2)

            else:
                if self.idling == False:
                    if self.direction == 1:
                        self.moving_right_enemy = True
                    else:
                        self.moving_right_enemy = False

                    self.moving_left_enemy = not self.moving_right_enemy
                    self.move(self.moving_left_enemy, self.moving_right_enemy, platforms, width, map_level)
                    self.update_action(1)
                    self.move_counter += 1
                
                    self.vision.center = (self.rect.centerx + 25 * self.direction, self.rect.centery)

                    if self.move_counter > 32:
                        self.direction *= -1
                        self.move_counter *= -1
                else:
                    self.idling_counter -= 1
                    if self.idling_counter <= 0:
                        self.idling = False
                        
    def draw(self, screen):
        screen.blit(pygame.transform.flip(self.image, not self.flip, False), self.rect)
