import pygame
import random
from ui import WHITE, BLACK, GRAY, GREEN, RED, YELLOW, BLUE, ORANGE, PURPLE, draw_center_text, draw_panel
from persistence import COLOR_OPTIONS, DIFFICULTY_OPTIONS

WIDTH, HEIGHT = 400, 600
ROAD_LEFT = 50
ROAD_RIGHT = WIDTH - 50
LANE_WIDTH = (ROAD_RIGHT - ROAD_LEFT) // 3
LANES = [ROAD_LEFT + LANE_WIDTH // 2, ROAD_LEFT + LANE_WIDTH + LANE_WIDTH // 2, ROAD_LEFT + LANE_WIDTH * 2 + LANE_WIDTH // 2]


class RacerGame:
    def __init__(self, screen, clock, fonts, settings, username):
        self.screen = screen
        self.clock = clock
        self.font = fonts["font"]
        self.small_font = fonts["small"]
        self.big_font = fonts["big"]
        self.settings = settings
        self.username = username if username else "Player"
        self.reset()

    def reset(self):
        difficulty = DIFFICULTY_OPTIONS[self.settings["difficulty"]]
        self.player_width = 50
        self.player_height = 90
        self.player_x = WIDTH // 2 - self.player_width // 2
        self.player_y = HEIGHT - self.player_height - 20
        self.player_speed = 6
        self.enemy_width = 50
        self.enemy_height = 90
        self.base_enemy_speed = difficulty["enemy_speed"]
        self.enemy_speed = self.base_enemy_speed
        self.spawn_rate = difficulty["spawn_rate"]
        self.finish_distance = difficulty["finish_distance"]
        self.coins_collected = 0
        self.distance = 0
        self.score = 0
        self.finished = False
        self.game_over = False
        self.saved = False
        self.traffic = []
        self.obstacles = []
        self.powerups = []
        self.road_lines_offset = 0
        self.last_traffic_spawn = pygame.time.get_ticks()
        self.last_obstacle_spawn = pygame.time.get_ticks()
        self.last_powerup_spawn = pygame.time.get_ticks()
        self.active_powerup = None
        self.powerup_end_time = 0
        self.shield_ready = False
        self.nitro_bonus = 0
        self.coins = [
            {"radius": 10, "value": 1},
            {"radius": 12, "value": 2},
            {"radius": 14, "value": 3},
            {"radius": 16, "value": 4},
            {"radius": 18, "value": 5}
        ]
        self.reset_coin()

    def random_lane_x(self, width):
        lane_center = random.choice(LANES)
        return lane_center - width // 2

    def safe_to_spawn(self, x, y, width, height):
        new_rect = pygame.Rect(x, y, width, height)
        player_rect = pygame.Rect(self.player_x, self.player_y, self.player_width, self.player_height).inflate(30, 120)

        if new_rect.colliderect(player_rect):
            return False

        for item in self.traffic + self.obstacles:
            item_rect = pygame.Rect(item["x"], item["y"], item["w"], item["h"]).inflate(10, 80)
            if new_rect.colliderect(item_rect):
                return False

        return True

    def reset_coin(self):
        current_coin = random.choice(self.coins)
        self.coin_radius = current_coin["radius"]
        self.coin_value = current_coin["value"]
        self.coin_x = random.choice(LANES)
        self.coin_y = random.randint(-600, -80)
        self.coin_speed = 4

    def current_density_bonus(self):
        return min(700, int(self.distance // 300) * 80)

    def spawn_traffic(self):
        x = self.random_lane_x(self.enemy_width)
        y = -self.enemy_height

        if self.safe_to_spawn(x, y, self.enemy_width, self.enemy_height):
            self.traffic.append({"x": x, "y": y, "w": self.enemy_width, "h": self.enemy_height, "speed": self.enemy_speed})

    def spawn_obstacle(self):
        kind = random.choice(["barrier", "oil", "pothole", "bump", "nitro_strip"])
        width, height = 54, 32
        if kind == "oil":
            width, height = 56, 36
        if kind == "pothole":
            width, height = 48, 34
        if kind == "nitro_strip":
            width, height = 60, 24

        x = self.random_lane_x(width)
        y = -height

        if self.safe_to_spawn(x, y, width, height):
            self.obstacles.append({"x": x, "y": y, "w": width, "h": height, "type": kind, "speed": self.enemy_speed - 1})

    def spawn_powerup(self):
        kind = random.choice(["nitro", "shield", "repair"])
        size = 28
        x = random.choice(LANES) - size // 2
        y = random.randint(-700, -120)

        if self.safe_to_spawn(x, y, size, size):
            self.powerups.append({"x": x, "y": y, "w": size, "h": size, "type": kind, "spawn_time": pygame.time.get_ticks()})

    def apply_powerup(self, kind):
        now = pygame.time.get_ticks()

        if kind == "repair":
            self.score += 80
            if self.obstacles:
                self.obstacles.pop(0)
            return

        if self.active_powerup is not None:
            return

        self.active_powerup = kind

        if kind == "nitro":
            self.powerup_end_time = now + 4000
            self.nitro_bonus += 100

        if kind == "shield":
            self.shield_ready = True
            self.powerup_end_time = 0

    def handle_collision(self):
        if self.shield_ready:
            self.shield_ready = False
            self.active_powerup = None
            return
        self.game_over = True

    def update_powerups(self):
        now = pygame.time.get_ticks()

        if self.active_powerup == "nitro" and now > self.powerup_end_time:
            self.active_powerup = None

        self.powerups = [item for item in self.powerups if now - item["spawn_time"] < 6000]

    def update_spawns(self):
        now = pygame.time.get_ticks()
        density = self.current_density_bonus()

        traffic_delay = max(430, self.spawn_rate - density)
        obstacle_delay = max(550, self.spawn_rate + 350 - density)
        powerup_delay = 5000

        if now - self.last_traffic_spawn > traffic_delay:
            self.spawn_traffic()
            self.last_traffic_spawn = now

        if now - self.last_obstacle_spawn > obstacle_delay:
            self.spawn_obstacle()
            self.last_obstacle_spawn = now

        if now - self.last_powerup_spawn > powerup_delay:
            self.spawn_powerup()
            self.last_powerup_spawn = now

    def update(self):
        keys = pygame.key.get_pressed()
        real_player_speed = self.player_speed + (3 if self.active_powerup == "nitro" else 0)

        if keys[pygame.K_LEFT] and self.player_x > ROAD_LEFT + 5:
            self.player_x -= real_player_speed

        if keys[pygame.K_RIGHT] and self.player_x < ROAD_RIGHT - self.player_width - 5:
            self.player_x += real_player_speed

        difficulty_level = int(self.distance // 500)
        self.enemy_speed = self.base_enemy_speed + difficulty_level
        movement_speed = self.enemy_speed + (2 if self.active_powerup == "nitro" else 0)

        self.distance += movement_speed * 0.08
        self.road_lines_offset = (self.road_lines_offset + movement_speed) % 80
        self.coin_y += self.coin_speed + (1 if self.active_powerup == "nitro" else 0)

        self.update_spawns()
        self.update_powerups()

        for car in self.traffic:
            car["y"] += car["speed"]

        for obstacle in self.obstacles:
            obstacle["y"] += obstacle["speed"]

        for powerup in self.powerups:
            powerup["y"] += movement_speed

        self.traffic = [car for car in self.traffic if car["y"] < HEIGHT + 100]
        self.obstacles = [obstacle for obstacle in self.obstacles if obstacle["y"] < HEIGHT + 100]
        self.powerups = [powerup for powerup in self.powerups if powerup["y"] < HEIGHT + 100]

        if self.coin_y > HEIGHT:
            self.reset_coin()

        player_rect = pygame.Rect(self.player_x, self.player_y, self.player_width, self.player_height)
        coin_rect = pygame.Rect(self.coin_x - self.coin_radius, self.coin_y - self.coin_radius, self.coin_radius * 2, self.coin_radius * 2)

        if player_rect.colliderect(coin_rect):
            old_level = self.coins_collected // 10
            self.coins_collected += self.coin_value
            new_level = self.coins_collected // 10

            if new_level > old_level:
                self.enemy_speed += 1

            self.reset_coin()

        for car in self.traffic[:]:
            car_rect = pygame.Rect(car["x"], car["y"], car["w"], car["h"])
            if player_rect.colliderect(car_rect):
                self.traffic.remove(car)
                self.handle_collision()
                break

        for obstacle in self.obstacles[:]:
            obstacle_rect = pygame.Rect(obstacle["x"], obstacle["y"], obstacle["w"], obstacle["h"])
            if player_rect.colliderect(obstacle_rect):
                if obstacle["type"] in ["oil", "pothole", "bump"]:
                    self.player_x += random.choice([-25, 25])
                    self.player_x = max(ROAD_LEFT + 5, min(self.player_x, ROAD_RIGHT - self.player_width - 5))
                    if obstacle["type"] == "bump":
                        self.distance = max(0, self.distance - 15)
                    self.obstacles.remove(obstacle)
                elif obstacle["type"] == "nitro_strip":
                    self.active_powerup = "nitro"
                    self.powerup_end_time = pygame.time.get_ticks() + 2500
                    self.nitro_bonus += 50
                    self.obstacles.remove(obstacle)
                else:
                    self.obstacles.remove(obstacle)
                    self.handle_collision()
                break

        for powerup in self.powerups[:]:
            powerup_rect = pygame.Rect(powerup["x"], powerup["y"], powerup["w"], powerup["h"])
            if player_rect.colliderect(powerup_rect):
                self.apply_powerup(powerup["type"])
                self.powerups.remove(powerup)

        self.score = int(self.coins_collected * 10 + self.distance + self.nitro_bonus)

        if self.distance >= self.finish_distance:
            self.finished = True
            self.game_over = True

    def draw_road(self):
        self.screen.fill(GREEN)
        pygame.draw.rect(self.screen, GRAY, (ROAD_LEFT, 0, ROAD_RIGHT - ROAD_LEFT, HEIGHT))

        for i in range(1, 3):
            x = ROAD_LEFT + LANE_WIDTH * i
            for y in range(-80, HEIGHT, 80):
                pygame.draw.rect(self.screen, WHITE, (x - 4, y + self.road_lines_offset, 8, 40))

    def draw_car(self, x, y, color):
        pygame.draw.rect(self.screen, color, (x, y, self.player_width, self.player_height), border_radius=8)
        pygame.draw.rect(self.screen, BLACK, (x + 8, y + 12, self.player_width - 16, 22), border_radius=5)
        pygame.draw.rect(self.screen, BLACK, (x + 8, y + 58, self.player_width - 16, 18), border_radius=5)

    def draw_obstacle(self, obstacle):
        rect = pygame.Rect(obstacle["x"], obstacle["y"], obstacle["w"], obstacle["h"])

        if obstacle["type"] == "barrier":
            pygame.draw.rect(self.screen, ORANGE, rect, border_radius=5)
            pygame.draw.line(self.screen, BLACK, rect.topleft, rect.bottomright, 4)
        elif obstacle["type"] == "oil":
            pygame.draw.ellipse(self.screen, BLACK, rect)
        elif obstacle["type"] == "pothole":
            pygame.draw.ellipse(self.screen, DARK_COLOR, rect)
        elif obstacle["type"] == "bump":
            pygame.draw.rect(self.screen, YELLOW, rect, border_radius=8)
        elif obstacle["type"] == "nitro_strip":
            pygame.draw.rect(self.screen, BLUE, rect, border_radius=8)

    def draw_powerup(self, powerup):
        colors = {"nitro": BLUE, "shield": PURPLE, "repair": GREEN}
        labels = {"nitro": "N", "shield": "S", "repair": "+"}
        rect = pygame.Rect(powerup["x"], powerup["y"], powerup["w"], powerup["h"])
        pygame.draw.ellipse(self.screen, colors[powerup["type"]], rect)
        pygame.draw.ellipse(self.screen, WHITE, rect, 2)
        text = self.small_font.render(labels[powerup["type"]], True, WHITE)
        self.screen.blit(text, text.get_rect(center=rect.center))

    def draw_hud(self):
        remaining = max(0, int(self.finish_distance - self.distance))
        data = [
            f"Name: {self.username}",
            f"Score: {self.score}",
            f"Coins: {self.coins_collected}",
            f"Dist: {int(self.distance)}m",
            f"Left: {remaining}m"
        ]

        for index, line in enumerate(data):
            surface = self.small_font.render(line, True, WHITE)
            self.screen.blit(surface, (8, 8 + index * 22))

        power_text = "Power: None"
        if self.active_powerup == "nitro":
            left = max(0, (self.powerup_end_time - pygame.time.get_ticks()) // 1000)
            power_text = f"Power: Nitro {left}s"
        elif self.active_powerup == "shield":
            power_text = "Power: Shield"

        surface = self.small_font.render(power_text, True, YELLOW)
        self.screen.blit(surface, (WIDTH - 150, 8))

    def draw(self):
        self.draw_road()

        for obstacle in self.obstacles:
            self.draw_obstacle(obstacle)

        for car in self.traffic:
            self.draw_car(car["x"], car["y"], BLACK)

        for powerup in self.powerups:
            self.draw_powerup(powerup)

        pygame.draw.circle(self.screen, YELLOW, (self.coin_x, int(self.coin_y)), self.coin_radius)
        value_text = self.small_font.render(str(self.coin_value), True, BLACK)
        self.screen.blit(value_text, value_text.get_rect(center=(self.coin_x, int(self.coin_y))))

        player_color = COLOR_OPTIONS[self.settings["car_color"]]
        self.draw_car(self.player_x, self.player_y, player_color)

        if self.shield_ready:
            shield_rect = pygame.Rect(self.player_x - 6, self.player_y - 6, self.player_width + 12, self.player_height + 12)
            pygame.draw.ellipse(self.screen, PURPLE, shield_rect, 3)

        self.draw_hud()

    def get_results(self):
        return {
            "score": self.score,
            "distance": int(self.distance),
            "coins": self.coins_collected,
            "finished": self.finished
        }


DARK_COLOR = (25, 25, 25)
