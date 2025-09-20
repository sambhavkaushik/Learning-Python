import pygame
import random
import sys

# -----------------------------
# Simple Flappy Bird (no assets)
# -----------------------------
# Controls: SPACE or UP to flap
# Press SPACE to restart after game over

WIDTH, HEIGHT = 400, 600
FPS = 60

PIPE_GAP = 160          # gap between top & bottom pipes
PIPE_SPEED = 3          # pipe move speed
PIPE_SPAWN_EVERY = 1500 # ms
BIRD_X = 80
GRAVITY = 0.35
FLAP_STRENGTH = -7.5
MAX_FALL_SPEED = 10

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SKY = (135, 206, 235)
GREEN = (60, 179, 113)
DARKGREEN = (34, 139, 34)
YELLOW = (255, 215, 0)
RED = (220, 20, 60)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy (pygame)")
clock = pygame.time.Clock()
font_big = pygame.font.SysFont(None, 64)
font_med = pygame.font.SysFont(None, 36)
font_small = pygame.font.SysFont(None, 24)

class Bird:
    def __init__(self):
        self.reset()

    def reset(self):
        self.x = BIRD_X
        self.y = HEIGHT // 2
        self.r = 16
        self.vel = 0
        self.alive = True
        self.rotation = 0

    def update(self):
        self.vel = min(self.vel + GRAVITY, MAX_FALL_SPEED)
        self.y += self.vel
        # rotate a bit based on velocity (just for feel)
        self.rotation = max(min(-self.vel * 3, 25), -45)

        # hit floor/ceiling
        if self.y + self.r >= HEIGHT - 60:  # ground height ~60
            self.y = HEIGHT - 60 - self.r
            self.alive = False
        if self.y - self.r <= 0:
            self.y = self.r
            self.vel = 0  # bounce off ceiling a bit

    def flap(self):
        if self.alive:
            self.vel = FLAP_STRENGTH

    def draw(self, surf):
        # Draw a simple circle bird + small triangle beak
        pygame.draw.circle(surf, YELLOW, (int(self.x), int(self.y)), self.r)
        # Beak
        beak_len = 10
        points = [
            (self.x + self.r, self.y),
            (self.x + self.r + beak_len, self.y - 4),
            (self.x + self.r + beak_len, self.y + 4),
        ]
        pygame.draw.polygon(surf, RED, points)
        # Eye
        pygame.draw.circle(surf, BLACK, (int(self.x + 6), int(self.y - 6)), 3)

    def rect(self):
        return pygame.Rect(self.x - self.r, self.y - self.r, self.r * 2, self.r * 2)

class Pipe:
    def __init__(self, x):
        self.x = x
        self.width = 60
        self.passed = False
        self._randomize_gap()

    def _randomize_gap(self):
        # ensure the gap stays within screen
        top_height = random.randint(50, HEIGHT - 60 - PIPE_GAP - 50)
        self.top_rect = pygame.Rect(self.x, 0, self.width, top_height)
        self.bot_rect = pygame.Rect(self.x, top_height + PIPE_GAP, self.width, HEIGHT - 60 - (top_height + PIPE_GAP))

    def update(self):
        self.x -= PIPE_SPEED
        self.top_rect.x = self.x
        self.bot_rect.x = self.x

    def draw(self, surf):
        pygame.draw.rect(surf, DARKGREEN, self.top_rect)
        pygame.draw.rect(surf, GREEN, self.bot_rect)

    def offscreen(self):
        return self.x + self.width < 0

def draw_ground(surf, t):
    # simple moving ground stripes
    ground_y = HEIGHT - 60
    pygame.draw.rect(surf, (222, 184, 135), (0, ground_y, WIDTH, 60))
    # stripes
    offset = int((t * PIPE_SPEED) % 40)
    for x in range(-offset, WIDTH, 40):
        pygame.draw.rect(surf, (210, 180, 140), (x, ground_y + 40, 20, 8))

def collide(bird: Bird, pipe: Pipe):
    # Circle-rect collision simplified by using bird's rect
    b = bird.rect()
    return b.colliderect(pipe.top_rect) or b.colliderect(pipe.bot_rect)

def main():
    bird = Bird()
    pipes = []
    score = 0
    high_score = 0
    running = True
    last_spawn = pygame.time.get_ticks()
    time_alive = 0
    started = False

    while running:
        dt = clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_SPACE, pygame.K_UP):
                    if not started:
                        started = True
                    if bird.alive:
                        bird.flap()
                    else:
                        # restart
                        bird = Bird()
                        pipes = []
                        score = 0
                        last_spawn = pygame.time.get_ticks()
                        started = False

        # Spawn pipes
        now = pygame.time.get_ticks()
        if started and bird.alive and (now - last_spawn) >= PIPE_SPAWN_EVERY:
            last_spawn = now
            spawn_x = WIDTH + 20
            pipes.append(Pipe(spawn_x))

        # Update
        if started and bird.alive:
            bird.update()
            for p in pipes:
                p.update()

        # Scoring & cleanup
        for p in list(pipes):
            if not p.passed and p.x + p.width < bird.x:
                p.passed = True
                score += 1
            if p.offscreen():
                pipes.remove(p)

        # Collision
        if bird.alive:
            for p in pipes:
                if collide(bird, p):
                    bird.alive = False
                    break

        high_score = max(high_score, score)
        time_alive += dt if started else 0

        # Draw
        screen.fill(SKY)
        # Title / tips
        if not started and bird.alive:
            title = font_big.render("Flappy", True, BLACK)
            tip = font_med.render("Press SPACE to start", True, BLACK)
            screen.blit(title, (WIDTH//2 - title.get_width()//2, 120))
            screen.blit(tip, (WIDTH//2 - tip.get_width()//2, 190))

        # Pipes & Bird
        for p in pipes:
            p.draw(screen)
        bird.draw(screen)

        # Ground
        draw_ground(screen, pygame.time.get_ticks()/16)

        # Score
        score_surf = font_big.render(str(score), True, BLACK)
        screen.blit(score_surf, (WIDTH//2 - score_surf.get_width()//2, 20))

        # Game over overlay
        if not bird.alive:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 120))
            screen.blit(overlay, (0, 0))

            go = font_big.render("Game Over", True, WHITE)
            s = font_med.render(f"Score: {score}   Best: {high_score}", True, WHITE)
            r = font_med.render("Press SPACE to restart", True, WHITE)
            screen.blit(go, (WIDTH//2 - go.get_width()//2, HEIGHT//2 - 80))
            screen.blit(s, (WIDTH//2 - s.get_width()//2, HEIGHT//2 - 20))
            screen.blit(r, (WIDTH//2 - r.get_width()//2, HEIGHT//2 + 30))

        # Tiny footer
        footer = font_small.render("SPACE/UP to flap • ESC to close window", True, BLACK)
        screen.blit(footer, (10, HEIGHT - 55))

        pygame.display.flip()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        pygame.quit()
        raise e
