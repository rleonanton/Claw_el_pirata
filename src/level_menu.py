import pygame
import sys
from config import width_button, height_button, NEGRO, GRIS, BUTTON_COLOR

class LevelMenu:

    def __init__(self, screen, width, height, path_background_menu):
        self.screen = screen
        self.width = width
        self.height = height
        self.background = pygame.transform.scale(pygame.image.load(path_background_menu),(self.width, self.height))

    def draw_button(self, text, color_button, bg_color_hoover, text_color, rect_button):

        if rect_button.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(self.screen, bg_color_hoover, rect_button, border_radius=25)
        else:
            pygame.draw.rect(self.screen, color_button, rect_button, border_radius=25)
        font = pygame.font.Font(None, 52)
        label = font.render(text, True, (text_color)) 
        text_rect = label.get_rect(center = rect_button.center)  # Centra el texto en el botón
        self.screen.blit(label, text_rect.topleft)

    def run(self):

        level_option = None
        while level_option is None:

            self.screen.blit(self.background, (0, 0))

            button_level1_rect = pygame.Rect(self.width // 2 - width_button // 2, self.height // 2 - 2 * height_button, width_button, height_button)
            button_level2_rect = pygame.Rect(self.width // 2 - width_button // 2, self.height // 2 - height_button // 2, width_button, height_button)
            button_level3_rect = pygame.Rect(self.width // 2 - width_button // 2, self.height // 2 + height_button, width_button, height_button)
            button_back_rect = pygame.Rect(self.width // 2 - width_button // 2, self.height // 2 + 2.5 * height_button, width_button, height_button)

            self.draw_button("NIVEL 1", GRIS, NEGRO, BUTTON_COLOR, button_level1_rect)
            self.draw_button("NIVEL 2", GRIS, NEGRO, BUTTON_COLOR, button_level2_rect)
            self.draw_button("NIVEL 3", GRIS, NEGRO, BUTTON_COLOR, button_level3_rect)
            self.draw_button("REGRESAR AL MENU", GRIS, NEGRO, BUTTON_COLOR, button_back_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if button_level1_rect.collidepoint(x, y):
                        level_option = "NIVEL 1" 
                    elif button_level2_rect.collidepoint(x, y):
                        level_option = "NIVEL 2" 
                    elif button_level3_rect.collidepoint(x, y):
                        level_option = "NIVEL 3" 
                    elif button_back_rect.collidepoint(x, y):
                        level_option = "REGRESAR"

            pygame.display.flip()

        return level_option
