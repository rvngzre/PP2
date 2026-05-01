import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (80, 80, 80)
DARK_GRAY = (35, 35, 35)
LIGHT_GRAY = (160, 160, 160)
GREEN = (0, 180, 0)
RED = (220, 0, 0)
YELLOW = (255, 220, 0)
BLUE = (40, 120, 255)
ORANGE = (255, 150, 0)
PURPLE = (140, 70, 220)


class Button:
    def __init__(self, x, y, width, height, text, font):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        color = LIGHT_GRAY if self.rect.collidepoint(mouse_pos) else WHITE
        pygame.draw.rect(screen, color, self.rect, border_radius=12)
        pygame.draw.rect(screen, BLACK, self.rect, 2, border_radius=12)
        text_surface = self.font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos)


def draw_center_text(screen, text, font, color, y):
    surface = font.render(text, True, color)
    rect = surface.get_rect(center=(screen.get_width() // 2, y))
    screen.blit(surface, rect)


def draw_panel(screen, rect):
    panel = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    panel.fill((0, 0, 0, 180))
    screen.blit(panel, rect)
    pygame.draw.rect(screen, WHITE, rect, 2, border_radius=16)
