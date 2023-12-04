import pygame, sys
from config import GRIS, NEGRO, BUTTON_COLOR, height_button, width_button


class GameOver:
    def __init__(self, screen, width, height, path_background_gameover, path_image_game_over, score):
        self.screen = screen
        self.width = width
        self.height = height
        self.background = pygame.transform.scale(pygame.image.load(path_background_gameover),(self.width, self.height))
        self.image_game_over = pygame.transform.scale(pygame.image.load(path_image_game_over), (800, 400))
        # self.player_name = player_name
        self.score = score


    def draw_button(self, text, color_button, bg_color_hoover, text_color, rect_button):
        if rect_button.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(self.screen, bg_color_hoover, rect_button, border_radius=25)
        else:
            pygame.draw.rect(self.screen, color_button, rect_button, border_radius=25)
        font = pygame.font.Font(None, 52)
        label = font.render(text, True, (text_color)) 
        text_rect = label.get_rect(center = rect_button.center)  # Centra el texto en el botón
        self.screen.blit(label, text_rect.topleft)

    def run(self, player_name):
        
        game_over = True
        while game_over:
            self.screen.blit(self.background, (0, 0))

            button_restart_rect = pygame.Rect(self.width // 2 - width_button // 2, self.height // 2 + 300, width_button, height_button)

            self.draw_button("RESTART", GRIS, NEGRO, BUTTON_COLOR, button_restart_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if button_restart_rect.collidepoint(x, y):
                        
                        game_over = False
            
            self.screen.blit(self.image_game_over, (self.width // 2 - 400, self.height // 2 - 200)) 
            
            # Dibujar el nombre del jugador y la puntuación
            font = pygame.font.Font(None, 52)
            name_label = font.render("Player: " + str(player_name), True, GRIS) 
            score_label = font.render("Score: " + str(self.score[0]), True, GRIS) 
            self.screen.blit(name_label, (50, 50))
            self.screen.blit(score_label, (50, 100))
            
            pygame.display.flip()

        return "REINICIAR"

    # def restart(self):
    #     global run, FPS, scroll_tresh, screen_scroll, background_scroll, player_name, run_menu, ver_puntuacion,sword_attack, shoot, magic_attack, moving_right, moving_left, jump, in_the_air, alive, flip_claw, gravity, time_last_shot, shot_interval, jump_velocity, qty_idle_images_claw, qty_running_images_claw, qty_jump_images_claw, qty_sword_attack_images_claw, qty_shoot_images_claw, qty_magic_attack_images_claw, qty_fall_images_claw, qty_death_images_claw, player_is_hurt, scale_claw, score, damage_interval, last_damage_time,speed_bullet, scale_bullet, x_bullet, y_bullet,enemy_alive, flip_enemy, moving_left_enemy, moving_right_enemy, qty_idle_images_enemy, qty_walking_images_enemy, qty_attack_images_enemy, health_enemy, is_hurt_enemy, speed_enemy, shots_recived, flee_health, attack_range, scale_enemy, pos_y_enemy1, pos_y_enemy2, qty_enemy,width_menu_screen, height_menu_screen, width_button, height_button,animation_cooldown_claw, animation_cooldown_enemy,tile_size, position_x_tile, speed_map, multiplier_scroll, scroll_start,qty_coins, coin_width, coin_height, pos_y_coins,background_x, background_y,pos_x_live_bar, pos_y_live_bar, width_bar, height_bar, percentage_live, percentage_magic, pos_x_magic_bar, pos_y_magic_bar    # Restablece todas las variables y estados del juego a sus valores iniciales
    
        