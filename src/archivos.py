import pygame, os, json

class HighScores:
    def __init__(self, file_path, width, height):
        self.file_path = file_path
        self.width = width
        self.height = height

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
        high_scores = []

        if os.path.isfile(self.file_path):
            with open(self.file_path, "r") as file:
                high_scores = [json.loads(line.strip()) for line in file]

        font = pygame.font.Font(None, 70)
        y = 10  # Coordenada Y inicial para mostrar los puntajes
        for i, entry in enumerate(high_scores, start=1):
            text_surface = font.render(f"Puntaje {i}: {entry['name']}     {entry['score']}", True, color)
            screen.blit(text_surface, (self.width // 2 - text_surface.get_width() + 240, 50 + y))
            y += text_surface.get_height() + 5
