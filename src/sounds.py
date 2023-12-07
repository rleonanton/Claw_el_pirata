import pygame

class Sounds:
    def __init__(self, main_sound_path, running_sound_path, shoot_sound_path, sword_sound_path, game_over_sound_path, magic_attack_sound_path, canon_final_boss_sound_path, win_sound_path):
        pygame.mixer.init()  # Inicializa el módulo mixer

        pygame.mixer.music.load(main_sound_path)
        self.running_sound = pygame.mixer.Sound(running_sound_path)
        self.shoot_sound = pygame.mixer.Sound(shoot_sound_path)
        self.sword_sound = pygame.mixer.Sound(sword_sound_path)
        self.game_over_sound = pygame.mixer.Sound(game_over_sound_path)
        self.magic_attack_sound = pygame.mixer.Sound(magic_attack_sound_path)
        self.canon_final_boss_sound = pygame.mixer.Sound(canon_final_boss_sound_path)
        self.win_sound = pygame.mixer.Sound(win_sound_path)

    def set_volume(self, volume):
        pygame.mixer_music.set_volume(volume)
        self.running_sound.set_volume(volume)
        self.shoot_sound.set_volume(volume)
        self.sword_sound.set_volume(volume)


    def play_main(self):
        pygame.mixer.music.play(-1)

    def play_running(self):
        self.running_sound.play()

    def play_shoot(self):
        self.shoot_sound.play()

    def play_sword(self):
        self.sword_sound.play()

    def play_game_over(self):
        self.game_over_sound.play()

    def play_magic_attack(self):
        self.magic_attack_sound.play()
    
    def play_canon_final_boss(self):
        self.canon_final_boss_sound.play()
    
    def play_win(self):
        self.win_sound.play()

    def pause_main(self):
        pygame.mixer.music.pause()