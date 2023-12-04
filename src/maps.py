import pygame
import csv


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, tile_size, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.mask = pygame.mask.from_surface(self.image)
        

class Map:
    def __init__(self, file_name, tile_size, position_x_tile, speed_map):
        self.data = self.load_map(file_name)
        self.height = len(self.data)
        self.width = len(self.data[0])
        self.cell_size = tile_size
        self.position_x = position_x_tile
        self.speed = speed_map
        self.platforms_group = pygame.sprite.Group()
        self.right_key_pressed = False
        self.left_key_pressed = False

    def load_map(self, file_name):
        with open(file_name, 'r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            return [list(map(int, row)) for row in csv_reader]

    def create_platform(self, x, y, tile_value):
        image = self.get_platform_image(tile_value)
        platform = Platform(x, y, self.cell_size, image)
        self.platforms_group.add(platform)

    def get_platform_image(self, tile_value):
        if tile_value == 9:
            return pygame.transform.scale(pygame.image.load("src/claw_images/otras imagenes/block.png"), (self.cell_size // 2, self.cell_size // 2))
        elif tile_value == 18:
            return pygame.transform.scale(pygame.image.load("src/claw_images/otras imagenes/techblocks.png"), (self.cell_size // 2, self.cell_size // 2))
        elif tile_value == 1235:
            return pygame.transform.scale(pygame.image.load("src/claw_images/otras imagenes/level2_tile2.png"), (self.cell_size // 2, self.cell_size // 2))
        elif tile_value == 1429:
            return pygame.transform.scale(pygame.image.load("src/claw_images/otras imagenes/level2_tile1.png"), (self.cell_size // 2, self.cell_size // 2))
        else:
            return pygame.Surface((self.cell_size, self.cell_size))

    def get_platform_rects(self):
        return [platform.rect for platform in self.platforms_group]
    
    def get_platform_masks(self):
        return [platform.mask for platform in self.platforms_group]

    def get_value(self, row, column):
        try:
            return self.data[row][column]
        except IndexError:
            raise IndexError("Índices fuera de rango en el mapa")

    def draw(self, screen):
        for row in range(self.height):
            for col in range(self.width):
                tile_value = self.get_value(row, col)
                image = self.get_platform_image(tile_value)
                screen.blit(image, (col * self.cell_size + self.position_x, row * self.cell_size))