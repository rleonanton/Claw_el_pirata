import pygame
from config import VERDE

class StatusBar:
    def __init__(self, pos_x_bar, pos_y_bar, width_bar, height_bar, color_fill, border_color, percentage, text, font_size):

        self.x = pos_x_bar
        self.y = pos_y_bar
        self.width = width_bar
        self.height = height_bar
        self.color = color_fill
        self.border_color = border_color
        self.percentage = percentage
        self.font = pygame.font.Font(None, font_size)  # Define la fuente del texto
        self.text = text

    def update_percentage(self, percentage):
        self.percentage = percentage

    def draw_bar(self, surface):
        fill_width = (self.percentage / 100) * self.width
        border_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        fill_rect = pygame.Rect(self.x, self.y, fill_width, self.height)

        pygame.draw.rect(surface, self.color, fill_rect)
        pygame.draw.rect(surface, self.border_color, border_rect, 2)

        # Dibuja el texto arriba de la barra de vida
        text = self.font.render(self.text, True, (VERDE))  # Crea el texto
        text_rect = text.get_rect(center=(self.x + self.width // 2, self.y - text.get_height() // 2))  # Centra el texto arriba de la barra de vida
        surface.blit(text, text_rect.topleft)  # Dibuja el texto en la superficie
