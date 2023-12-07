class FinalLevel:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height

        # Inicializa el enemigo
        self.enemy = Enemy()  # Asume que tienes una clase Enemy

        # Inicializa la plataforma
        self.platform = Platform()  # Asume que tienes una clase Platform

    def run(self):
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            # Dibuja la plataforma
            self.platform.draw(self.screen)

            # Dibuja el enemigo
            self.enemy.draw(self.screen)

            # Actualiza la pantalla
            pygame.display.update()

        pygame.quit()
