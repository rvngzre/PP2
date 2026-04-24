import pygame

pygame.init()

WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 22)

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

def draw_toolbar():
    pygame.draw.rect(screen, (220, 220, 220), (0, 0, WIDTH, 80))

    tools = ["brush", "rect", "circle", "eraser"]
    x = 10

    for t in tools:
        rect = pygame.Rect(x, 15, 90, 40)
        pygame.draw.rect(screen, (180, 180, 180), rect)
        pygame.draw.rect(screen, BLACK, rect, 2)

        text = font.render(t, True, BLACK)
        text_rect = text.get_rect(center=rect.center)
        screen.blit(text, text_rect)

        x += 100

    cx = 430
    for c in colors:
        pygame.draw.rect(screen, c, (cx, 20, 35, 35))
        pygame.draw.rect(screen, BLACK, (cx, 20, 35, 35), 2)
        cx += 45


def select_toolbar(pos):
    global tool, current_color

    x, y = pos

    if 15 <= y <= 55:
        if 10 <= x <= 100:
            tool = "brush"
        elif 110 <= x <= 200:
            tool = "rect"
        elif 210 <= x <= 300:
            tool = "circle"
        elif 310 <= x <= 400:
            tool = "eraser"

    cx = 430
    for c in colors:
        if cx <= x <= cx + 35 and 20 <= y <= 55:
            current_color = c
            tool = "brush"
        cx += 45


running = True
drawing = False
start_pos = None

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()

            if pos[1] <= 80:
                select_toolbar(pos)
            else:
                drawing = True
                start_pos = pos
                canvas = screen.copy()

        if event.type == pygame.MOUSEBUTTONUP:
            if drawing and start_pos:
                end = pygame.mouse.get_pos()

                if tool == "rect":
                    r = pygame.Rect(
                        min(start_pos[0], end[0]),
                        min(start_pos[1], end[1]),
                        abs(end[0] - start_pos[0]),
                        abs(end[1] - start_pos[1])
                    )
                    pygame.draw.rect(screen, current_color, r, 3)

                elif tool == "circle":
                    radius = int(((end[0] - start_pos[0]) ** 2 +
                                  (end[1] - start_pos[1]) ** 2) ** 0.5)
                    pygame.draw.circle(screen, current_color, start_pos, radius, 3)

            drawing = False
            start_pos = None
            canvas = screen.copy()

        if event.type == pygame.MOUSEMOTION and drawing:
            pos = pygame.mouse.get_pos()

            if tool in ["rect", "circle"]:
                screen.blit(canvas, (0, 0))

            if pos[1] > 80:
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

                elif tool == "rect":
                    r = pygame.Rect(
                        min(start_pos[0], pos[0]),
                        min(start_pos[1], pos[1]),
                        abs(pos[0] - start_pos[0]),
                        abs(pos[1] - start_pos[1])
                    )
                    pygame.draw.rect(screen, current_color, r, 3)

                elif tool == "circle":
                    radius = int(((pos[0] - start_pos[0]) ** 2 +
                                  (pos[1] - start_pos[1]) ** 2) ** 0.5)
                    pygame.draw.circle(screen, current_color, start_pos, radius, 3)

    draw_toolbar()
    pygame.display.update()

pygame.quit()