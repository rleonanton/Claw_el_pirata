import pygame

class Trap(pygame.sprite.Sprite):

    def __init__(self, image, x, y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(image),(32, 32))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def check_collision(self, group):
        if pygame.sprite.groupcollide(group, self, False, False):
            for sprite in group:
                sprite.alive = False  # Todos los sprites en el grupo mueren al instante


    def draw(self, screen):
        for trap in self.traps:
            screen.blit(self.image, self.rect)