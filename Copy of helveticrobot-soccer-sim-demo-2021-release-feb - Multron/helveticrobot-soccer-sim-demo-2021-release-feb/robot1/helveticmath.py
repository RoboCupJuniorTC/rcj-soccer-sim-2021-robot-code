import math

def distance(a: dict, b: dict) -> dict:
    """Calculate the distance between two points

    Source: https://stackoverflow.com/a/5228392

    Args:
        a (dict): the from point
        b (dict): the to point

    Returns:
        dict: the distance between the two points
    """
    return math.hypot(b["x"] - a["x"], b["y"] - a["y"])

def line_intersection(line1: dict, line2: dict, segment: bool) -> dict:
    """Calculate the intersection point of two lines

    Source: https://stackoverflow.com/a/20677983

    Args:
        line1 (dict): the first line. When segment is true, this is the segment
        line2 (dict): the second line
        segment (bool): whether the first line is a segment

    Raises:
        Exception: When the lines do not intersect

    Returns:
        dict: the point where the lines intersect
    """
    xdiff = (line1[0]["x"] - line1[1]["x"], line2[0]["x"] - line2[1]["x"])
    ydiff = (line1[0]["y"] - line1[1]["y"], line2[0]["y"] - line2[1]["y"])

    def detp(a, b):
        return a[0] * b[1] - a[1] * b[0]

    def detk(a, b):
        return a["x"] * b["y"] - a["y"] * b["x"]

    div = detp(xdiff, ydiff)
    if div == 0:
       raise Exception('lines do not intersect')

    d = (detk(*line1), detk(*line2))
    x = detp(d, xdiff) / div
    y = detp(d, ydiff) / div

    intersect = {"x": x, "y": y}

    if segment:
        if not isBetween(line1[0], line1[1], intersect):
            raise Exception('lines do not intersect with segment')

    return intersect

def isBetween(a: dict, b: dict, c: dict) -> bool:
    """Check whether point c is on the line segment of points a and b

    Source: https://stackoverflow.com/a/328122

    Args:
        a (dict): the point a
        b (dict): the point b
        c (dict): the point c

    Returns:
        bool: whether point c is on the line segment of points a and b
    """

    epsilon = 1e-6

    crossproduct = (c["y"] - a["y"]) * (b["x"] - a["x"]) - (c["x"] - a["x"]) * (b["y"] - a["y"])

    return -epsilon < crossproduct < epsilon and min(a["x"], b["x"]) <= c["x"] <= max(a["x"], b["x"]) and min(a["y"], b["y"]) <= c["y"] <= max(a["y"], b["y"])