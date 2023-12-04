import pygame

class TextRenderer:
    def __init__(self, screen):
        self.screen = screen

    def show_text(self, text, font_size, coordinates, font_color):
        font = pygame.font.Font(None, font_size)
        text_surface = font.render(text, True, font_color)
        rect_text = text_surface.get_rect()
        rect_text.center = coordinates
        self.screen.blit(text_surface, rect_text)
        pygame.display.flip()