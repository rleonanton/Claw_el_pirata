import pygame


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, speed_bullet, path_bullet_image, screen_width, scale_bullet, enemy, bullet_group, is_hurt_enemy, player_is_hurt):
        pygame.sprite.Sprite.__init__(self)
        self.speed = speed_bullet
        self.image = pygame.transform.scale(pygame.image.load(path_bullet_image), (scale_bullet, scale_bullet))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.mask = pygame.mask.from_surface(self.image)
        self.direction = direction
        self.screen_width = screen_width
        self.enemy = enemy
        self.bullet_group = bullet_group
        self.enemy_is_hurt = is_hurt_enemy
        self.player_is_hurt = player_is_hurt

    def update(self):
        #move bullet
        self.rect.x += (self.direction * self.speed)
        #check if bullet has gone off screen
        if self.rect.right < 0 or self.rect.left > self.screen_width:
            self.kill()

        