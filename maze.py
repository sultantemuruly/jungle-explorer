import pygame


class Maze:
    def __init__(self, width, height, blueprint_file="maze_blueprint.txt"):
        self.width = width
        self.height = height
        self.blueprint_file = blueprint_file

        self.floor_color = (200, 200, 200)  # Light grey floor
        self.transition_color = (255, 255, 255)  # White for transition zone

        self.walls = []
        self.obstacles = []
        self.transitions = []  # For '1' cells

        self.blueprint_lines = []
        self.cell_size = 40

        # Load images for walls and obstacles
        self.wall_image = pygame.image.load("public/wall.png")
        self.obstacle_image = pygame.image.load("public/obstacle.png")

        self.load_blueprint()

    def load_blueprint(self):
        """
        Reads the blueprint file and creates Rects for:
          - walls ('#')
          - obstacles ('*')
          - transition zones ('1')
        """
        with open(self.blueprint_file, "r") as f:
            self.blueprint_lines = [line.rstrip("\n") for line in f if line.strip()]

        if not self.blueprint_lines:
            return

        num_rows = len(self.blueprint_lines)
        num_cols = max(len(line) for line in self.blueprint_lines)

        self.cell_size = min(self.width // num_cols, self.height // num_rows)

        # Resize images to fit the grid cells
        self.wall_image = pygame.transform.scale(
            self.wall_image, (self.cell_size, self.cell_size)
        )
        self.obstacle_image = pygame.transform.scale(
            self.obstacle_image, (self.cell_size, self.cell_size)
        )

        self.walls = []
        self.obstacles = []
        self.transitions = []

        for row, line in enumerate(self.blueprint_lines):
            for col, char in enumerate(line):
                x = col * self.cell_size
                y = row * self.cell_size
                rect = pygame.Rect(x, y, self.cell_size, self.cell_size)
                if char == "#":
                    self.walls.append(rect)
                elif char == "*":
                    self.obstacles.append(rect)
                elif char == "1":
                    self.transitions.append(rect)

    def draw(self, screen):
        """
        Draws the maze on the provided screen:
        - Draws walls, obstacles, and transition zones
        """
        # screen.fill(self.floor_color)  # Comment out or remove this line to remove the floor

        for wall in self.walls:
            screen.blit(self.wall_image, (wall.x, wall.y))

        for obs in self.obstacles:
            screen.blit(self.obstacle_image, (obs.x, obs.y))

        for trans in self.transitions:
            pygame.draw.rect(screen, self.transition_color, trans)

    def check_collision(self, player_rect):
        """
        Returns True if the player's rectangle collides with any obstacle.
        """
        return any(player_rect.colliderect(obs) for obs in self.obstacles)

    def check_wall_collision(self, player_rect):
        """
        Returns True if the player's rectangle collides with any wall.
        """
        return any(player_rect.colliderect(wall) for wall in self.walls)
