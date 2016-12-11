import math
import numpy as np
from settings import width, height, goal_width, goal_height
from pygame import Rect


def tonp(x):
    if type(x) != np.ndarray:
        x = np.array(x)
    return x


def dist(a, b):
    a = tonp(a)
    b = tonp(b)
    return math.hypot(a[0] - b[0], a[1] - b[1])


def angle_diff(a, b):
    diff = a - b
    diff = (diff + 180) % 360 - 180
    return diff


def vector_to(a, b):
    a = tonp(a)
    b = tonp(b)
    return b - a


def normalize_vector(a, limit):
    # limit must be positive
    d = dist([0, 0], a)
    if d == 0:
        return a
    a = tonp(a)
    a = a / d   # make vector of size 1
    return a * limit


def pixelof(x, y):
    # print x, y
    return int((x + 1) * width / 2.0), int((y + 1) * height / 2.0)


def size2pixels(size):
    return int(size * min(width, height))


def angle_to(a, b):
    ret = np.arctan2(b[1] - a[1], b[0] - a[0])
    return np.degrees(ret)


def angle_of(a):
    return angle_to([0, 0], a)


def get_goal_rect(goal):
    top_left = pixelof(goal[0] - goal_width, goal[1] - goal_height)
    return Rect(top_left, (goal_width * width, goal_height * height))
