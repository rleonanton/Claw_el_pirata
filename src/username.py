import pygame, sys

class UsernameScreen:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        self.username = ""
        self.active = False

    def draw_input_box(self, rect, text=''):

        font = pygame.font.Font(None, 32)
        color_inactive = pygame.Color('lightskyblue3')
        color_active = pygame.Color('dodgerblue2')
        color = color_active if self.active else color_inactive

        txt_surface = font.render(text, True, color)
        width = max(200, txt_surface.get_width()+10)
        rect.w = width
        self.screen.blit(txt_surface, (rect.x+5, rect.y+5))
        pygame.draw.rect(self.screen, color, rect, 2)

    def handle_event(self, event, rect):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    return self.username
                if event.key == pygame.K_BACKSPACE:
                    self.username = self.username[:-1]
                else:
                    if event.unicode.isalnum():
                        self.username += event.unicode

    def run(self):
        font = pygame.font.Font(None, 32)
        text_surface = font.render("Ingrese aqui su nombre de usuario y presione ENTER para continuar", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(self.width // 2, self.height // 2 - 50))
        input_box_rect = pygame.Rect(self.width // 2 - 100, self.height // 2, 140, 32)
        
        while True:
            self.screen.fill((30, 30, 30))
            self.screen.blit(text_surface, text_rect)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                self.handle_event(event, input_box_rect)

            # Check if Enter key is pressed
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RETURN] and self.username:
                return self.username

            self.draw_input_box(input_box_rect, self.username)
            pygame.display.flip()