import pygame
import random
from bullet_final_boss import Bullet
from config import VERDE, RED
from status_bar import StatusBar

class FinalBoss(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image_path, screen):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(image_path), (480,480))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = width
        self.height = height
        self.screen = screen
        self.direction = 5
        self.last_shot = pygame.time.get_ticks()
        self.shot_delay = 2000  # Dispara cada 2 segundos
        self.bullet_group = pygame.sprite.Group()
        self.initial_x = x  # Posición inicial del barco
        self.range = 400 
        self.health = 100  # Salud inicial del jefe final
        self.health_bar = StatusBar(x, y - 20, 100, 10, VERDE, RED, self.health, "LIVE BAR", 10)  # Barra de vida del jefe final

    def update(self, sounds):
        # Mover el barco de un lado a otro dentro del rango especificado
        if self.rect.x > self.initial_x + self.range or self.rect.x < self.initial_x:
            self.direction *= -1
        self.rect.x += self.direction

        # Disparar cada 2 segundos
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot > self.shot_delay:
            self.shoot(sounds)
            self.last_shot = current_time

        # Actualiza la posición de la barra de vida para que siga al jefe final
        self.health_bar.x = self.rect.x + 20
        self.health_bar.y = self.rect.y + 120

    def shoot(self, sounds):
        bullet = Bullet(self.rect.left, self.rect.centery + 85, "src/claw_images/otras imagenes/bullet.png")
        sounds.play_canon_final_boss()
        self.bullet_group.add(bullet)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        
        for bullet in self.bullet_group:
            bullet.draw(screen)

        # Dibuja la barra de vida
        self.health_bar.draw_bar(screen)
