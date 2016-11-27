import math
import numpy as np
from settings import width, height
from pygame import Rect


def dist(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])


def pixelof(x, y):
    return int((x + 1) * width / 2.0), int((y + 1) * height / 2.0)


def size2pixels(size):
    return int(size * min(width, height))


def angle_to(a, b):
    ret = np.arctan2(b[0] - a[0], b[1] - a[1])
    return np.degrees(ret)


def get_goal_rect(goal):
    goal_width = 0.05
    goal_height = 0.25
    top_left = pixelof(goal[0] - goal_width, goal[1] - goal_height)
    return Rect(top_left, (goal_width * width, goal_height * height))
