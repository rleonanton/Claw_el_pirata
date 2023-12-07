import pygame, os, json

class HighScores:
    def __init__(self, file_path, width, height, background_image_path, path_image_top_1, path_image_top_2, path_image_top_3):
        self.file_path = file_path
        self.width = width
        self.height = height
        self.background_image = pygame.transform.scale(pygame.image.load(background_image_path), (self.width, self.height))
        self.medals = [pygame.transform.scale(pygame.image.load(path_image_top_1), (40, 40)),\
                    pygame.transform.scale(pygame.image.load(path_image_top_2), (40, 40)),\
                    pygame.transform.scale(pygame.image.load(path_image_top_3), (40, 40))]

    def save_high_score(self, name, score):
        high_scores = []

        # Carga las puntuaciones altas existentes
        if os.path.isfile(self.file_path):
            with open(self.file_path, "r") as file:
                try:
                    high_scores = json.load(file)
                except json.JSONDecodeError:
                    print("Error: No se pudo analizar el archivo JSON. Asegúrate de que el archivo tenga un formato JSON válido.")

        # Añade la nueva puntuación alta
        high_scores.append({"name": name, "score": score})

        # Guarda todas las puntuaciones altas en el archivo
        with open(self.file_path, "w") as file:
            json.dump(high_scores, file)

    def update_high_scores(self, name, score):
        high_scores = []

        # Carga las puntuaciones altas existentes
        if os.path.isfile(self.file_path):
            with open(self.file_path, "r") as file:
                try:
                    high_scores = json.load(file)
                except json.JSONDecodeError:
                    print("Failed to parse JSON file")

        # Añade la nueva puntuación alta
        high_scores.append({"name": name, "score": score})

        # Ordena las puntuaciones altas y guarda las 5 mejores
        high_scores.sort(key=lambda x: x["score"], reverse=True)
        high_scores = high_scores[:5]

        # Guarda las 5 mejores puntuaciones altas en el archivo
        with open(self.file_path, "w") as file:
            json.dump(high_scores, file)

    def draw_button(self, text, color_button, bg_color_hoover, text_color, rect_button):
        if rect_button.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(self.screen, bg_color_hoover, rect_button, border_radius=25)
        else:
            pygame.draw.rect(self.screen, color_button, rect_button, border_radius=25)
        font = pygame.font.Font(None, 52)
        label = font.render(text, True, (text_color)) 
        text_rect = label.get_rect(center = rect_button.center)  # Centra el texto en el botón
        self.screen.blit(label, text_rect.topleft)

    def show_high_scores(self, screen, color):
        # Dibuja el fondo
        screen.blit(self.background_image, (0, 0))

        high_scores = []
        if os.path.isfile(self.file_path):
            with open(self.file_path, "r") as file:
                try:
                    high_scores = json.load(file)
                except json.JSONDecodeError:
                    print("Failed to parse JSON file")

        # print(high_scores)  # Imprime las puntuaciones altas

        font = pygame.font.Font(None, 70)
        y = 10  # Coordenada Y inicial para mostrar los puntajes
        for i, entry in enumerate(high_scores, start=1):
            # Dibuja las medallas para los tres primeros lugares
            if i <= 3:
                screen.blit(self.medals[i-1], (650, 50 + y))

            text_surface = font.render(f"Puntaje {i}: {entry['name']}     {entry['score']}", True, color)
            screen.blit(text_surface, (700, 50 + y))
            y += text_surface.get_height() + 5

