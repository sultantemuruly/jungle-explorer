import pygame
from scene_manager import SceneManager

pygame.init()

WIDTH, HEIGHT = 800, 600
VELOCITY = 5
GREEN = (47, 201, 10)
BLUE = (0, 94, 201)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Basic Pygame Scene")

player_size = 50
player_x, player_y = WIDTH // 2, HEIGHT // 2

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
    
    screen.fill(GREEN)
    scene_manager.draw_current_scene(screen)
    if not scene_manager.show_next_button and not scene_manager.is_game_over():
        pygame.draw.rect(screen, BLUE, player_rect)
    pygame.display.update()
    
    if scene_manager.is_game_over():
        pygame.time.delay(2000)  # Wait for 2 seconds before closing
        running = False
    
pygame.quit()