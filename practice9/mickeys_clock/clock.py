import math
from datetime import datetime

def get_angles():
    now = datetime.now()
    seconds = now.second
    minutes = now.minute

    sec_angle = seconds * 6
    min_angle = minutes * 6

    return sec_angle, min_angle


def get_hand_position(center, length, angle):
    x = center[0] + length * math.cos(math.radians(angle - 90))
    y = center[1] + length * math.sin(math.radians(angle - 90))
    return (x, y)