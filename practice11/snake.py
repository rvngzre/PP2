import pygame
import random

pygame.init()

WIDTH, HEIGHT = 600, 400
CELL = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Practice 11")
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 180, 0)
RED = (220, 0, 0)

font = pygame.font.SysFont("Arial", 26)
small_font = pygame.font.SysFont("Arial", 20)

snake = [(WIDTH // 2, HEIGHT // 2)]
direction = (CELL, 0)

score = 0
level = 1
move_delay = 150
last_move = pygame.time.get_ticks()

food_types = [
    {"value": 1},
    {"value": 2},
    {"value": 3},
    {"value": 4},
    {"value": 5}
]

food = None
food_value = 1
food_spawn_time = pygame.time.get_ticks()
FOOD_LIFETIME = 5000

game_over = False


def generate_food():
    global food_value, food_spawn_time

    while True:
        x = random.randrange(0, WIDTH, CELL)
        y = random.randrange(0, HEIGHT, CELL)

        if (x, y) not in snake:
            selected_food = random.choice(food_types)

            food_value = selected_food["value"]
            food_spawn_time = pygame.time.get_ticks()

            return (x, y)


def restart_game():
    global snake
    global direction
    global score
    global level
    global move_delay
    global last_move
    global food
    global game_over

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

    if not game_over and now - food_spawn_time > FOOD_LIFETIME:
        food = generate_food()

    if not game_over and now - last_move > move_delay:

        last_move = now

        head = (
            snake[0][0] + direction[0],
            snake[0][1] + direction[1]
        )

        if (
            head[0] < 0 or
            head[0] >= WIDTH or
            head[1] < 0 or
            head[1] >= HEIGHT or
            head in snake
        ):
            game_over = True

        else:
            snake.insert(0, head)

            if head == food:

                score += food_value

                food = generate_food()

                if score // 4 + 1 > level:
                    level += 1
                    move_delay = max(60, move_delay - 10)

            else:
                snake.pop()

    screen.fill(WHITE)

    for part in snake:
        pygame.draw.rect(
            screen,
            GREEN,
            (part[0], part[1], CELL, CELL)
        )

    pygame.draw.rect(
        screen,
        RED,
        (food[0], food[1], CELL, CELL)
    )

    value_text = small_font.render(
        str(food_value),
        True,
        WHITE
    )

    value_rect = value_text.get_rect(
        center=(food[0] + CELL // 2, food[1] + CELL // 2)
    )

    screen.blit(value_text, value_rect)

    time_left = max(
        0,
        (FOOD_LIFETIME - (now - food_spawn_time)) // 1000 + 1
    )

    score_text = font.render(
        f"Score: {score}",
        True,
        BLACK
    )

    level_text = font.render(
        f"Level: {level}",
        True,
        BLACK
    )

    timer_text = font.render(
        f"Food time: {time_left}",
        True,
        BLACK
    )

    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10, 40))
    screen.blit(timer_text, (10, 70))

    if game_over:

        overlay = pygame.Surface((300, 150), pygame.SRCALPHA)

        overlay.fill((0, 0, 0, 180))

        overlay_rect = overlay.get_rect(
            center=(WIDTH // 2, HEIGHT // 2)
        )

        screen.blit(overlay, overlay_rect)

        game_text = font.render(
            "GAME OVER",
            True,
            RED
        )

        game_rect = game_text.get_rect(
            center=(WIDTH // 2, HEIGHT // 2 - 20)
        )

        screen.blit(game_text, game_rect)

        restart_text = font.render(
            "Press R to restart",
            True,
            WHITE
        )

        restart_rect = restart_text.get_rect(
            center=(WIDTH // 2, HEIGHT // 2 + 25)
        )

        screen.blit(restart_text, restart_rect)

    pygame.display.update()

pygame.quit()