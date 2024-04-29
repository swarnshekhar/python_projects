import pygame
import random

# Initialize Pygame
pygame.init()

# Set up display
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
CELL_SIZE = 20
GRID_WIDTH, GRID_HEIGHT = SCREEN_WIDTH // CELL_SIZE, SCREEN_HEIGHT // CELL_SIZE
FPS = 10
FONT_SIZE = 24
SCORE_FONT = pygame.font.Font(None, FONT_SIZE)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 200)

# Direction vectors
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Snake class
class Snake:
    def __init__(self):
        self.length = 1
        self.positions = [((GRID_WIDTH // 2) * CELL_SIZE, (GRID_HEIGHT // 2) * CELL_SIZE)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = GREEN

    def get_head_position(self):
        return self.positions[0]

    def turn(self, point):
        if self.length > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return
        else:
            self.direction = point

    def move(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = (((cur[0] + (x * CELL_SIZE)) % SCREEN_WIDTH), (cur[1] + (y * CELL_SIZE)) % SCREEN_HEIGHT)
        if len(self.positions) > 2 and new in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()

    def reset(self):
        self.length = 1
        self.positions = [((GRID_WIDTH // 2) * CELL_SIZE, (GRID_HEIGHT // 2) * CELL_SIZE)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])

    def draw(self, surface):
        for p in self.positions:
            r = pygame.Rect((p[0], p[1]), (CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(surface, self.color, r)
            pygame.draw.rect(surface, BLACK, r, 1)

# Apple class
class Apple:
    def __init__(self):
        self.position = (0, 0)
        self.color = RED
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, GRID_WIDTH - 1) * CELL_SIZE, random.randint(0, GRID_HEIGHT - 1) * CELL_SIZE)

    def draw(self, surface):
        r = pygame.Rect((self.position[0], self.position[1]), (CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(surface, self.color, r)
        pygame.draw.rect(surface, BLACK, r, 1)

# Main function
def main():
    # Set up display
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Snaky Game')

    # Set up clock
    clock = pygame.time.Clock()

    # Initialize snake and apple
    snake = Snake()
    apple = Apple()

    # Main loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.turn(UP)
                elif event.key == pygame.K_DOWN:
                    snake.turn(DOWN)
                elif event.key == pygame.K_LEFT:
                    snake.turn(LEFT)
                elif event.key == pygame.K_RIGHT:
                    snake.turn(RIGHT)

        # Move snake
        snake.move()

        # Check for collision with apple
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()

        # Draw everything
        screen.fill(WHITE)
        snake.draw(screen)
        apple.draw(screen)
        
        # Display score
        score_text = SCORE_FONT.render(f"Score: {snake.length - 1}", True, BLUE)
        screen.blit(score_text, (10, 10))

        pygame.display.update()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
