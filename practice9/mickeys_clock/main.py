import pygame
import sys
from clock import get_angles, get_hand_position

pygame.init()

WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

background = pygame.image.load("images/mickeyclock.jpeg")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

center = (WIDTH // 2, HEIGHT // 2)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.blit(background, (0, 0))

    sec_angle, min_angle = get_angles()

    pygame.draw.line(screen, (255, 0, 0), center,
                     get_hand_position(center, 250, sec_angle), 4)

    pygame.draw.line(screen, (0, 0, 0), center,
                     get_hand_position(center, 200, min_angle), 6)

    pygame.display.flip()
    clock.tick(1)