import pygame
import time

class Timer:
    def __init__(self, x, y, font_size, font_color, font):
        
        self.start_time = time.time()
        self.pause_time = None  # Nuevo atributo para almacenar el tiempo de pausa
        self.font = pygame.font.Font(font, font_size)
        self.x = x
        self.y = y
        self.font_color = font_color

    def draw(self, screen):
        if self.pause_time is not None:
            return False  # El tiempo está pausado, no actualices el temporizador

        elapsed_time = int(time.time() - self.start_time)
        remaining_time = max(0, 120 - elapsed_time)
        text = self.font.render("Timer: " + str(remaining_time), True, self.font_color)
        screen.blit(text, (self.x, self.y))

        if remaining_time == 0:
            return True  # El tiempo se acabó
        else:
            return False

    def reset(self):
        self.start_time = time.time()
        self.pause_time = None  # Reinicia el tiempo de pausa al reiniciar el temporizador

    def pause(self):
        if self.pause_time is None:
            self.pause_time = time.time() - self.start_time

    def unpause(self):
        if self.pause_time is not None:
            self.start_time = time.time() - self.pause_time
            self.pause_time = None
