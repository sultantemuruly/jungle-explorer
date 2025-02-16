import pygame

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
VELOCITY = 5

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Create screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Basic Pygame Scene")

# Player setup
player_size = 50
player_x, player_y = WIDTH // 2, HEIGHT // 2

# Game loop
running = True
while running:
    pygame.time.delay(30)  # Control frame rate
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Movement handling
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and player_y - VELOCITY > 0:
        player_y -= VELOCITY
    if keys[pygame.K_s] and player_y + VELOCITY + player_size < HEIGHT:
        player_y += VELOCITY
    if keys[pygame.K_a] and player_x - VELOCITY > 0:
        player_x -= VELOCITY
    if keys[pygame.K_d] and player_x + VELOCITY + player_size < WIDTH:
        player_x += VELOCITY
    
    # Drawing
    screen.fill(WHITE)
    pygame.draw.rect(screen, RED, (player_x, player_y, player_size, player_size))
    pygame.display.update()
    
# Quit pygame
pygame.quit()
