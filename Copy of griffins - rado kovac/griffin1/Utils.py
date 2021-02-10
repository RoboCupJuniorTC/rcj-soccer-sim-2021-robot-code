import math

from controller import Robot

def ProcessDataOrientation(orientation):
    # Set rotation to be in degrees and to be 0 when facing North
    rotation = math.degrees(RadiansOrientationToRotation(orientation)) + 90
    if rotation > 360:
        rotation -= 360
    return 360 - rotation     

def RadiansOrientationToRotation(orientation):
    if orientation < 0:
        return orientation + 2 * math.pi
    else:
        return orientation

def DegreesOrientationToRotation(orientation):
    if orientation < 0:
        return orientation + 360
    else:
        return orientation

def Clamp(value, min_value, max_value):
    return max(min(value, max_value), min_value)

class Vector2:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return "({0}, {1})".format(self.x, self.y)


    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Vector2(x, y)

    def __sub__(self, other):
        x = self.x - other.x
        y = self.y - other.y
        return Vector2(x, y)
    
    def __mul__(self, other):
        x = self.x * other.x
        y = self.y * other.y
        return Vector2(x, y)

    def __mul__(self, other: float):
        x = self.x * other
        y = self.y * other
        return Vector2(x, y)

def GetDisplacement(firstVector2: Vector2, secondVector2: Vector2) -> float:
    vectorDiffrence = firstVector2 - secondVector2
    return math.hypot(vectorDiffrence.x, vectorDiffrence.y)

def GetAngleBetweenVector2(firstVector2: Vector2, secondVector2: Vector2) -> float:
    positionDifference = firstVector2 - secondVector2
    return DegreesOrientationToRotation(math.degrees(math.atan2(positionDifference.y, positionDifference.x)))

class Timer:
    def __init__(self, robot: Robot) -> None:
        self.__startTime = 0
        self.__robot = robot
        self.ResetTimer()

    def ResetTimer(self) -> None:
        self.time = 0
        self.__startTime = self.__robot.getTime()

    def GetTime(self) -> float:
        return self.__robot.getTime() - self.__startTime

class LackOfProgressCounter:
    def __init__(self, robot: Robot, lackOfProgressTime: float, position: Vector2, treshhold: float) -> None:
        self.__timer = Timer(robot)
        self.__timer.ResetTimer()

        self.timeToLackOfProgress = lackOfProgressTime
        self.__lackOfProgressTime = lackOfProgressTime
        self.__treshhold = treshhold
        self.__position = position

    def Update(self, position: Vector2):
        if GetDisplacement(self.__position, position) > self.__treshhold:
            self.timeToLackOfProgress = self.__lackOfProgressTime
            self.__position = position
            self.__timer.ResetTimer()
            return
        else:
            self.timeToLackOfProgress = self.__lackOfProgressTime - self.__timer.GetTime()

        #print("Debug: " + str(self.__position) + "         " + str(position) + "         " + str(GetDisplacement(self.__position, position)))

