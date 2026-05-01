import psycopg2
from config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT


class Database:
    def __init__(self):
        self.connection = None
        self.connect()
        self.create_tables()

    def connect(self):
        try:
            self.connection = psycopg2.connect(
                dbname=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD,
                host=DB_HOST,
                port=DB_PORT
            )
        except Exception as error:
            print("Database connection error:", error)
            self.connection = None

    def create_tables(self):
        if self.connection is None:
            return

        cursor = self.connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS players (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL
            );
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS game_sessions (
                id SERIAL PRIMARY KEY,
                player_id INTEGER REFERENCES players(id),
                score INTEGER NOT NULL,
                level_reached INTEGER NOT NULL,
                played_at TIMESTAMP DEFAULT NOW()
            );
        """)

        self.connection.commit()
        cursor.close()

    def get_player_id(self, username):
        if self.connection is None:
            return None

        cursor = self.connection.cursor()

        cursor.execute(
            "INSERT INTO players (username) VALUES (%s) ON CONFLICT (username) DO NOTHING;",
            (username,)
        )

        self.connection.commit()

        cursor.execute(
            "SELECT id FROM players WHERE username = %s;",
            (username,)
        )

        result = cursor.fetchone()
        cursor.close()

        if result:
            return result[0]
        return None

    def save_result(self, username, score, level):
        if self.connection is None:
            return

        player_id = self.get_player_id(username)

        if player_id is None:
            return

        cursor = self.connection.cursor()

        cursor.execute(
            "INSERT INTO game_sessions (player_id, score, level_reached) VALUES (%s, %s, %s);",
            (player_id, score, level)
        )

        self.connection.commit()
        cursor.close()

    def get_personal_best(self, username):
        if self.connection is None:
            return 0

        player_id = self.get_player_id(username)

        if player_id is None:
            return 0

        cursor = self.connection.cursor()

        cursor.execute(
            "SELECT COALESCE(MAX(score), 0) FROM game_sessions WHERE player_id = %s;",
            (player_id,)
        )

        result = cursor.fetchone()
        cursor.close()

        return result[0]

    def get_top_scores(self):
        if self.connection is None:
            return []

        cursor = self.connection.cursor()

        cursor.execute("""
            SELECT players.username, game_sessions.score, game_sessions.level_reached, game_sessions.played_at
            FROM game_sessions
            JOIN players ON players.id = game_sessions.player_id
            ORDER BY game_sessions.score DESC, game_sessions.level_reached DESC
            LIMIT 10;
        """)

        results = cursor.fetchall()
        cursor.close()

        return results
