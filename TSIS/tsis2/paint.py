import pygame
from tools import (
    get_rect_from_points,
    draw_right_triangle,
    draw_equilateral_triangle,
    draw_rhombus,
    flood_fill,
    save_canvas
)

pygame.init()

WIDTH, HEIGHT = 1200, 700
TOOLBAR_HEIGHT = 90

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint TSIS2")
clock = pygame.time.Clock()

font = pygame.font.SysFont("Arial", 18)
text_font = pygame.font.SysFont("Arial", 28)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

colors = [
    (0, 0, 0),
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (255, 255, 0),
    (255, 165, 0),
    (128, 0, 128)
]

current_color = BLACK
tool = "pencil"
brush_size = 5

screen.fill(WHITE)
canvas = screen.copy()

text_input = ""
text_position = None
typing = False

running = True
drawing = False
start_pos = None

tools = [
    "pencil",
    "line",
    "rect",
    "circle",
    "eraser",
    "fill",
    "text",
    "square",
    "right_tri",
    "eq_tri",
    "rhombus"
]

shape_tools = [
    "line",
    "rect",
    "circle",
    "square",
    "right_tri",
    "eq_tri",
    "rhombus"
]


def draw_selected_shape(surface, pos):
    if tool == "line":
        pygame.draw.line(surface, current_color, start_pos, pos, brush_size)

    elif tool == "rect":
        pygame.draw.rect(
            surface,
            current_color,
            get_rect_from_points(start_pos, pos),
            brush_size
        )

    elif tool == "circle":
        radius = int(
            (
                (pos[0] - start_pos[0]) ** 2 +
                (pos[1] - start_pos[1]) ** 2
            ) ** 0.5
        )
        pygame.draw.circle(surface, current_color, start_pos, radius, brush_size)

    elif tool == "square":
        size = max(abs(pos[0] - start_pos[0]), abs(pos[1] - start_pos[1]))
        x = start_pos[0] if pos[0] >= start_pos[0] else start_pos[0] - size
        y = start_pos[1] if pos[1] >= start_pos[1] else start_pos[1] - size
        pygame.draw.rect(surface, current_color, (x, y, size, size), brush_size)

    elif tool == "right_tri":
        draw_right_triangle(surface, current_color, start_pos, pos, brush_size)

    elif tool == "eq_tri":
        draw_equilateral_triangle(surface, current_color, start_pos, pos, brush_size)

    elif tool == "rhombus":
        draw_rhombus(surface, current_color, start_pos, pos, brush_size)


def draw_toolbar():
    pygame.draw.rect(screen, (220, 220, 220), (0, 0, WIDTH, TOOLBAR_HEIGHT))

    x = 10

    for item in tools:
        rect = pygame.Rect(x, 10, 95, 35)
        button_color = (160, 160, 160) if tool == item else (180, 180, 180)

        pygame.draw.rect(screen, button_color, rect)
        pygame.draw.rect(screen, BLACK, rect, 2)

        text = font.render(item, True, BLACK)
        text_rect = text.get_rect(center=rect.center)
        screen.blit(text, text_rect)

        x += 100

    size_text = font.render(f"Size: {brush_size}  Press 1/2/3", True, BLACK)
    screen.blit(size_text, (10, 55))

    save_text = font.render("Ctrl+S save", True, BLACK)
    screen.blit(save_text, (140, 55))

    cx = 270

    for color in colors:
        pygame.draw.rect(screen, color, (cx, 55, 35, 25))
        pygame.draw.rect(screen, BLACK, (cx, 55, 35, 25), 2)
        cx += 45


def select_toolbar(pos):
    global tool
    global current_color

    x, y = pos

    if 10 <= y <= 45:
        button_x = 10

        for item in tools:
            if button_x <= x <= button_x + 95:
                tool = item
            button_x += 100

    cx = 270

    for color in colors:
        if cx <= x <= cx + 35 and 55 <= y <= 80:
            current_color = color
        cx += 45


while running:
    clock.tick(60)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_1:
                brush_size = 2

            elif event.key == pygame.K_2:
                brush_size = 5

            elif event.key == pygame.K_3:
                brush_size = 10

            elif event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                filename = save_canvas(screen)
                print("Saved:", filename)

            elif typing:

                if event.key == pygame.K_RETURN:
                    rendered = text_font.render(text_input, True, current_color)
                    screen.blit(rendered, text_position)
                    canvas = screen.copy()
                    text_input = ""
                    typing = False

                elif event.key == pygame.K_ESCAPE:
                    screen.blit(canvas, (0, 0))
                    text_input = ""
                    typing = False

                elif event.key == pygame.K_BACKSPACE:
                    text_input = text_input[:-1]

                else:
                    text_input += event.unicode

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()

            if pos[1] <= TOOLBAR_HEIGHT:
                select_toolbar(pos)

            else:
                if tool == "fill":
                    flood_fill(
                        screen,
                        pos[0],
                        pos[1],
                        current_color,
                        TOOLBAR_HEIGHT,
                        WIDTH,
                        HEIGHT
                    )
                    canvas = screen.copy()

                elif tool == "text":
                    typing = True
                    text_position = pos
                    text_input = ""
                    canvas = screen.copy()

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

            if pos[1] > TOOLBAR_HEIGHT:

                if tool == "pencil":
                    if start_pos:
                        pygame.draw.line(
                            screen,
                            current_color,
                            start_pos,
                            pos,
                            brush_size
                        )

                    start_pos = pos
                    canvas = screen.copy()

                elif tool == "eraser":
                    if start_pos:
                        pygame.draw.line(
                            screen,
                            WHITE,
                            start_pos,
                            pos,
                            brush_size * 2
                        )

                    start_pos = pos
                    canvas = screen.copy()

                elif tool in shape_tools:
                    screen.blit(canvas, (0, 0))
                    draw_selected_shape(screen, pos)

    if typing:
        screen.blit(canvas, (0, 0))
        preview = text_font.render(text_input, True, current_color)
        screen.blit(preview, text_position)

    draw_toolbar()
    pygame.display.update()

pygame.quit()
