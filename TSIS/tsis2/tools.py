import pygame
import math
from collections import deque
from datetime import datetime


def get_rect_from_points(start, end):
    return pygame.Rect(
        min(start[0], end[0]),
        min(start[1], end[1]),
        abs(end[0] - start[0]),
        abs(end[1] - start[1])
    )


def draw_right_triangle(surface, color, start, end, size):
    points = [
        start,
        (start[0], end[1]),
        end
    ]
    pygame.draw.polygon(surface, color, points, size)


def draw_equilateral_triangle(surface, color, start, end, size):
    side = max(abs(end[0] - start[0]), abs(end[1] - start[1]))
    height = int(side * math.sqrt(3) / 2)

    points = [
        (start[0], start[1] - height // 2),
        (start[0] - side // 2, start[1] + height // 2),
        (start[0] + side // 2, start[1] + height // 2)
    ]

    pygame.draw.polygon(surface, color, points, size)


def draw_rhombus(surface, color, start, end, size):
    width = abs(end[0] - start[0])
    height = abs(end[1] - start[1])

    points = [
        (start[0], start[1] - height // 2),
        (start[0] + width // 2, start[1]),
        (start[0], start[1] + height // 2),
        (start[0] - width // 2, start[1])
    ]

    pygame.draw.polygon(surface, color, points, size)


def flood_fill(surface, x, y, new_color, top_limit, width, height):
    target_color = surface.get_at((x, y))

    if target_color == new_color:
        return

    queue = deque()
    queue.append((x, y))

    while queue:
        px, py = queue.popleft()

        if px < 0 or px >= width or py < top_limit or py >= height:
            continue

        if surface.get_at((px, py)) != target_color:
            continue

        surface.set_at((px, py), new_color)

        queue.append((px + 1, py))
        queue.append((px - 1, py))
        queue.append((px, py + 1))
        queue.append((px, py - 1))


def save_canvas(surface):
    filename = datetime.now().strftime("paint_%Y%m%d_%H%M%S.png")
    pygame.image.save(surface, filename)
    return filename
