import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions and settings
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tank Game with Cliffs and Holes")

# Colors
GREEN = (0, 255, 0)
GRAY = (80, 80, 80)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Tank settings
TANK_WIDTH = 50
TANK_HEIGHT = 30
TANK_SPEED = 5

# Game clock
clock = pygame.time.Clock()
FPS = 60

# Terrain class (the road)
def draw_terrain_with_cliffs(cliffs):
    pygame.draw.rect(screen, GRAY, (100, 0, SCREEN_WIDTH - 200, SCREEN_HEIGHT))  # Road
    
    # Draw integrated cliffs
    for cliff in cliffs:
        pygame.draw.rect(screen, WHITE, (0, cliff.y, SCREEN_WIDTH, cliff.height))  # Entire cliff area
        if cliff.gap_side == "LEFT":
            pygame.draw.rect(screen, GRAY, (0, cliff.y, cliff.gap_width, cliff.height))  # Left gap
        elif cliff.gap_side == "RIGHT":
            pygame.draw.rect(screen, GRAY, (SCREEN_WIDTH - cliff.gap_width, cliff.y, cliff.gap_width, cliff.height))  # Right gap

# Tank class
class Tank:
    def __init__(self):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT - TANK_HEIGHT - 10
        self.speed = TANK_SPEED

    def draw(self):
        pygame.draw.rect(screen, GREEN, (self.x, self.y, TANK_WIDTH, TANK_HEIGHT))

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.x > 100:  # Stay within left road boundary
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < SCREEN_WIDTH - 100 - TANK_WIDTH:  # Stay within right road boundary
            self.x += self.speed
        if keys[pygame.K_UP] and self.y > 0:  # Top boundary
            self.y -= self.speed
        if keys[pygame.K_DOWN] and self.y < SCREEN_HEIGHT - TANK_HEIGHT:  # Bottom boundary
            self.y += self.speed

# Hole class
class Hole:
    def __init__(self, x, y, width, speed):
        self.x = x
        self.y = y
        self.width = width
        self.height = 20
        self.speed = speed

    def draw(self):
        pygame.draw.rect(screen, BLACK, (self.x, self.y, self.width, self.height))

    def move(self):
        self.y += self.speed

# Cliff class
class Cliff:
    def __init__(self, y, gap_side, gap_width, speed):
        self.y = y
        self.gap_side = gap_side  # "LEFT" or "RIGHT"
        self.gap_width = gap_width
        self.height = 20
        self.speed = speed

    def move(self):
        self.y += self.speed

# Main game loop
def main():
    tank = Tank()
    holes = []
    cliffs = []
    hole_timer = 0
    cliff_timer = 0
    running = True

    while running:
        screen.fill((0, 0, 0))  # Clear screen

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Tank controls
        keys = pygame.key.get_pressed()
        tank.move(keys)

        # Spawn holes
        hole_timer += 1
        if hole_timer > 100:  # Spawn a hole every 100 frames
            hole_x = random.randint(100, SCREEN_WIDTH - 200 - 50)  # Random within road
            holes.append(Hole(hole_x, -20, random.randint(50, 100), 4))
            hole_timer = 0

        # Spawn cliffs
        cliff_timer += 1
        if cliff_timer > 300:  # Spawn a cliff every 300 frames
            gap_side = random.choice(["LEFT", "RIGHT"])
            gap_width = random.randint(100, 200)
            cliffs.append(Cliff(-20, gap_side, gap_width, 4))
            cliff_timer = 0

        # Move and draw terrain with integrated cliffs
        draw_terrain_with_cliffs(cliffs)

        # Move and draw holes
        for hole in holes[:]:
            hole.move()
            hole.draw()
            if hole.y > SCREEN_HEIGHT:
                holes.remove(hole)

            # Collision with tank
            if (
                tank.x < hole.x + hole.width and
                tank.x + TANK_WIDTH > hole.x and
                tank.y < hole.y + hole.height and
                tank.y + TANK_HEIGHT > hole.y
            ):
                print("Game Over! Fell into a hole.")
                running = False

        # Move and draw cliffs
        for cliff in cliffs[:]:
            cliff.move()
            if cliff.y > SCREEN_HEIGHT:
                cliffs.remove(cliff)

            # Collision with tank
            if cliff.gap_side == "LEFT":
                if tank.x > cliff.gap_width and tank.y < cliff.y + cliff.height and tank.y + TANK_HEIGHT > cliff.y:
                    print("Game Over! Fell off the cliff.")
                    running = False
            elif cliff.gap_side == "RIGHT":
                if tank.x < SCREEN_WIDTH - cliff.gap_width and tank.y < cliff.y + cliff.height and tank.y + TANK_HEIGHT > cliff.y:
                    print("Game Over! Fell off the cliff.")
                    running = False

        # Draw tank
        tank.draw()

        # Update display
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

# Run the game
if __name__ == "__main__":
    main()
 