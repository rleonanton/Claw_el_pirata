import pygame
import csv

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, tile_size, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))

class Level:
    def __init__(self, file_name, tile_size):
        self.data = self.load_map(file_name)
        self.height = len(self.data)
        self.width = len(self.data[0])
        self.cell_size = tile_size
        self.platforms_group = pygame.sprite.Group()

    def load_map(self, file_name):
        with open(file_name, 'r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            return [list(map(int, row)) for row in csv_reader]

    def create_platforms(self):
        for row in range(self.height):
            for col in range(self.width):
                tile_value = self.data[row][col]
                if tile_value == 9 or tile_value == 18:
                    x = col * self.cell_size
                    y = row * self.cell_size
                    platform = Platform(x, y, self.cell_size, self.get_platform_image(tile_value))
                    self.platforms_group.add(platform)

    def get_platform_image(self, tile_value):
        if tile_value == 9:
            return pygame.Surface((self.cell_size, self.cell_size))  # Cambia según tus imágenes
        elif tile_value == 18:
            return pygame.Surface((self.cell_size, self.cell_size))  # Cambia según tus imágenes

# class Game:
#     def __init__(self):
#         pygame.init()
#         self.screen = pygame.display.set_mode((800, 600))
#         self.clock = pygame.time.Clock()
#         self.current_level = None
#         self.level_index = 0
#         self.levels = [
#             Level("level1.csv", 32),  # Reemplaza "level1.csv" con tus archivos de nivel
#             Level("level2.csv", 32),  # Agrega más niveles según sea necesario
#         ]
#         self.load_level()

#     def load_level(self):
#         self.current_level = self.levels[self.level_index]
#         self.current_level.create_platforms()

#     def run(self):
#         running = True
#         while running:
#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     running = False

#             # Lógica del juego aquí
#             # Verifica si el jugador ha alcanzado ciertos límites para cambiar de nivel

#             # Dibuja el nivel actual
#             self.current_level.platforms_group.draw(self.screen)

#             pygame.display.flip()
#             self.clock.tick(60)

#         pygame.quit()

# if __name__ == "__main__":
#     game = Game()
#     game.run()