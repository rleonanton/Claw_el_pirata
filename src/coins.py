import pygame
import random
import os

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y, coin_type, coin_width, coin_height):
        super().__init__()

        self.coin_type = coin_type
        self.image_list = self.load_coin_images(coin_width, coin_height)
        self.image = random.choice(self.image_list)
        self.rect = self.image.get_rect(center=(x, y))
        self.animation_cooldown = 75
        self.last_update = pygame.time.get_ticks()
        self.coin_width = coin_width
        self.coin_height = coin_height

    def load_coin_images(self, coin_width, coin_height):
        image_list = []
        coin_folder = f"src/coins/{self.coin_type}/"
        
        for i in range(6):
            image_path = os.path.join(coin_folder, f"{i}.png")
            ori_image = pygame.image.load(image_path).convert_alpha()
            scaled_image = pygame.transform.scale(ori_image, (coin_width, coin_height))
            image_list.append(scaled_image)
            
        return image_list

    def update(self):
        # Controlar la animación y el cooldown
        now = pygame.time.get_ticks()
        if now - self.last_update > self.animation_cooldown:
            self.last_update = now
            self.image = random.choice(self.image_list)