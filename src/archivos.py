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
        with open(self.file_path, "a") as file:
            json.dump({"name": name, "score": score}, file)
            file.write("\n")

    def update_high_scores(self, name, score):
        high_scores = []

        if os.path.isfile(self.file_path):
            with open(self.file_path, "r") as file:
                for line in file:
                    entry = json.loads(line.strip())
                    if isinstance(entry, dict) and "score" in entry and isinstance(entry["score"], int):
                        high_scores.append(entry)

        high_scores.append({"name": name, "score": score})
        high_scores.sort(key=lambda x: x["score"], reverse=True)
        high_scores = high_scores[:5]

        with open(self.file_path, "w") as file:
            for entry in high_scores:
                json.dump(entry, file)
                file.write("\n")

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
                high_scores = [json.loads(line.strip()) for line in file if line.strip()]

        font = pygame.font.Font(None, 70)
        y = 10  # Coordenada Y inicial para mostrar los puntajes
        for i, entry in enumerate(high_scores, start=1):
            # Dibuja las medallas para los tres primeros lugares
            if i <= 3:
                screen.blit(self.medals[i-1], (650, 50 + y))

            text_surface = font.render(f"Puntaje {i}: {entry['name']}     {entry['score']}", True, color)
            screen.blit(text_surface, (700, 50 + y))  # Ajusta la coordenada X para dejar espacio para la medalla
            y += text_surface.get_height() + 5
