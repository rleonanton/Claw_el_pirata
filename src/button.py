import pygame


class Button:
    def __init__(self, x, y, width, height, color, hover_color, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.text = text

    def draw(self, screen):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, self.hover_color, self.rect, border_radius=25)
        else:
            pygame.draw.rect(screen, self.color, self.rect, border_radius=25)
        font = pygame.font.Font(None, 52)
        label = font.render(self.text, True, (0, 0, 0))  # Asume que el texto es negro
        text_rect = label.get_rect(center=self.rect.center)
        screen.blit(label, text_rect.topleft)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            return self.rect.collidepoint(event.pos)
        return False
