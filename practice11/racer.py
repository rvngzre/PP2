import pygame
import random

pygame.init()

WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer")
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
GRAY = (80, 80, 80)
GREEN = (0, 180, 0)
RED = (220, 0, 0)
YELLOW = (255, 220, 0)
BLACK = (0, 0, 0)

font = pygame.font.SysFont("Arial", 28)
big_font = pygame.font.SysFont("Arial", 40)

player_width = 50
player_height = 90
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - player_height - 20
player_speed = 6

enemy_width = 50
enemy_height = 90
enemy_x = random.randint(60, WIDTH - 60 - enemy_width)
enemy_y = -enemy_height
enemy_speed = 5

coins = [
    {"radius": 10, "value": 1},
    {"radius": 12, "value": 2},
    {"radius": 14, "value": 3},
    {"radius": 16, "value": 4},
    {"radius": 18, "value": 5}
]

current_coin = random.choice(coins)
coin_radius = current_coin["radius"]
coin_value = current_coin["value"]

coin_x = random.randint(70, WIDTH - 70)
coin_y = random.randint(-500, -50)
coin_speed = 4

coins_collected = 0
game_over = False


def reset_enemy():
    global enemy_x, enemy_y

    enemy_x = random.randint(60, WIDTH - 60 - enemy_width)
    enemy_y = -enemy_height


def reset_coin():
    global coin_x, coin_y, coin_radius, coin_value

    current_coin = random.choice(coins)

    coin_radius = current_coin["radius"]
    coin_value = current_coin["value"]

    coin_x = random.randint(70, WIDTH - 70)
    coin_y = random.randint(-500, -50)


def restart_game():
    global player_x, player_y, coins_collected, enemy_speed, game_over

    player_x = WIDTH // 2 - player_width // 2
    player_y = HEIGHT - player_height - 20

    coins_collected = 0
    enemy_speed = 5

    reset_enemy()
    reset_coin()

    game_over = False


running = True

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and game_over:
                restart_game()

    if not game_over:
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and player_x > 60:
            player_x -= player_speed

        if keys[pygame.K_RIGHT] and player_x < WIDTH - 60 - player_width:
            player_x += player_speed

        enemy_y += enemy_speed
        coin_y += coin_speed

        if enemy_y > HEIGHT:
            reset_enemy()

        if coin_y > HEIGHT:
            reset_coin()

        player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
        enemy_rect = pygame.Rect(enemy_x, enemy_y, enemy_width, enemy_height)

        coin_rect = pygame.Rect(
            coin_x - coin_radius,
            coin_y - coin_radius,
            coin_radius * 2,
            coin_radius * 2
        )

        if player_rect.colliderect(enemy_rect):
            game_over = True

        if player_rect.colliderect(coin_rect):
            old_level = coins_collected // 10

            coins_collected += coin_value

            new_level = coins_collected // 10

            if new_level > old_level:
                enemy_speed += 1

            reset_coin()

    screen.fill(GREEN)

    pygame.draw.rect(screen, GRAY, (50, 0, WIDTH - 100, HEIGHT))

    for y in range(0, HEIGHT, 80):
        pygame.draw.rect(screen, WHITE, (WIDTH // 2 - 5, y, 10, 40))

    pygame.draw.rect(screen, RED, (player_x, player_y, player_width, player_height))
    pygame.draw.rect(screen, BLACK, (enemy_x, enemy_y, enemy_width, enemy_height))

    pygame.draw.circle(screen, YELLOW, (coin_x, coin_y), coin_radius)

    value_text = font.render(str(coin_value), True, BLACK)
    value_rect = value_text.get_rect(center=(coin_x, coin_y))
    screen.blit(value_text, value_rect)

    coin_text = font.render(f"Points: {coins_collected}", True, WHITE)
    screen.blit(coin_text, (WIDTH - 170, 10))

    speed_text = font.render(f"Speed: {enemy_speed}", True, WHITE)
    screen.blit(speed_text, (10, 10))

    if game_over:
        overlay = pygame.Surface((260, 140), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        overlay_rect = overlay.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(overlay, overlay_rect)

        game_text = big_font.render("GAME OVER", True, RED)
        game_rect = game_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20))
        screen.blit(game_text, game_rect)

        restart_text = font.render("Press R to restart", True, WHITE)
        restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 30))
        screen.blit(restart_text, restart_rect)

    pygame.display.update()

pygame.quit()