import pygame


class Maze:
    def __init__(self, width, height, blueprint_file="maze_blueprint.txt"):
        self.width = width
        self.height = height
        self.blueprint_file = blueprint_file

        self.wall_color = (128, 128, 128)  # Grey walls
        self.obstacle_color = (255, 0, 0)  # Red obstacles
        self.floor_color = (200, 200, 200)  # Light grey floor
        self.transition_color = (255, 255, 255)  # White for transition zone

        self.walls = []
        self.obstacles = []
        self.transitions = []  # For '1' cells

        self.blueprint_lines = []

        self.cell_size = 40

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

        # Calculate cell size so the maze fits within the given width and height.
        self.cell_size = min(self.width // num_cols, self.height // num_rows)

        # Clear lists
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
          - Fills the floor
          - Draws walls, obstacles, and transition zones
        """
        screen.fill(self.floor_color)

        for wall in self.walls:
            pygame.draw.rect(screen, self.wall_color, wall)

        for obs in self.obstacles:
            pygame.draw.rect(screen, self.obstacle_color, obs)

        for trans in self.transitions:
            pygame.draw.rect(screen, self.transition_color, trans)

    def check_collision(self, player_rect):
        """
        Returns True if the player's rectangle collides with any red obstacle.
        """
        for obs in self.obstacles:
            if player_rect.colliderect(obs):
                return True
        return False

    def check_wall_collision(self, player_rect):
        """
        Returns True if the player's rectangle collides with any grey wall.
        """
        for wall in self.walls:
            if player_rect.colliderect(wall):
                return True
        return False
