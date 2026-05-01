import pygame
import math

pygame.init()

WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 18)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

colors = [
    (0, 0, 0), (255, 0, 0), (0, 255, 0),
    (0, 0, 255), (255, 255, 0), (255, 165, 0),
    (128, 0, 128)
]

current_color = BLACK
tool = "brush"

screen.fill(WHITE)
canvas = screen.copy()


def get_rect_from_points(start, end):
    return pygame.Rect(
        min(start[0], end[0]),
        min(start[1], end[1]),
        abs(end[0] - start[0]),
        abs(end[1] - start[1])
    )


def draw_right_triangle(surface, color, start, end):
    points = [
        start,
        (start[0], end[1]),
        end
    ]
    pygame.draw.polygon(surface, color, points, 3)


def draw_equilateral_triangle(surface, color, start, end):
    side = max(abs(end[0] - start[0]), abs(end[1] - start[1]))
    height = int(side * math.sqrt(3) / 2)

    points = [
        (start[0], start[1] - height // 2),
        (start[0] - side // 2, start[1] + height // 2),
        (start[0] + side // 2, start[1] + height // 2)
    ]
    pygame.draw.polygon(surface, color, points, 3)


def draw_rhombus(surface, color, start, end):
    width = abs(end[0] - start[0])
    height = abs(end[1] - start[1])

    points = [
        (start[0], start[1] - height // 2),
        (start[0] + width // 2, start[1]),
        (start[0], start[1] + height // 2),
        (start[0] - width // 2, start[1])
    ]
    pygame.draw.polygon(surface, color, points, 3)


def draw_selected_shape(surface, pos):
    if tool == "rect":
        pygame.draw.rect(surface, current_color, get_rect_from_points(start_pos, pos), 3)

    elif tool == "circle":
        radius = int(((pos[0] - start_pos[0]) ** 2 +
                      (pos[1] - start_pos[1]) ** 2) ** 0.5)
        pygame.draw.circle(surface, current_color, start_pos, radius, 3)

    elif tool == "square":
        size = max(abs(pos[0] - start_pos[0]), abs(pos[1] - start_pos[1]))
        x = start_pos[0] if pos[0] >= start_pos[0] else start_pos[0] - size
        y = start_pos[1] if pos[1] >= start_pos[1] else start_pos[1] - size
        pygame.draw.rect(surface, current_color, (x, y, size, size), 3)

    elif tool == "right_tri":
        draw_right_triangle(surface, current_color, start_pos, pos)

    elif tool == "eq_tri":
        draw_equilateral_triangle(surface, current_color, start_pos, pos)

    elif tool == "rhombus":
        draw_rhombus(surface, current_color, start_pos, pos)


def draw_toolbar():
    pygame.draw.rect(screen, (220, 220, 220), (0, 0, WIDTH, 90))

    tools = ["brush", "rect", "circle", "eraser", "square", "right_tri", "eq_tri", "rhombus"]
    x = 10

    for t in tools:
        rect = pygame.Rect(x, 15, 95, 40)
        button_color = (160, 160, 160) if tool == t else (180, 180, 180)
        pygame.draw.rect(screen, button_color, rect)
        pygame.draw.rect(screen, BLACK, rect, 2)

        text = font.render(t, True, BLACK)
        text_rect = text.get_rect(center=rect.center)
        screen.blit(text, text_rect)
        x += 105

    cx = 10
    for c in colors:
        pygame.draw.rect(screen, c, (cx, 62, 35, 22))
        pygame.draw.rect(screen, BLACK, (cx, 62, 35, 22), 2)
        cx += 45


def select_toolbar(pos):
    global tool, current_color

    x, y = pos
    tools = ["brush", "rect", "circle", "eraser", "square", "right_tri", "eq_tri", "rhombus"]

    if 15 <= y <= 55:
        button_x = 10
        for t in tools:
            if button_x <= x <= button_x + 95:
                tool = t
            button_x += 105

    cx = 10
    for c in colors:
        if cx <= x <= cx + 35 and 62 <= y <= 84:
            current_color = c
        cx += 45


running = True
drawing = False
start_pos = None
shape_tools = ["rect", "circle", "square", "right_tri", "eq_tri", "rhombus"]

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()

            if pos[1] <= 90:
                select_toolbar(pos)
            else:
                drawing = True
                start_pos = pos
                canvas = screen.copy()

        if event.type == pygame.MOUSEBUTTONUP:
            if drawing and start_pos:
                end = pygame.mouse.get_pos()

                if tool in shape_tools:
                    draw_selected_shape(screen, end)

            drawing = False
            start_pos = None
            canvas = screen.copy()

        if event.type == pygame.MOUSEMOTION and drawing:
            pos = pygame.mouse.get_pos()

            if pos[1] > 90:
                if tool == "brush":
                    if start_pos:
                        pygame.draw.line(screen, current_color, start_pos, pos, 10)
                    start_pos = pos
                    canvas = screen.copy()

                elif tool == "eraser":
                    if start_pos:
                        pygame.draw.line(screen, WHITE, start_pos, pos, 20)
                    start_pos = pos
                    canvas = screen.copy()

                elif tool in shape_tools:
                    screen.blit(canvas, (0, 0))
                    draw_selected_shape(screen, pos)

    draw_toolbar()
    pygame.display.update()

pygame.quit()
