import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("River Raid")

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 105, 148)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Clock for controlling frame rate
clock = pygame.time.Clock()

highest_score = 0
main_menu = True
game_over = False


# Load the sprite sheet
sprite_sheet = pygame.image.load(r"atari.png").convert_alpha()

# Function to display text on the screen
def draw_text(surface, text, size, x, y, color=(255, 255, 255)):
    font = pygame.font.SysFont(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    surface.blit(text_surface, text_rect)


# Define AirplaneEnemy class
class AirplaneEnemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.original_image = sprite_sheet.subsurface(pygame.Rect(40, 49, 16, 6))  # Adjust coordinates
        self.original_image = pygame.transform.scale(self.original_image, (50, 20))
        self.original_image.set_colorkey((45, 50, 184))  # Set transparency color
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(x, y))
        self.speed_x = 4  # Horizontal speed
        self.speed_y = 3  # Downward scrolling speed
        self.direction = -1  # 1 for moving right, -1 for moving left
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        # Move horizontally
        self.rect.x += self.speed_x * self.direction

        # Move downward
        self.rect.y += self.speed_y

        # Check for edges and flip direction if necessary
        if self.rect.right >= WIDTH and self.direction == 1:  # Hit the right edge
            self.direction = -1
            self.image = pygame.transform.flip(self.original_image, True, False)
            self.image.set_colorkey((45, 50, 184))  # Reset colorkey after flipping
            self.mask = pygame.mask.from_surface(self.image)  # Update mask after flipping
        elif self.rect.left <= 0 and self.direction == -1:  # Hit the left edge
            self.direction = 1
            self.image = pygame.transform.flip(self.original_image, True, False)
            self.image.set_colorkey((45, 50, 184))  # Reset colorkey after flipping
            self.mask = pygame.mask.from_surface(self.image)  # Update mask after flipping

        # Remove the airplane if it goes off-screen at the bottom
        if self.rect.top > HEIGHT:
            self.kill()


class Bridge(pygame.sprite.Sprite):
    def __init__(self, y):
        super().__init__()
        self.image = sprite_sheet.subsurface(pygame.Rect(172, 16, 63, 22))  # Bridge sprite coordinates
        self.image = pygame.transform.scale(self.image, (WIDTH - 200, 30))  # Width to fit river
        self.image.set_colorkey((45, 50, 184))
        self.rect = self.image.get_rect(center=(WIDTH // 2, y))  # Center on the river
        self.mask = pygame.mask.from_surface(self.image)
        self.speed_y = 3  # Scroll speed

    def update(self):
        # Move downward
        self.rect.y += self.speed_y

        # Remove if off-screen
        if self.rect.top > HEIGHT:
            self.kill()


class Street(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = sprite_sheet.subsurface(pygame.Rect(67, 14, 16, 26))  # Street sprite coordinates
        self.image = pygame.transform.scale(self.image, (100, 30))  # Width to fit grass
        self.image.set_colorkey((45, 50, 184))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed_y = 3  # Scroll speed

    def update(self):
        # Move downward
        self.rect.y += self.speed_y

        # Remove if off-screen
        if self.rect.top > HEIGHT:
            self.kill()


# Define Player class
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = sprite_sheet.subsurface(pygame.Rect(25, 15, 16, 17))
        self.image = pygame.transform.smoothscale(self.image, (40, 50))
        self.image.set_colorkey((45, 50, 184))  # Replace with the unwanted color
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 5
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, keys):
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        self.rect.x = max(100, min(WIDTH - 100 - self.rect.width, self.rect.x))
        self.rect.y = min(HEIGHT - 50, min(WIDTH - 100 - self.rect.width, self.rect.y) )

# Define Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill(RED)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = -10

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()


# Define Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = sprite_sheet.subsurface(pygame.Rect(4, 56, 32, 15))
        self.image = pygame.transform.scale(self.image, (55, 39))
        self.image.set_colorkey((45, 50, 184))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 3
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()


# Define FuelTank class
class FuelTank(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = sprite_sheet.subsurface(pygame.Rect(150, 12, 20, 30))
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.image.set_colorkey((45, 50, 184))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 3
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()


# Initialize game objects
player = Player(WIDTH // 2, HEIGHT - 50)
player_group = pygame.sprite.GroupSingle(player)

airplane_enemies = pygame.sprite.Group()  # Group for horizontal airplane enemies
bullets = pygame.sprite.Group()
enemies = pygame.sprite.Group()
fuel_tanks = pygame.sprite.Group()
streets = pygame.sprite.Group()
bridge_enemies = pygame.sprite.Group()

# Background scrolling
background_height = 800
background_surface = pygame.Surface((WIDTH, background_height))
background_surface.fill(BLUE)
pygame.draw.rect(background_surface, (34, 139, 34), (0, 0, 100, background_height))
pygame.draw.rect(background_surface, (34, 139, 34), (WIDTH - 100, 0, 100, background_height))
background_y = 0
scroll_speed = 3

# Game variables
fuel = 100
max_fuel = 100
fuel_depletion_rate = 0.05
fuel_bar_width = 200
fuel_bar_height = 20
score = 0
scroll_speed = 3
difficulty_timer = 0
font = pygame.font.SysFont(None, 36)
enemy_spawn_chance = 100  # Probability of spawning a vertical enemy
airplane_spawn_chance = 200  # Probability of spawning an airplane enemy
running = True

# Main menu loop
while main_menu:
    screen.fill(BLUE)
    draw_text(screen, "River Raid", 64, WIDTH // 2, HEIGHT // 2 - 50, WHITE)
    draw_text(screen, "Press any key to start", 36, WIDTH // 2, HEIGHT // 2 + 50, WHITE)
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            main_menu = False


# Game loop
while running:
    keys = pygame.key.get_pressed()

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            bullet = Bullet(player.rect.centerx, player.rect.top)
            bullets.add(bullet)

    # Background scrolling
    background_y += scroll_speed
    if background_y >= background_height:
        background_y = 0
        
    # Increase difficulty over time    
    difficulty_timer += 1
    if difficulty_timer % 600 == 0:  # Every 10 seconds (assuming 60 FPS)
        scroll_speed += 0.2  # Increase scroll speed
        fuel_depletion_rate += 0.005  # Increase fuel depletion
        # Decrease enemy spawn probabilities
        enemy_spawn_chance = max(1, int(100 - difficulty_timer // 600))
        airplane_spawn_chance = max(1, int(200 - difficulty_timer // 600 * 2))    

    # Spawn enemies
    if random.randint(1, enemy_spawn_chance) == 1:
        enemy = Enemy(random.randint(100, WIDTH - 100), -50)
        enemies.add(enemy)
    
    # Spawn airplanes
    if random.randint(1, airplane_spawn_chance) == 1:  # Adjust spawn probability
       airplane_enemy = AirplaneEnemy(random.randint(50, WIDTH - 50), -50)
       airplane_enemies.add(airplane_enemy)

    if random.randint(1, 500) == 1:  # Adjust spawn probability
        y = -50  # Start above the screen
        bridge = Bridge(y + 13)
        left_street = Street(0, y)  # Left side
        right_street = Street(WIDTH - 100, y)  # Right side

        # Add them to the appropriate groups
        bridge_enemies.add(bridge)  # Bridge is treated as an enemy
        streets.add(left_street, right_street)  # Separate group for streets


    # Spawn fuel tanks
    if random.randint(1, 200) == 1:
        fuel_tank = FuelTank(random.randint(100, WIDTH - 100), -50)
        fuel_tanks.add(fuel_tank)

    # Update player, bullets, enemies, and fuel tanks
    player_group.update(keys)
    bullets.update()
    enemies.update()
    fuel_tanks.update()
    airplane_enemies.update()
    streets.update()
    bridge_enemies.update()

    # Collision: Player and enemies
    if pygame.sprite.spritecollide(player, enemies, False, pygame.sprite.collide_mask):
        print("Game Over! Enemy hit the player.")
        game_over = True
        running = False

    # Collision: Bullets and enemies
    for bullet in bullets:
        hit_enemies = pygame.sprite.spritecollide(bullet, enemies, True, pygame.sprite.collide_mask)
        if hit_enemies:
            bullet.kill()
            score += 10

    # Collision: Bullets and fuel tanks
    for bullet in bullets:
        hit_tanks = pygame.sprite.spritecollide(bullet, fuel_tanks, True, pygame.sprite.collide_mask)
        if hit_tanks:
            bullet.kill()

    # Collision: Player and fuel tanks
    hit_fuel_tanks = pygame.sprite.spritecollide(player, fuel_tanks, True, pygame.sprite.collide_mask)
    for tank in hit_fuel_tanks:
        fuel = min(fuel + 20, max_fuel)

    # Collision: Player and airplane enemies
    if pygame.sprite.spritecollide(player, airplane_enemies, False, pygame.sprite.collide_mask):
      print("Game Over! Airplane enemy hit the player.")
      game_over = True
      running = False

    # Collision: Bullets and airplane enemies
    for bullet in bullets:
        hit_airplanes = pygame.sprite.spritecollide(bullet, airplane_enemies, True, pygame.sprite.collide_mask)
        if hit_airplanes:
           bullet.kill()
           score += 15  # Higher score for airplane enemies

    if pygame.sprite.spritecollide(player, bridge_enemies, False, pygame.sprite.collide_mask):
        print("Game Over! You hit the bridge.")
        game_over = True
        running = False

    for bullet in bullets:
        hit_bridges = pygame.sprite.spritecollide(bullet, bridge_enemies, True, pygame.sprite.collide_mask)
        if hit_bridges:
            bullet.kill()
            score += 20  # Increase score for destroying the bridge

    
    # Deplete fuel
    fuel -= fuel_depletion_rate
    if fuel <= 0:
        print("Game Over! Out of fuel.")
        game_over = True
        running = False

    
    
    # Render objects
    screen.fill(WHITE)
    screen.blit(background_surface, (0, background_y))
    screen.blit(background_surface, (0, background_y - background_height))

    player_group.draw(screen)
    bullets.draw(screen)
    enemies.draw(screen)
    fuel_tanks.draw(screen)
    streets.draw(screen)
    bridge_enemies.draw(screen)

    # Draw fuel bar
    pygame.draw.rect(screen, RED, (10, HEIGHT - 30, fuel_bar_width, fuel_bar_height))
    pygame.draw.rect(screen, GREEN, (10, HEIGHT - 30, int(fuel_bar_width * (fuel / max_fuel)), fuel_bar_height))

    # Draw score
    score_text = font.render(f"Score: {int(score)}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

    # Draw airplane
    airplane_enemies.draw(screen)

    pygame.display.flip()
    clock.tick(60)

    # Update the highest score
    if score > highest_score:
        highest_score = score
    
    # Game over menu
    while game_over:
        screen.fill(BLUE)
        draw_text(screen, "Game Over", 64, WIDTH // 2, HEIGHT // 2 - 100, WHITE)
        draw_text(screen, f"Your Score: {int(score)}", 36, WIDTH // 2, HEIGHT // 2, WHITE)
        draw_text(screen, f"Highest Score: {highest_score}", 36, WIDTH // 2, HEIGHT // 2 + 50, WHITE)
        draw_text(screen, "Press R to Restart or Q to Quit", 36, WIDTH // 2, HEIGHT // 2 + 100, WHITE)
        pygame.display.flip()   

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    # Reset game variables
                    score = 0
                    fuel = 100
                    scroll_speed = 2
                    difficulty_timer = 0    

                    # Clear all sprite groups
                    bullets.empty()
                    enemies.empty()
                    airplane_enemies.empty()
                    fuel_tanks.empty()
                    streets.empty()
                    bridge_enemies.empty()  

                    # Reset the player position
                    player.rect.centerx = WIDTH // 2
                    player.rect.bottom = HEIGHT - 20    

                    # Exit game over menu and restart the game
                    game_over = False
                    running = True
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()


#pygame.quit()
#sys.exit()