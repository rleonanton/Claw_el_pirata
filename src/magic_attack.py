import pygame

class MagicAttack(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, speed_attack, screen_width, scale_attack, enemy, attack_group, animation_cooldown, qty_magic_attack_power):
        pygame.sprite.Sprite.__init__(self)
        self.speed = speed_attack
        self.direction = direction
        self.screen_width = screen_width
        self.enemy = enemy
        self.attack_group = attack_group
        self.animation_cooldown = animation_cooldown
        self.animation_timer = 0
        self.animation_list = []
        self.frame_index = 0
        self.qty_magic_attack_power = qty_magic_attack_power

        animations_info = [(self.qty_magic_attack_power, "src/claw_images/claw/magicattck_power")]

        for num_images, folder in animations_info:
            temp_list = []
            for i in range(num_images):
                image = pygame.image.load(f"{folder}/{i}.png")
                image = pygame.transform.scale(image, (int(image.get_width() * scale_attack), int(image.get_height() * scale_attack)))
                temp_list.append(image)
            self.animation_list.append(temp_list)

        self.image = self.animation_list[0][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.x += (self.direction * self.speed)
        if self.rect.right < 0 or self.rect.left > self.screen_width:
            self.kill()
        self.handle_animation()

    def handle_animation(self):
        self.animation_timer += 1
        if self.animation_timer >= self.animation_cooldown:
            self.animation_timer = 0
            self.frame_index += 1
            if self.frame_index >= len(self.animation_list[0]):
                self.kill()
            else:
                self.image = self.animation_list[0][self.frame_index]

    def draw(self, screen):
        screen.blit(self.image, self.rect)
