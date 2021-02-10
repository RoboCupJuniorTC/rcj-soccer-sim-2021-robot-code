# -*- coding: utf-8 -*-

from __future__ import division
from typing import Optional, Tuple, Union

from math import atan2, degrees, hypot, pi, acos, sqrt


class Vector(object):
    def __init__(self, x: float = 0.0, y: float = 0.0):
        self.__x = x
        self.__y = y

    @property
    def x(self) -> float:
        return self.__x

    @property
    def y(self) -> float:
        return self.__y

    def __repr__(self):
        return self.__class__.__name__ + f"({self.x}, {self.y})"

    def __abs__(self) -> float:
        return hypot(self.__x, self.__y)

    # TODO add type hinting
    def __add__(self, other: "Vector") -> "Vector":
        x = self.__x + other.x
        y = self.__y + other.y
        return Vector(x, y)

    def __sub__(self, other: "Vector") -> "Vector":
        x = self.__x - other.x
        y = self.__y - other.y
        return Vector(x, y)

    def __mul__(self, other: Union[float, "Vector"]) -> Union[float, "Vector"]:
        if isinstance(other, (int, float)):
            """Scalar product"""
            return Vector(self.__x * other, self.__y * other)
        if isinstance(other, Vector):
            """Cross product"""
            return self.x * other.y - self.y * self.x

    def __rmul__(self, scalar: float) -> "Vector":
        return self * scalar

    def __pow__(self, power, modulo=None) -> "Vector":
        if modulo:
            raise NotImplementedError
        return (self * power) * power

    def __div__(self, scalar: float) -> "Vector":
        return Vector(self.__x / scalar, self.__y / scalar)

    # TODO division entera

    def __truediv__(self, scalar: float) -> "Vector":
        return Vector(self.__x / scalar, self.__y / scalar)

    def unit(self) -> "Vector":
        """
        Returns the unit vector correspondent to the original one
        """
        module = abs(self)
        if module == 0:
            module = 99999999
        return Vector(self.__x / float(module), self.__y / float(module))

    def __getitem__(self, item: int) -> float:
        return (self.x, self.y)[item]

    def __hash__(self):
        return hash((self.x, self.y))

    def get_comps(self, f=True):
        # TODO hacer que si se construye con valores enteros siempre devuelva valores enteros
        # TODO hacer que si se construye con valores float siempre devuelva valores float
        """
        Returns a tuple with the vector components
        Float by default, integer when f=False
        :param f: bool
        :return: tuple with the vector components
        """
        if f:
            return self.__x, self.__y
        return int(self.__x), int(self.__y)

    def set_comp(self, comp, value):
        """
        A function se set component value via numerical index
        0 = x
        1 = y
        """
        if comp == 0:
            self.__x = value
        else:
            self.__y = value

    def __neg__(self) -> "Vector":
        """ unary minus overridden """
        return Vector(-self.__x, -self.__y)

    def __call__(self, comp=None):
        # FIXME que esto sea sobrecargando []
        if comp is None:
            return self.get_comps()
        return self.get_comps()[comp]

    def __eq__(self, other: "Vector") -> bool:
        if other.x == self.__x and other.y == self.__y:
            return True
        return False

    def __iter__(self):
        return iter((self.x, self.y))

    def int(self) -> Tuple[int, int]:
        return int(self.__x), int(self.__y)

    def int_vector(self) -> "Vector":
        return Vector(round(self.__x, 0), round(self.__y, 0))

    def normal(self, unit=True) -> "Vector":
        if unit:
            return self.to_polar().normal().to_cartesian().unit()
        return self.to_polar().normal().to_cartesian()

    def angle_to(self, other: "Vector") -> float:
        angle = atan2(self.y - other.y, self.x - other.x)

        if angle < 0:
            angle = 2 * pi + angle

        as_deg = degrees(angle)

        as_deg -= 90
        if as_deg > 360:
            as_deg -= 360

        return as_deg


def round_vector(vector, decimal_places: int = 5):
    """ "
    Return a vector with its components rounded.
    It allow compare vectors ignoring precision errors due to how floats numbers are stored as binaries
    """
    return vector.__class__(*(round(attribute, decimal_places) for attribute in vector))


def angle(first: "Vector", second: "Vector" = Vector(1, 0)) -> float:
    """
    Returns the angle in radians between the two given vectors.
    If only one is give the return is the angle between this and the horizontal.
    """
    angles = [atan2(*reversed(first.get_comps())), atan2(*reversed(second.get_comps()))]
    for i in (0, 1):
        if angles[i] < 0:
            angles[i] = 2 * pi + angles[i]
    return max(angles) - min(angles)


def distance_point_line(point: "Vector", line: Tuple["Vector", "Vector"]) -> float:
    """ Returns the distance between a point and a line. The line is given by a tuple of points """
    # TODO hacer que los puntos puedan ser polares
    p1, p2 = line
    return abs(
        (p2.y - p1.y) * point.x - (p2.x - p1.x) * point.y + p2.x * p1.y - p2.y * p1.x
    ) / abs(p1 - p2)


def distance_point_segment(point: "Vector", line: Tuple["Vector", "Vector"]) -> float:
    b = abs(line[0] - line[1])
    angles = [0, 0]
    for i in (0, 1):
        a = abs(point - line[i])
        if a == 0:
            return 0
        c = abs(point - line[i - 1])
        angles[i] = acos((a ** 2 + b ** 2 - c ** 2) / (2 * a * b))

    if sum([1 if a > pi / 2.0 else 0 for a in angles]):
        return min([abs(point - line[0]), abs(point - line[1])])
    else:
        return distance_point_line(point, line)


def length(vec: Vector):
    return sqrt(vec.x ** 2 + vec.y ** 2)


def distance(a: Vector, b: Vector) -> float:
    return sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2)


def is_angle_between(target: float, angle1: float, angle2: float) -> bool:
    rAngle = ((angle2 - angle1) % 360 + 360) % 360
    if rAngle >= 180:
        angle1, angle2 = angle2, angle1

    if angle1 <= angle2:
        return target >= angle1 and target <= angle2
    else:
        return target >= angle1 or target <= angle2


def line_intersect(
    line1: Tuple["Vector", "Vector"], line2: Tuple["Vector", "Vector"]
) -> Vector:
    xdiff = Vector(line1[0].x - line1[1].x, line2[0].x - line2[1].x)
    ydiff = Vector(line1[0].y - line1[1].y, line2[0].y - line2[1].y)

    def det(a, b):
        return a.x * b.y - a.y * b.x

    div = det(xdiff, ydiff)
    if div == 0:
        raise Exception("lines do not intersect")

    d = Vector(det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return Vector(x, y)


if __name__ == "__main__":
    assert line_intersect(
        (Vector(-100, 0), Vector(100, 0)), (Vector(0, -100), Vector(0, 100))
    ) == Vector(0, 0)
    print("Full pass")