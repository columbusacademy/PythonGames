import pygame
import sys

# Initialize pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("School Maze Adventure")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Set up player properties
player_size = 50
player_pos = [50, 50]  # Starting position
player_speed = 5

# Game States
LEVELS = ['lower_school', 'middle_school', 'upper_school']
current_level = 0  # Start with 'lower_school'

# Maze design (simple grid-based structure for now)
mazes = {
    'lower_school': [[0, 1, 0, 0, 0],
                     [0, 1, 0, 1, 0],
                     [0, 0, 0, 1, 0],
                     [1, 1, 0, 0, 0],
                     [0, 0, 0, 1, 0]],
    
    'middle_school': [[1, 0, 1, 0, 0],
                      [0, 0, 1, 0, 1],
                      [0, 1, 0, 0, 0],
                      [0, 1, 1, 1, 0],
                      [0, 0, 0, 1, 0]],
    
    'upper_school': [[1, 0, 0, 0, 1],
                     [1, 0, 1, 1, 0],
                     [0, 0, 0, 0, 0],
                     [0, 1, 1, 0, 1],
                     [0, 0, 0, 1, 0]]
}

# Define player images for each level
explorer = pygame.Surface((player_size, player_size))
explorer.fill(RED)
grader_6th = pygame.Surface((player_size, player_size))
grader_6th.fill(GREEN)
freshman = pygame.Surface((player_size, player_size))
freshman.fill(BLUE)

player = explorer  # Start with the explorer

# Functions
def draw_maze(maze):
    """Draw the current maze on the screen."""
    cell_size = WIDTH // len(maze[0])
    for row in range(len(maze)):
        for col in range(len(maze[0])):
            if maze[row][col] == 1:
                pygame.draw.rect(screen, BLACK, (col * cell_size, row * cell_size, cell_size, cell_size))

def is_collision(maze, player_pos):
    """Check for collision with walls."""
    cell_size = WIDTH // len(maze[0])
    row = player_pos[1] // cell_size
    col = player_pos[0] // cell_size
    if maze[row][col] == 1:
        return True
    return False

def level_completed(player_pos, maze):
    """Check if the player has reached the end of the maze."""
    return player_pos[0] >= WIDTH - player_size and player_pos[1] >= HEIGHT - player_size

# Main Game Loop
while True:
    screen.fill(WHITE)
    
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Movement handling
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_pos[0] -= player_speed
    if keys[pygame.K_RIGHT]:
        player_pos[0] += player_speed
    if keys[pygame.K_UP]:
        player_pos[1] -= player_speed
    if keys[pygame.K_DOWN]:
        player_pos[1] += player_speed

    # Collision detection
    if is_collision(mazes[LEVELS[current_level]], player_pos):
        # Undo movement if collision detected
        if keys[pygame.K_LEFT]:
            player_pos[0] += player_speed
        if keys[pygame.K_RIGHT]:
            player_pos[0] -= player_speed
        if keys[pygame.K_UP]:
            player_pos[1] += player_speed
        if keys[pygame.K_DOWN]:
            player_pos[1] -= player_speed

    # Check if the player has completed the level
    if level_completed(player_pos, mazes[LEVELS[current_level]]):
        current_level += 1
        if current_level >= len(LEVELS):
            print("Congratulations! You've completed the game!")
            pygame.quit()
            sys.exit()
        else:
            # Change player character and reset position
            if LEVELS[current_level] == 'middle_school':
                player = grader_6th
            elif LEVELS[current_level] == 'upper_school':
                player = freshman
            player_pos = [50, 50]  # Reset player position

    # Draw the maze
    draw_maze(mazes[LEVELS[current_level]])

    # Draw the player
    screen.blit(player, player_pos)

    # Update display
    pygame.display.update()

    # Frame rate control
    pygame.time.Clock().tick(30)
