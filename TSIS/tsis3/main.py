import pygame
import sys
from racer import RacerGame, WIDTH, HEIGHT
from ui import Button, WHITE, BLACK, DARK_GRAY, GREEN, RED, YELLOW, draw_center_text, draw_panel
from persistence import load_settings, save_settings, load_leaderboard, save_score, COLOR_OPTIONS, DIFFICULTY_OPTIONS

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer")
clock = pygame.time.Clock()

fonts = {
    "small": pygame.font.SysFont("Arial", 20),
    "font": pygame.font.SysFont("Arial", 28),
    "big": pygame.font.SysFont("Arial", 42)
}

settings = load_settings()
username = ""


def quit_game():
    pygame.quit()
    sys.exit()


def get_username():
    global username
    username = ""
    active = True

    while active:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and username.strip():
                    active = False
                elif event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                elif len(username) < 12 and event.unicode.isprintable():
                    username += event.unicode

        screen.fill(DARK_GRAY)
        draw_center_text(screen, "Enter username", fonts["big"], WHITE, 170)
        pygame.draw.rect(screen, WHITE, (70, 250, 260, 55), border_radius=10)
        pygame.draw.rect(screen, BLACK, (70, 250, 260, 55), 2, border_radius=10)

        name_surface = fonts["font"].render(username, True, BLACK)
        screen.blit(name_surface, (85, 260))

        draw_center_text(screen, "Press ENTER to start", fonts["small"], WHITE, 340)
        pygame.display.update()

    if not username.strip():
        username = "Player"


def main_menu():
    buttons = [
        Button(100, 180, 200, 50, "Play", fonts["font"]),
        Button(100, 250, 200, 50, "Leaderboard", fonts["font"]),
        Button(100, 320, 200, 50, "Settings", fonts["font"]),
        Button(100, 390, 200, 50, "Quit", fonts["font"])
    ]

    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

            if buttons[0].clicked(event):
                get_username()
                game_loop()
            elif buttons[1].clicked(event):
                leaderboard_screen()
            elif buttons[2].clicked(event):
                settings_screen()
            elif buttons[3].clicked(event):
                quit_game()

        screen.fill(WHITE)
        draw_center_text(screen, "RACER", fonts["big"], BLACK, 115)

        for button in buttons:
            button.draw(screen)

        pygame.display.update()


def settings_screen():
    global settings

    back_button = Button(115, 500, 170, 45, "Back", fonts["font"])
    sound_button = Button(70, 140, 260, 45, "", fonts["font"])
    color_button = Button(70, 220, 260, 45, "", fonts["font"])
    diff_button = Button(70, 300, 260, 45, "", fonts["font"])

    colors = list(COLOR_OPTIONS.keys())
    difficulties = list(DIFFICULTY_OPTIONS.keys())

    while True:
        clock.tick(60)

        sound_button.text = f"Sound: {'ON' if settings['sound'] else 'OFF'}"
        color_button.text = f"Car: {settings['car_color'].title()}"
        diff_button.text = f"Difficulty: {settings['difficulty'].title()}"

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

            if sound_button.clicked(event):
                settings["sound"] = not settings["sound"]
                save_settings(settings)
            elif color_button.clicked(event):
                index = colors.index(settings["car_color"])
                settings["car_color"] = colors[(index + 1) % len(colors)]
                save_settings(settings)
            elif diff_button.clicked(event):
                index = difficulties.index(settings["difficulty"])
                settings["difficulty"] = difficulties[(index + 1) % len(difficulties)]
                save_settings(settings)
            elif back_button.clicked(event):
                return

        screen.fill(DARK_GRAY)
        draw_center_text(screen, "Settings", fonts["big"], WHITE, 80)
        sound_button.draw(screen)
        color_button.draw(screen)
        diff_button.draw(screen)
        back_button.draw(screen)
        pygame.display.update()


def leaderboard_screen():
    back_button = Button(115, 520, 170, 45, "Back", fonts["font"])

    while True:
        clock.tick(60)
        leaderboard = load_leaderboard()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

            if back_button.clicked(event):
                return

        screen.fill(DARK_GRAY)
        draw_center_text(screen, "Top 10 Leaderboard", fonts["big"], WHITE, 55)

        header = fonts["small"].render("Rank   Name        Score   Distance", True, YELLOW)
        screen.blit(header, (35, 105))

        if not leaderboard:
            draw_center_text(screen, "No scores yet", fonts["font"], WHITE, 280)
        else:
            for index, item in enumerate(leaderboard[:10], start=1):
                line = f"{index:<3}    {item['name'][:9]:<9}   {item['score']:<5}   {item['distance']}m"
                surface = fonts["small"].render(line, True, WHITE)
                screen.blit(surface, (35, 115 + index * 35))

        back_button.draw(screen)
        pygame.display.update()


def game_over_screen(results):
    retry_button = Button(70, 400, 120, 45, "Retry", fonts["font"])
    menu_button = Button(210, 400, 120, 45, "Menu", fonts["font"])

    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

            if retry_button.clicked(event):
                game_loop()
                return

            if menu_button.clicked(event):
                return

        screen.fill(DARK_GRAY)
        title = "FINISH!" if results["finished"] else "GAME OVER"
        title_color = YELLOW if results["finished"] else RED

        draw_center_text(screen, title, fonts["big"], title_color, 120)
        panel_rect = pygame.Rect(55, 180, 290, 170)
        draw_panel(screen, panel_rect)

        lines = [
            f"Score: {results['score']}",
            f"Distance: {results['distance']}m",
            f"Coins: {results['coins']}",
            f"Player: {username}"
        ]

        for index, line in enumerate(lines):
            surface = fonts["font"].render(line, True, WHITE)
            screen.blit(surface, (85, 205 + index * 35))

        retry_button.draw(screen)
        menu_button.draw(screen)
        pygame.display.update()


def game_loop():
    game = RacerGame(screen, clock, fonts, settings, username)

    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

        if not game.game_over:
            game.update()

        game.draw()
        pygame.display.update()

        if game.game_over:
            results = game.get_results()
            if not game.saved:
                save_score(username, results["score"], results["distance"], results["coins"])
                game.saved = True
            game_over_screen(results)
            return


if __name__ == "__main__":
    main_menu()
