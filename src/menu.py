import pygame
import sys
from config import width_button, height_button, NEGRO, GRIS, BUTTON_COLOR

class MainMenu:

    def __init__(self, screen, width, height, path_background_menu, path_image_title, path_image_player, menu_option):
        
        self.screen = screen
        self.menu_option = menu_option
        self.width = width
        self.height = height
        self.background = pygame.transform.scale(pygame.image.load(path_background_menu),(self.width, self.height))
        self.image_title = pygame.transform.scale(pygame.image.load(path_image_title), (600, 200))
        self.image_player = pygame.transform.scale(pygame.image.load(path_image_player), (600, 400))

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

        while self.menu_option is None:
            self.screen.blit(self.background, (0, 0))
            

            button_start_rect = pygame.Rect(self.width // 2 - width_button // 2, self.height // 2 - 2 * height_button, width_button, height_button)
            button_scores_rect = pygame.Rect(self.width // 2 - width_button // 2, self.height // 2 - height_button // 2, width_button, height_button)
            button_niveles_rect = pygame.Rect(self.width // 2 - width_button // 2, self.height // 2 + height_button, width_button, height_button)
            button_exit_rect = pygame.Rect(self.width // 2 - width_button // 2, self.height // 2 + 2.5 * height_button, width_button, height_button)

            # self.draw_button("INICIAR JUEGO", GRIS, NEGRO, BUTTON_COLOR, button_start_rect)
            self.draw_button("VER PUNTUACIONES", GRIS, NEGRO, BUTTON_COLOR, button_scores_rect)
            self.draw_button("NIVELES", GRIS, NEGRO, BUTTON_COLOR, button_niveles_rect)
            self.draw_button("SALIR", GRIS, NEGRO, BUTTON_COLOR, button_exit_rect)

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
                    if button_start_rect.collidepoint(x, y):
                        self.menu_option = "INICIAR JUEGO" 
                    elif button_scores_rect.collidepoint(x, y):
                        self.menu_option = "VER PUNTUACIONES"
                    elif button_niveles_rect.collidepoint(x, y):
                        self.menu_option = "NIVELES"
                    elif button_exit_rect.collidepoint(x, y):
                        pygame.quit()
                        sys.exit()
            
            self.screen.blit(self.image_player, (150, 600))
            self.screen.blit(self.image_title, (640, 100)) 
            pygame.display.flip()

        return self.menu_option
