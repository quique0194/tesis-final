import math
import numpy as np
from settings import width, height


def dist(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])


def pixelof(x, y):
    return int((x + 1) * width / 2.0), int((y + 1) * height / 2.0)


def angle_to(a, b):
    print a, b
    ret = np.arctan2(b[0] - a[0], b[1] - a[1])
    return np.degrees(ret)
