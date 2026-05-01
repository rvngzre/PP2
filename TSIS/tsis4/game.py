import json
import random
import pygame
from config import *
from db import Database


class SnakeGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Snake")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 26)
        self.small_font = pygame.font.SysFont("Arial", 19)
        self.big_font = pygame.font.SysFont("Arial", 42)
        self.db = Database()
        self.settings = self.load_settings()
        self.username = "Player"
        self.screen_name = "menu"
        self.running = True
        self.saved = False
        self.start_new_game()

    def load_settings(self):
        try:
            with open("settings.json", "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {"snake_color": [0, 180, 0], "grid": True, "sound": True}

    def save_settings(self):
        with open("settings.json", "w") as file:
            json.dump(self.settings, file, indent=4)

    def start_new_game(self):
        self.snake = [(WIDTH // 2, HEIGHT // 2)]
        self.direction = (CELL, 0)
        self.next_direction = self.direction
        self.score = 0
        self.level = 1
        self.move_delay = 150
        self.last_move = pygame.time.get_ticks()
        self.food_types = [{"value": 1}, {"value": 2}, {"value": 3}, {"value": 4}, {"value": 5}]
        self.food = None
        self.food_value = 1
        self.food_spawn_time = pygame.time.get_ticks()
        self.food_lifetime = 5000
        self.poison = None
        self.power_up = None
        self.power_up_type = None
        self.power_up_spawn_time = 0
        self.power_up_active = None
        self.power_up_end_time = 0
        self.shield = False
        self.obstacles = []
        self.game_over = False
        self.saved = False
        self.personal_best = self.db.get_personal_best(self.username)
        self.food = self.generate_free_position()
        self.spawn_poison()

    def generate_free_position(self):
        while True:
            x = random.randrange(0, WIDTH, CELL)
            y = random.randrange(0, HEIGHT, CELL)
            position = (x, y)
            if position not in self.snake and position not in self.obstacles and position != self.food and position != self.poison:
                return position

    def spawn_food(self):
        selected_food = random.choice(self.food_types)
        self.food_value = selected_food["value"]
        self.food_spawn_time = pygame.time.get_ticks()
        self.food = self.generate_free_position()

    def spawn_poison(self):
        self.poison = self.generate_free_position()

    def spawn_power_up(self):
        if self.power_up is None and random.randint(1, 100) <= 2:
            self.power_up = self.generate_free_position()
            self.power_up_type = random.choice(["speed", "slow", "shield"])
            self.power_up_spawn_time = pygame.time.get_ticks()

    def generate_obstacles(self):
        if self.level < 3:
            self.obstacles = []
            return

        new_obstacles = []
        count = min(4 + self.level * 2, 35)
        safe_area = [
            self.snake[0],
            (self.snake[0][0] + CELL, self.snake[0][1]),
            (self.snake[0][0] - CELL, self.snake[0][1]),
            (self.snake[0][0], self.snake[0][1] + CELL),
            (self.snake[0][0], self.snake[0][1] - CELL)
        ]

        while len(new_obstacles) < count:
            x = random.randrange(0, WIDTH, CELL)
            y = random.randrange(0, HEIGHT, CELL)
            block = (x, y)
            if block not in self.snake and block not in safe_area and block not in new_obstacles and block != self.food:
                new_obstacles.append(block)

        self.obstacles = new_obstacles

    def draw_text(self, text, font, color, x, y, center=False):
        surface = font.render(text, True, color)
        rect = surface.get_rect()
        if center:
            rect.center = (x, y)
        else:
            rect.topleft = (x, y)
        self.screen.blit(surface, rect)
        return rect

    def draw_button(self, text, x, y, w, h):
        mouse = pygame.mouse.get_pos()
        rect = pygame.Rect(x, y, w, h)
        color = GRAY if rect.collidepoint(mouse) else DARK_GRAY
        pygame.draw.rect(self.screen, color, rect, border_radius=8)
        pygame.draw.rect(self.screen, BLACK, rect, 2, border_radius=8)
        self.draw_text(text, self.font, WHITE, x + w // 2, y + h // 2, True)
        return rect

    def draw_grid(self):
        if not self.settings.get("grid", True):
            return

        for x in range(0, WIDTH, CELL):
            pygame.draw.line(self.screen, (230, 230, 230), (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, CELL):
            pygame.draw.line(self.screen, (230, 230, 230), (0, y), (WIDTH, y))

    def handle_menu_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.username = self.username[:-1]
            elif event.key == pygame.K_RETURN:
                if self.username.strip() == "":
                    self.username = "Player"
                self.start_new_game()
                self.screen_name = "game"
            else:
                if len(self.username) < 15 and event.unicode.isprintable():
                    self.username += event.unicode

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.play_button.collidepoint(event.pos):
                if self.username.strip() == "":
                    self.username = "Player"
                self.start_new_game()
                self.screen_name = "game"
            elif self.leaderboard_button.collidepoint(event.pos):
                self.screen_name = "leaderboard"
            elif self.settings_button.collidepoint(event.pos):
                self.screen_name = "settings"
            elif self.quit_button.collidepoint(event.pos):
                self.running = False

    def handle_game_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and self.direction != (0, CELL):
                self.next_direction = (0, -CELL)
            elif event.key == pygame.K_DOWN and self.direction != (0, -CELL):
                self.next_direction = (0, CELL)
            elif event.key == pygame.K_LEFT and self.direction != (CELL, 0):
                self.next_direction = (-CELL, 0)
            elif event.key == pygame.K_RIGHT and self.direction != (-CELL, 0):
                self.next_direction = (CELL, 0)
            elif event.key == pygame.K_ESCAPE:
                self.screen_name = "menu"

    def handle_game_over_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.retry_button.collidepoint(event.pos):
                self.start_new_game()
                self.screen_name = "game"
            elif self.menu_button.collidepoint(event.pos):
                self.screen_name = "menu"

    def handle_leaderboard_events(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.screen_name = "menu"
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.back_button.collidepoint(event.pos):
                self.screen_name = "menu"

    def handle_settings_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.grid_button.collidepoint(event.pos):
                self.settings["grid"] = not self.settings.get("grid", True)
            elif self.sound_button.collidepoint(event.pos):
                self.settings["sound"] = not self.settings.get("sound", True)
            elif self.color_button.collidepoint(event.pos):
                colors = [[0, 180, 0], [40, 120, 255], [150, 70, 220], [230, 190, 0]]
                current = self.settings.get("snake_color", [0, 180, 0])
                index = colors.index(current) if current in colors else 0
                self.settings["snake_color"] = colors[(index + 1) % len(colors)]
            elif self.save_button.collidepoint(event.pos):
                self.save_settings()
                self.screen_name = "menu"

    def update_game(self):
        now = pygame.time.get_ticks()

        if self.game_over:
            if not self.saved:
                self.db.save_result(self.username, self.score, self.level)
                self.personal_best = max(self.personal_best, self.score)
                self.saved = True
            self.screen_name = "game_over"
            return

        if now - self.food_spawn_time > self.food_lifetime:
            self.spawn_food()

        if self.power_up is None:
            self.spawn_power_up()
        elif now - self.power_up_spawn_time > 8000:
            self.power_up = None
            self.power_up_type = None

        if self.power_up_active in ["speed", "slow"] and now > self.power_up_end_time:
            self.power_up_active = None

        current_delay = self.move_delay
        if self.power_up_active == "speed":
            current_delay = max(40, self.move_delay - 50)
        elif self.power_up_active == "slow":
            current_delay = self.move_delay + 70

        if now - self.last_move <= current_delay:
            return

        self.last_move = now
        self.direction = self.next_direction

        head = (
            self.snake[0][0] + self.direction[0],
            self.snake[0][1] + self.direction[1]
        )

        collision = (
            head[0] < 0 or
            head[0] >= WIDTH or
            head[1] < 0 or
            head[1] >= HEIGHT or
            head in self.snake or
            head in self.obstacles
        )

        if collision:
            if self.shield:
                self.shield = False
                return
            self.game_over = True
            return

        self.snake.insert(0, head)

        if head == self.food:
            self.score += self.food_value
            self.spawn_food()

            new_level = self.score // 4 + 1
            if new_level > self.level:
                self.level = new_level
                self.move_delay = max(60, self.move_delay - 10)
                self.generate_obstacles()

        elif head == self.poison:
            for _ in range(2):
                if len(self.snake) > 1:
                    self.snake.pop()
            self.spawn_poison()
            if len(self.snake) <= 1:
                self.game_over = True

        elif head == self.power_up:
            if self.power_up_type == "shield":
                self.shield = True
            else:
                self.power_up_active = self.power_up_type
                self.power_up_end_time = pygame.time.get_ticks() + 5000
            self.power_up = None
            self.power_up_type = None

        else:
            self.snake.pop()

    def draw_menu(self):
        self.screen.fill(WHITE)
        self.draw_text("SNAKE TSIS4", self.big_font, BLACK, WIDTH // 2, 55, True)
        self.draw_text("Enter username:", self.font, BLACK, WIDTH // 2, 110, True)
        pygame.draw.rect(self.screen, WHITE, (190, 135, 220, 40))
        pygame.draw.rect(self.screen, BLACK, (190, 135, 220, 40), 2)
        self.draw_text(self.username, self.font, BLACK, WIDTH // 2, 155, True)
        self.play_button = self.draw_button("Play", 220, 195, 160, 40)
        self.leaderboard_button = self.draw_button("Leaderboard", 220, 245, 160, 40)
        self.settings_button = self.draw_button("Settings", 220, 295, 160, 40)
        self.quit_button = self.draw_button("Quit", 220, 345, 160, 40)

    def draw_game(self):
        self.screen.fill(WHITE)
        self.draw_grid()

        for block in self.obstacles:
            pygame.draw.rect(self.screen, DARK_GRAY, (block[0], block[1], CELL, CELL))

        snake_color = tuple(self.settings.get("snake_color", [0, 180, 0]))
        for part in self.snake:
            pygame.draw.rect(self.screen, snake_color, (part[0], part[1], CELL, CELL))

        pygame.draw.rect(self.screen, RED, (self.food[0], self.food[1], CELL, CELL))
        food_text = self.small_font.render(str(self.food_value), True, WHITE)
        food_rect = food_text.get_rect(center=(self.food[0] + CELL // 2, self.food[1] + CELL // 2))
        self.screen.blit(food_text, food_rect)

        if self.poison:
            pygame.draw.rect(self.screen, DARK_RED, (self.poison[0], self.poison[1], CELL, CELL))
            self.draw_text("P", self.small_font, WHITE, self.poison[0] + CELL // 2, self.poison[1] + CELL // 2, True)

        if self.power_up:
            color = BLUE if self.power_up_type == "speed" else YELLOW if self.power_up_type == "slow" else PURPLE
            letter = "F" if self.power_up_type == "speed" else "S" if self.power_up_type == "slow" else "H"
            pygame.draw.rect(self.screen, color, (self.power_up[0], self.power_up[1], CELL, CELL))
            self.draw_text(letter, self.small_font, BLACK, self.power_up[0] + CELL // 2, self.power_up[1] + CELL // 2, True)

        now = pygame.time.get_ticks()
        time_left = max(0, (self.food_lifetime - (now - self.food_spawn_time)) // 1000 + 1)
        self.draw_text(f"Score: {self.score}", self.small_font, BLACK, 10, 8)
        self.draw_text(f"Level: {self.level}", self.small_font, BLACK, 10, 30)
        self.draw_text(f"Best: {self.personal_best}", self.small_font, BLACK, 10, 52)
        self.draw_text(f"Food time: {time_left}", self.small_font, BLACK, 10, 74)
        if self.shield:
            self.draw_text("Shield: ON", self.small_font, PURPLE, 470, 8)
        if self.power_up_active:
            self.draw_text(f"Power: {self.power_up_active}", self.small_font, BLUE, 450, 30)

    def draw_game_over(self):
        self.screen.fill(WHITE)
        self.draw_text("GAME OVER", self.big_font, RED, WIDTH // 2, 85, True)
        self.draw_text(f"Score: {self.score}", self.font, BLACK, WIDTH // 2, 145, True)
        self.draw_text(f"Level reached: {self.level}", self.font, BLACK, WIDTH // 2, 180, True)
        self.draw_text(f"Personal best: {self.personal_best}", self.font, BLACK, WIDTH // 2, 215, True)
        self.retry_button = self.draw_button("Retry", 210, 270, 180, 45)
        self.menu_button = self.draw_button("Main Menu", 210, 325, 180, 45)

    def draw_leaderboard(self):
        self.screen.fill(WHITE)
        self.draw_text("LEADERBOARD", self.big_font, BLACK, WIDTH // 2, 40, True)
        self.draw_text("#  Username        Score  Level  Date", self.small_font, BLACK, 55, 85)
        scores = self.db.get_top_scores()
        y = 115
        for index, row in enumerate(scores, start=1):
            username, score, level, played_at = row
            date = played_at.strftime("%Y-%m-%d")
            self.draw_text(f"{index:<2} {username:<14} {score:<6} {level:<5} {date}", self.small_font, BLACK, 55, y)
            y += 25
        if not scores:
            self.draw_text("No database records yet", self.font, RED, WIDTH // 2, 180, True)
        self.back_button = self.draw_button("Back", 220, 335, 160, 40)

    def draw_settings(self):
        self.screen.fill(WHITE)
        self.draw_text("SETTINGS", self.big_font, BLACK, WIDTH // 2, 60, True)
        grid_status = "ON" if self.settings.get("grid", True) else "OFF"
        sound_status = "ON" if self.settings.get("sound", True) else "OFF"
        self.grid_button = self.draw_button(f"Grid: {grid_status}", 190, 130, 220, 45)
        self.sound_button = self.draw_button(f"Sound: {sound_status}", 190, 190, 220, 45)
        self.color_button = self.draw_button("Change Snake Color", 190, 250, 220, 45)
        snake_color = tuple(self.settings.get("snake_color", [0, 180, 0]))
        pygame.draw.rect(self.screen, snake_color, (430, 257, 30, 30))
        self.save_button = self.draw_button("Save & Back", 190, 320, 220, 45)

    def run(self):
        while self.running:
            self.clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if self.screen_name == "menu":
                    self.handle_menu_events(event)
                elif self.screen_name == "game":
                    self.handle_game_events(event)
                elif self.screen_name == "game_over":
                    self.handle_game_over_events(event)
                elif self.screen_name == "leaderboard":
                    self.handle_leaderboard_events(event)
                elif self.screen_name == "settings":
                    self.handle_settings_events(event)

            if self.screen_name == "game":
                self.update_game()
                self.draw_game()
            elif self.screen_name == "menu":
                self.draw_menu()
            elif self.screen_name == "game_over":
                self.draw_game_over()
            elif self.screen_name == "leaderboard":
                self.draw_leaderboard()
            elif self.screen_name == "settings":
                self.draw_settings()

            pygame.display.update()

        pygame.quit()
