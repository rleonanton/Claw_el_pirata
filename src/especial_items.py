import pygame
import random

class SpecialItem(pygame.sprite.Sprite):
    def __init__(self, screen, pos_x, pos_y, image_path, item_type, scale_special_items):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.image = pygame.transform.scale(pygame.image.load(image_path), scale_special_items)
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.type = item_type  # 'life' o 'magic'

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def check_collision(self, player_rect):
        if self.rect.colliderect(player_rect):
            if self.type == 'life':
                return 'life'
            elif self.type == 'magic':
                return 'magic'
        return None