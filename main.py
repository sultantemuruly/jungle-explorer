import pygame
from scene_manager import SceneManager

pygame.init()

WIDTH, HEIGHT = 800, 600
VELOCITY = 5
BROWN = (108, 72, 10)
BLUE = (0, 94, 201)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Basic Pygame Scene")

player_size = 50
player_x, player_y = WIDTH // 2, HEIGHT // 2

# Load background image and scale it to fit the screen, then darken it
bg_image = pygame.image.load("public/bg.png")
bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))
dark_overlay = pygame.Surface((WIDTH, HEIGHT))
dark_overlay.set_alpha(100)
dark_overlay.fill((0, 0, 0))

# Load player image
player_image = pygame.image.load("public/player.png")
player_image = pygame.transform.scale(player_image, (player_size, player_size))

scene_manager = SceneManager(WIDTH, HEIGHT)

running = True
while running:
    pygame.time.delay(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if scene_manager.show_next_button:
                mouse_pos = pygame.mouse.get_pos()
                if scene_manager.is_next_button_clicked(mouse_pos):
                    scene_manager.go_to_next_scene()

    if not scene_manager.show_next_button and not scene_manager.is_game_over():
        keys = pygame.key.get_pressed()
        if scene_manager.current_scene == 1:
            if keys[pygame.K_w]:
                potential_rect = pygame.Rect(
                    player_x, player_y - VELOCITY, player_size, player_size
                )
                if (
                    player_y - VELOCITY > 0
                    and not scene_manager.maze.check_wall_collision(potential_rect)
                ):
                    player_y -= VELOCITY
            if keys[pygame.K_s]:
                potential_rect = pygame.Rect(
                    player_x, player_y + VELOCITY, player_size, player_size
                )
                if (
                    player_y + VELOCITY + player_size < HEIGHT
                    and not scene_manager.maze.check_wall_collision(potential_rect)
                ):
                    player_y += VELOCITY
            if keys[pygame.K_a]:
                potential_rect = pygame.Rect(
                    player_x - VELOCITY, player_y, player_size, player_size
                )
                if (
                    player_x - VELOCITY > 0
                    and not scene_manager.maze.check_wall_collision(potential_rect)
                ):
                    player_x -= VELOCITY
            if keys[pygame.K_d]:
                potential_rect = pygame.Rect(
                    player_x + VELOCITY, player_y, player_size, player_size
                )
                if (
                    player_x + VELOCITY + player_size < WIDTH
                    and not scene_manager.maze.check_wall_collision(potential_rect)
                ):
                    player_x += VELOCITY
        else:
            if keys[pygame.K_w] and player_y - VELOCITY > 0:
                player_y -= VELOCITY
            if keys[pygame.K_s] and player_y + VELOCITY + player_size < HEIGHT:
                player_y += VELOCITY
            if keys[pygame.K_a] and player_x - VELOCITY > 0:
                player_x -= VELOCITY
            if keys[pygame.K_d] and player_x + VELOCITY + player_size < WIDTH:
                player_x += VELOCITY

    player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
    scene_manager.check_scene_transition(player_rect)

    if scene_manager.current_scene == 1:
        if scene_manager.maze.check_collision(player_rect):
            player_x, player_y = WIDTH // 2, HEIGHT // 2
            scene_manager.current_scene = 0
            scene_manager.game_over = False
            scene_manager.show_next_button = False

    if scene_manager.current_scene == 2:
        scene_manager.update_third_scene(player_rect)
        if player_rect.colliderect(scene_manager.enemy_rect):
            player_x, player_y = WIDTH // 2, HEIGHT // 2
            scene_manager.current_scene = 0
            scene_manager.game_over = False
            scene_manager.show_next_button = False
        elif player_rect.colliderect(scene_manager.portal):
            scene_manager.go_to_next_scene()

    screen.blit(bg_image, (0, 0))
    screen.blit(dark_overlay, (0, 0))

    scene_manager.draw_current_scene(screen)

    if not scene_manager.show_next_button and not scene_manager.is_game_over():
        screen.blit(player_image, (player_x, player_y))

    pygame.display.update()

    if scene_manager.is_game_over():
        pygame.time.delay(2000)
        running = False

pygame.quit()
