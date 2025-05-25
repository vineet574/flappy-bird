import pygame
import random
import time

pygame.init()

WIDTH, HEIGHT = 700, 1000
GRAVITY = 1
JUMP_STRENGTH = -20
PIPE_WIDTH = 70
PIPE_GAP = 150
PIPE_SPEED = 3
BIRD_RADIUS = 20
POWER_UP_TIME = 5

WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
BLUE = (135, 206, 250)
NIGHT_BLUE = (20, 24, 82)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

pygame.mixer.init()
jump_sound = pygame.mixer.Sound("jump.wav")
score_sound = pygame.mixer.Sound("score.wav")
power_up_sound = pygame.mixer.Sound("powerup.wav")
pygame.mixer.music.load("background_music.mp3")
pygame.mixer.music.play(-1)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()
start_time = time.time()
paused = False
muted = False
highest_score = 0

class Bird:
    def __init__(self):
        self.x = 50
        self.y = HEIGHT // 2
        self.velocity = 0
        self.invincible = False
        self.invincibility_timer = 0

    def update(self):
        if not self.invincible:
            self.velocity += GRAVITY
        self.y += self.velocity

    def jump(self):
        self.velocity = JUMP_STRENGTH
        if not muted:
            jump_sound.play()

    def draw(self, screen):
        pygame.draw.circle(screen, YELLOW if not self.invincible else RED, (self.x, int(self.y)), BIRD_RADIUS)

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
        if bird.invincible:
            return False
        if bird.x + BIRD_RADIUS > self.x and bird.x - BIRD_RADIUS < self.x + PIPE_WIDTH:
            if bird.y - BIRD_RADIUS < self.height or bird.y + BIRD_RADIUS > self.height + PIPE_GAP:
                return True
        return False

class PowerUp:
    def __init__(self):
        self.x = random.randint(100, WIDTH - 100)
        self.y = random.randint(100, HEIGHT - 100)
        self.active = True

    def draw(self, screen):
        if self.active:
            pygame.draw.circle(screen, RED, (self.x, self.y), 15)

    def check_collision(self, bird):
        if self.active and abs(bird.x - self.x) < 20 and abs(bird.y - self.y) < 20:
            self.active = False
            bird.invincible = True
            bird.invincibility_timer = POWER_UP_TIME * 30  # Convert seconds to frames
            if not muted:
                power_up_sound.play()

def get_background_color():
    elapsed = time.time() - start_time
    if elapsed < 30:
        return BLUE
    elif elapsed < 60:
        ratio = (elapsed - 30) / 30
        r = BLUE[0] + int((NIGHT_BLUE[0] - BLUE[0]) * ratio)
        g = BLUE[1] + int((NIGHT_BLUE[1] - BLUE[1]) * ratio)
        b = BLUE[2] + int((NIGHT_BLUE[2] - BLUE[2]) * ratio)
        return (r, g, b)
    else:
        return NIGHT_BLUE

def game_loop():
    global highest_score, paused, muted
    bird = Bird()
    pipes = [Pipe(WIDTH), Pipe(WIDTH + 200), Pipe(WIDTH + 400)]
    power_up = PowerUp()
    score = 0
    milestone_display = ""
    milestone_timer = 0
    font = pygame.font.Font(None, 36)

    try:
        with open("high_score.txt", "r") as file:
            highest_score = int(file.read())
    except:
        highest_score = 0

    running = True
    while running:
        screen.fill(get_background_color())
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.jump()
                elif event.key == pygame.K_p:
                    paused = not paused
                elif event.key == pygame.K_m:
                    muted = not muted
                    if muted:
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()

        if paused:
            pause_text = font.render("Paused! Press P to resume.", True, WHITE)
            screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2))
            pygame.display.update()
            continue

        bird.update()
        if bird.invincible:
            bird.invincibility_timer -= 1
            if bird.invincibility_timer <= 0:
                bird.invincible = False

        for pipe in pipes:
            pipe.update()
            if pipe.x == bird.x:
                score += 1
                if not muted:
                    score_sound.play()
                if score % 5 == 0:
                    milestone_display = f"Milestone reached! {score} points!"
                    milestone_timer = 60
            if pipe.check_collision(bird):
                running = False

        power_up.draw(screen)
        power_up.check_collision(bird)

        bird.draw(screen)
        for pipe in pipes:
            pipe.draw(screen)

        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        if milestone_timer > 0:
            milestone = font.render(milestone_display, True, RED)
            screen.blit(milestone, (WIDTH // 2 - milestone.get_width() // 2, 40))
            milestone_timer -= 1

        if bird.y + BIRD_RADIUS > HEIGHT or bird.y - BIRD_RADIUS < 0:
            running = False

        pygame.display.update()
        clock.tick(30)

    highest_score = max(highest_score, score)
    with open("high_score.txt", "w") as file:
        file.write(str(highest_score))

    game_over(score)

def game_over(score):
    font = pygame.font.Font(None, 48)
    while True:
        screen.fill(NIGHT_BLUE)

        game_over_text = font.render("Game Over", True, RED)
        score_text = font.render(f"Score: {score}", True, WHITE)
        high_score_text = font.render(f"High Score: {highest_score}", True, WHITE)
        restart_text = font.render("Press R to Restart or Q to Quit", True, WHITE)

        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 80))
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 - 20))
        screen.blit(high_score_text, (WIDTH // 2 - high_score_text.get_width() // 2, HEIGHT // 2 + 20))
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 60))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game_loop()
                    return
                elif event.key == pygame.K_q:
                    pygame.quit()
                    return

        pygame.display.update()

game_loop()
pygame.quit()
