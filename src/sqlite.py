import pygame
import sqlite3
import json

class Sqlite:
    def __init__(self, width, height):
        self.connection = sqlite3.connect("src/scores.db")
        self.cursor = self.connection.cursor()
        self.cursor.execute("CREATE TABLE if not exists scores (player text, score int)")
        self.connection.commit()

        self.width = width
        self.height = height
        pygame.init()
        self.display_surface = pygame.display.set_mode((self.width, self.height))

        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.font = pygame.font.Font('freesansbold.ttf', 32)

    def insert_score(self, player, score):
        self.cursor.execute("INSERT INTO scores VALUES (?,?)", (player, score))
        self.connection.commit()

    def get_top_scores(self):
        self.cursor.execute("SELECT * FROM scores ORDER BY score DESC LIMIT 5")
        output = self.cursor.fetchall()
        return output

    def load_scores_from_json(self, filename):
        with open(filename, 'r') as f:
            data = json.load(f)

        for item in data:
            self.insert_score(item['name'], item['score'])

    def game_loop(self, top_scores):

        run_sqlite = True
        while run_sqlite:
            self.display_surface.fill(self.white)
            top_scores = self.get_top_scores()
            for i, (player, score) in enumerate(top_scores):
                text = self.font.render(f"{player}: {score}", True, self.black, self.white)
                textRect = text.get_rect()
                textRect.center = (self.width // 2, 200 + (i+1)*self.height // 12)

                self.display_surface.blit(text, textRect)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.connection.close()
                    run_sqlite = False
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:  # Presionar ESC para regresar al menú
                        run_sqlite = False
            pygame.display.update()



