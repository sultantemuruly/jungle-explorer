import pygame

class SceneManager:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.current_scene = 0
        self.scenes = [
            {"rect": pygame.Rect(100, 100, 100, 100), "color": (255, 255, 255)},
            {"rect": pygame.Rect(300, 300, 100, 100), "color": (255, 255, 255)},
            {"rect": pygame.Rect(500, 100, 100, 100), "color": (255, 255, 255)}
        ]
        self.game_over = False
        self.show_next_button = False
        self.next_button = pygame.Rect(width // 2 - 50, height // 2 - 25, 100, 50)

    def check_scene_transition(self, player_rect):
        if self.current_scene < len(self.scenes):
            if player_rect.colliderect(self.scenes[self.current_scene]["rect"]):
                self.show_next_button = True

    def go_to_next_scene(self):
        if self.current_scene < len(self.scenes) - 1:
            self.current_scene += 1
            self.show_next_button = False
        else:
            self.game_over = True

    def draw_current_scene(self, screen):
        if self.game_over:
            self.draw_game_over(screen)
        elif self.show_next_button:
            self.draw_next_button(screen)
        else:
            scene = self.scenes[self.current_scene]
            pygame.draw.rect(screen, scene["color"], scene["rect"])

    def draw_next_button(self, screen):
        font = pygame.font.Font(None, 36)
        pygame.draw.rect(screen, (255, 255, 255), self.next_button)
        text = font.render("Next", True, (0, 0, 0))
        screen.blit(text, (self.next_button.x + 30, self.next_button.y + 15))

    def draw_game_over(self, screen):
        font = pygame.font.Font(None, 74)
        text = font.render("Game Over", True, (255, 0, 0))
        screen.blit(text, (self.width // 2 - 140, self.height // 2 - 50))

    def is_game_over(self):
        return self.game_over

    def is_next_button_clicked(self, mouse_pos):
        return self.next_button.collidepoint(mouse_pos)