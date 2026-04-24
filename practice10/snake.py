import pygame
import random

pygame.init()

WIDTH, HEIGHT = 600, 400
CELL = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 180, 0)
RED = (220, 0, 0)

font = pygame.font.SysFont("Arial", 26)

snake = [(WIDTH // 2, HEIGHT // 2)]
direction = (CELL, 0)

score = 0
level = 1
move_delay = 150
last_move = pygame.time.get_ticks()
food = None
game_over = False


def generate_food():
    while True:
        x = random.randrange(0, WIDTH, CELL)
        y = random.randrange(0, HEIGHT, CELL)
        if (x, y) not in snake:
            return (x, y)


def restart_game():
    global snake, direction, score, level, move_delay, last_move, food, game_over

    snake = [(WIDTH // 2, HEIGHT // 2)]
    direction = (CELL, 0)
    score = 0
    level = 1
    move_delay = 150
    last_move = pygame.time.get_ticks()
    food = generate_food()
    game_over = False


food = generate_food()

running = True
while running:
    clock.tick(120)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if not game_over:
                if event.key == pygame.K_UP and direction != (0, CELL):
                    direction = (0, -CELL)
                elif event.key == pygame.K_DOWN and direction != (0, -CELL):
                    direction = (0, CELL)
                elif event.key == pygame.K_LEFT and direction != (CELL, 0):
                    direction = (-CELL, 0)
                elif event.key == pygame.K_RIGHT and direction != (-CELL, 0):
                    direction = (CELL, 0)
            else:
                if event.key == pygame.K_r:
                    restart_game()

    now = pygame.time.get_ticks()

    if not game_over and now - last_move > move_delay:
        last_move = now

        head = (snake[0][0] + direction[0], snake[0][1] + direction[1])

        if (head[0] < 0 or head[0] >= WIDTH or
            head[1] < 0 or head[1] >= HEIGHT or
            head in snake):
            game_over = True
        else:
            snake.insert(0, head)

            if head == food:
                score += 1
                food = generate_food()

                if score % 4 == 0:
                    level += 1
                    move_delay = max(60, move_delay - 10)
            else:
                snake.pop()

    screen.fill(WHITE)

    for part in snake:
        pygame.draw.rect(screen, GREEN, (part[0], part[1], CELL, CELL))

    pygame.draw.rect(screen, RED, (food[0], food[1], CELL, CELL))

    score_text = font.render(f"Score: {score}", True, BLACK)
    level_text = font.render(f"Level: {level}", True, BLACK)

    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10, 40))

    if game_over:
        overlay = pygame.Surface((300, 150), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        overlay_rect = overlay.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(overlay, overlay_rect)

        game_text = font.render("GAME OVER", True, RED)
        game_rect = game_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20))
        screen.blit(game_text, game_rect)

        restart_text = font.render("Press R to restart", True, WHITE)
        restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 25))
        screen.blit(restart_text, restart_rect)

    pygame.display.update()

pygame.quit()