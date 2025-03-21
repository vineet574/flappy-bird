import pygame
import random

pygame.init()

WIDTH, HEIGHT = 500, 800
GRAVITY = 1
JUMP_STRENGTH = -10
PIPE_WIDTH = 70
PIPE_GAP = 150
PIPE_SPEED = 3
BIRD_RADIUS = 15

WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
BLUE = (135, 206, 250)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

jump_sound = pygame.mixer.Sound("jump.wav")
score_sound = pygame.mixer.Sound("score.wav")

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

clock = pygame.time.Clock()

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
        jump_sound.play()

    def draw(self, screen):
        pygame.draw.circle(screen, YELLOW, (self.x, int(self.y)), BIRD_RADIUS)

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
        pygame.draw.rect(screen, GREEN, (self.x, 0, PIPE_WIDTH, self.height))
        pygame.draw.rect(screen, GREEN, (self.x, self.height + PIPE_GAP, PIPE_WIDTH, HEIGHT - self.height - PIPE_GAP))

    def check_collision(self, bird):
        if (bird.x + BIRD_RADIUS > self.x and bird.x - BIRD_RADIUS < self.x + PIPE_WIDTH):
            if bird.y - BIRD_RADIUS < self.height or bird.y + BIRD_RADIUS > self.height + PIPE_GAP:
                return True
        return False

def game_loop():
    bird = Bird()
    pipes = [Pipe(WIDTH), Pipe(WIDTH + 200), Pipe(WIDTH + 400)]
    running = True
    score = 0
    font = pygame.font.Font(None, 36)

    while running:
        screen.fill(BLUE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.jump()

        bird.update()

        for pipe in pipes:
            pipe.update()
            if pipe.x == bird.x:
                score += 1
                score_sound.play()
            if pipe.check_collision(bird):
                running = False

        bird.draw(screen)
        for pipe in pipes:
            pipe.draw(screen)

        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        if bird.y + BIRD_RADIUS > HEIGHT or bird.y - BIRD_RADIUS < 0:
            running = False

        pygame.display.update()
        clock.tick(30)

    game_over(score)

def game_over(score):
    font = pygame.font.Font(None, 48)
    while True:
        screen.fill(BLUE)
        
        game_over_text = font.render("Game Over", True, RED)
        score_text = font.render(f"Score: {score}", True, WHITE)
        
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2 - 20))
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 + score_text.get_height() // 2))

        restart_text = font.render("Press R to Restart or Q to Quit", True, WHITE)
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + restart_text.get_height() // 2 + 20))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game_loop()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    return
        
        pygame.display.update()

game_loop()
pygame.quit()
