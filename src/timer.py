import pygame
import time

class Timer:
    def __init__(self, x, y, font_size, font_color, font):

        self.start_time = time.time()
        self.font = pygame.font.Font(font, font_size)
        self.x = x
        self.y = y
        self.font_color = font_color

    def draw(self, screen):
        elapsed_time = int(time.time() - self.start_time)
        remaining_time = max(0, 60 - elapsed_time)
        text = self.font.render("Timer: " + str(remaining_time), True, self.font_color)
        screen.blit(text, (self.x, self.y))

        if remaining_time == 0:
            return True  # El tiempo se acabó
        else:
            return False

    def reset(self):
        self.start_time = time.time()