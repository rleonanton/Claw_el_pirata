import pygame

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(image_path),(55,55))
        self.rect = self.image.get_rect()
        self.rect.midleft = (x, y)

    def update(self):
        self.rect.x -= 10  # Ajusta la velocidad de la bala a tus necesidades

    def draw(self, screen):
        screen.blit(self.image, self.rect)