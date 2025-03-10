import pygame
import random

# Initialize Pygame
pygame.init()

# Game Constants
WIDTH, HEIGHT = 500, 800
GRAVITY = 1
JUMP_STRENGTH = -10
PIPE_WIDTH = 70
PIPE_GAP = 150
PIPE_SPEED = 3
BIRD_RADIUS = 15

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
BLUE = (135, 206, 250)
YELLOW = (255, 255, 0)

# Create Game Window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Clock for FPS Control
clock = pygame.time.Clock()

# Bird Class
class Bird:
    def __init__(self):
        self.x = 50
        self.y = HEIGHT // 2
        self.velocity = 0

    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity

    def jump(self):
        self.velocity = JUMP_STRENGTH

    def draw(self, screen):
        pygame.draw.circle(screen, YELLOW, (self.x, int(self.y)), BIRD_RADIUS)

# Pipe Class
class Pipe:
    def __init__(self, x):
        self.x = x
        self.height = random.randint(100, 400)

    def update(self):
        self.x -= PIPE_SPEED
        if self.x + PIPE_WIDTH < 0:
            self.x = WIDTH
            self.height = random.randint(100, 400)

    def draw(self, screen):
        # Draw top pipe
        pygame.draw.rect(screen, GREEN, (self.x, 0, PIPE_WIDTH, self.height))
        # Draw bottom pipe
        pygame.draw.rect(screen, GREEN, (self.x, self.height + PIPE_GAP, PIPE_WIDTH, HEIGHT - self.height - PIPE_GAP))

    def check_collision(self, bird):
        if (bird.x + BIRD_RADIUS > self.x and bird.x - BIRD_RADIUS < self.x + PIPE_WIDTH):
            if bird.y - BIRD_RADIUS < self.height or bird.y + BIRD_RADIUS > self.height + PIPE_GAP:
                return True
        return False

# Game Loop
def game_loop():
    bird = Bird()
    pipes = [Pipe(WIDTH), Pipe(WIDTH + 200), Pipe(WIDTH + 400)]
    running = True
    score = 0
    font = pygame.font.Font(None, 36)

    while running:
        screen.fill(BLUE)

        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.jump()

        # Update Bird
        bird.update()

        # Update Pipes
        for pipe in pipes:
            pipe.update()
            if pipe.x == bird.x:
                score += 1
            if pipe.check_collision(bird):
                running = False

        # Draw Everything
        bird.draw(screen)
        for pipe in pipes:
            pipe.draw(screen)

        # Display Score
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        # Check if Bird Hits the Ground or Ceiling
        if bird.y + BIRD_RADIUS > HEIGHT or bird.y - BIRD_RADIUS < 0:
            running = False

        pygame.display.update()
        clock.tick(30)

# Run the Game
game_loop()
pygame.quit()
