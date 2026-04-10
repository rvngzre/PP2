class Ball:
    def __init__(self, x, y, radius, speed):
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = speed

    def move_left(self):
        if self.x - self.speed - self.radius >= 0:
            self.x -= self.speed

    def move_right(self, screen_width):
        if self.x + self.speed + self.radius <= screen_width:
            self.x += self.speed

    def move_up(self):
        if self.y - self.speed - self.radius >= 0:
            self.y -= self.speed

    def move_down(self, screen_height):
        if self.y + self.speed + self.radius <= screen_height:
            self.y += self.speed