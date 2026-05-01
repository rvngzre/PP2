import json
import os

SETTINGS_FILE = "settings.json"
LEADERBOARD_FILE = "leaderboard.json"

DEFAULT_SETTINGS = {
    "sound": True,
    "car_color": "red",
    "difficulty": "normal"
}

COLOR_OPTIONS = {
    "red": (220, 0, 0),
    "blue": (40, 120, 255),
    "green": (0, 180, 80),
    "yellow": (255, 220, 0)
}

DIFFICULTY_OPTIONS = {
    "easy": {"enemy_speed": 4, "spawn_rate": 1500, "finish_distance": 2500},
    "normal": {"enemy_speed": 5, "spawn_rate": 1100, "finish_distance": 3000},
    "hard": {"enemy_speed": 6, "spawn_rate": 800, "finish_distance": 3500}
}


def load_json(filename, default_data):
    if not os.path.exists(filename):
        save_json(filename, default_data)
        return default_data.copy() if isinstance(default_data, dict) else list(default_data)

    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data
    except (json.JSONDecodeError, OSError):
        save_json(filename, default_data)
        return default_data.copy() if isinstance(default_data, dict) else list(default_data)


def save_json(filename, data):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def load_settings():
    settings = load_json(SETTINGS_FILE, DEFAULT_SETTINGS)

    for key, value in DEFAULT_SETTINGS.items():
        if key not in settings:
            settings[key] = value

    if settings["car_color"] not in COLOR_OPTIONS:
        settings["car_color"] = DEFAULT_SETTINGS["car_color"]

    if settings["difficulty"] not in DIFFICULTY_OPTIONS:
        settings["difficulty"] = DEFAULT_SETTINGS["difficulty"]

    save_settings(settings)
    return settings


def save_settings(settings):
    save_json(SETTINGS_FILE, settings)


def load_leaderboard():
    data = load_json(LEADERBOARD_FILE, [])
    if not isinstance(data, list):
        data = []
    return data


def save_score(name, score, distance, coins):
    leaderboard = load_leaderboard()

    leaderboard.append({
        "name": name if name else "Player",
        "score": int(score),
        "distance": int(distance),
        "coins": int(coins)
    })

    leaderboard.sort(key=lambda item: item["score"], reverse=True)
    leaderboard = leaderboard[:10]
    save_json(LEADERBOARD_FILE, leaderboard)
    return leaderboard
