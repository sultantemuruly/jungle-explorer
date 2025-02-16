import pygame
from maze import Maze


class SceneManager:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.current_scene = 0
        self.scenes = [
            {
                "rect": pygame.Rect(100, 100, 100, 100),
                "color": (255, 255, 255),
            },  # Scene 0
            {"rect": None, "color": None},  # Scene 1: Maze
            {"rect": None, "color": None},  # Scene 2: Enemy
        ]
        self.game_over = False
        self.show_next_button = False
        self.next_button = pygame.Rect(width // 2 - 50, height // 2 - 25, 100, 50)

        self.maze = Maze(width, height)

        # Enemy setup
        self.enemy_image = pygame.image.load("public/enemy.png")
        self.enemy_size = 50
        self.enemy_image = pygame.transform.scale(
            self.enemy_image, (self.enemy_size, self.enemy_size)
        )
        self.purple_cube = pygame.Rect(120, 50, self.enemy_size, self.enemy_size)
        self.purple_speed = 2

        self.portal = pygame.Rect(50, 50, 50, 50)

    @property
    def enemy_rect(self):
        return self.purple_cube

    def update_third_scene(self, player_rect):
        """
        Moves the enemy toward the player's center.
        """
        cube_speed = self.purple_speed
        cube_center = self.purple_cube.center
        player_center = player_rect.center
        dx = player_center[0] - cube_center[0]
        dy = player_center[1] - cube_center[1]
        distance = (dx**2 + dy**2) ** 0.5
        if distance != 0:
            move_x = cube_speed * dx / distance
            move_y = cube_speed * dy / distance
        else:
            move_x = move_y = 0
        self.purple_cube.x += int(move_x)
        self.purple_cube.y += int(move_y)

    def check_scene_transition(self, player_rect):
        if self.current_scene == 1:
            for trans in self.maze.transitions:
                if player_rect.colliderect(trans):
                    self.show_next_button = True
                    return
        else:
            if self.current_scene == 0:
                scene_data = self.scenes[self.current_scene]
                if scene_data["rect"] is not None and player_rect.colliderect(
                    scene_data["rect"]
                ):
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
            if self.current_scene == 1:
                self.maze.draw(screen)
            elif self.current_scene == 2:
                pygame.draw.rect(screen, (255, 255, 255), self.portal)
                screen.blit(self.enemy_image, (self.purple_cube.x, self.purple_cube.y))
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
