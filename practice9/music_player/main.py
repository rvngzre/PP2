import pygame
import sys
from player import MusicPlayer

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Music Player")

background = pygame.image.load("images/bg.jpeg")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

panel_size = 400
panel_rect = pygame.Rect(
    (WIDTH - panel_size) // 2,
    (HEIGHT - panel_size) // 2,
    panel_size,
    panel_size
)

title_font = pygame.font.SysFont("Arial", 30)
main_font = pygame.font.SysFont("Arial", 22)
hint_font = pygame.font.SysFont("Arial", 16)

tracks = [
    "music/sample_tracks/Playboi-Carti-Magnolia.wav",
    "music/sample_tracks/Playboi-Carti-RIP.wav",
    "music/sample_tracks/Playboi-Carti-FlatBed-Freestyle.wav"
]

player = MusicPlayer(tracks)
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                player.play()
            elif event.key == pygame.K_s:
                player.pause()
            elif event.key == pygame.K_n:
                player.next_track()
            elif event.key == pygame.K_b:
                player.previous_track()
            elif event.key == pygame.K_q:
                pygame.quit()
                sys.exit()

    screen.blit(background, (0, 0))

    panel_surface = pygame.Surface((panel_size, panel_size), pygame.SRCALPHA)
    panel_surface.fill((0, 0, 0, 220))
    screen.blit(panel_surface, panel_rect.topleft)

    cx = panel_rect.centerx
    top = panel_rect.top

    title = title_font.render("Music Player", True, (255, 255, 255))
    screen.blit(title, title.get_rect(center=(cx, top + 60)))

    track = main_font.render(
        f"{player.current_index + 1}/3: {player.get_current_track()}",
        True, (255, 255, 255)
    )
    screen.blit(track, track.get_rect(center=(cx, top + 150)))

    status = "Playing" if player.is_playing else "Paused"
    status_text = main_font.render(
        f"Status: {status}",
        True, (255, 255, 255)
    )
    screen.blit(status_text, status_text.get_rect(center=(cx, top + 190)))

    hints = hint_font.render(
        "P-Play   S-Pause   N-Next   B-Back   Q-Quit",
        True, (255, 255, 255)
    )
    screen.blit(hints, hints.get_rect(center=(cx, panel_rect.bottom - 40)))

    pygame.display.flip()
    clock.tick(10)