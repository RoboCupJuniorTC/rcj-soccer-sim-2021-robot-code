import math

from controller import Robot

from .GamaData import GameData
from . import Utils

from .Consts import TIMESTEP

class SoccerRobot:
    def __init__(self) -> None:
        self.robot = Robot()
        self.name = self.robot.getName()
        self.team = self.name[0]
        self.playerID = int(self.name[1])

        self.gameData = GameData(self.robot, TIMESTEP)
        self.timer = Utils.Timer(self.robot)

        self.position: Utils.Vector2 = self.gameData.GetPosition(self.name)
        self.rotation = Utils.ProcessDataOrientation(self.gameData.GetRotation(self.name))

        self.lackOfProgressTimer = Utils.LackOfProgressCounter(self.robot, 15, self.position, 0.25)

        self.leftMotor = self.robot.getDevice("left wheel motor")
        self.rightMotor = self.robot.getDevice("right wheel motor")

        self.leftMotor.setPosition(float("+inf"))
        self.rightMotor.setPosition(float("+inf"))

        self.leftMotor.setVelocity(0.0)
        self.rightMotor.setVelocity(0.0)

    def GoToPosition(self, position: Utils.Vector2, speed) -> bool:
        # This function should be call in a loop
        # Returns True while moving

        positionDifference = self.position - position
        angle = Utils.GetAngleBetweenVector2(self.position, position)    

        if abs(positionDifference.x) >= 0.02 or abs(positionDifference.y) >= 0.02:
            if not (self.RotateTo(angle, speed)):
                self.GoForward(speed)
            return True
        else:
            self.StopMotors()
            return False


    def RotateTo(self, angle, speed) -> bool:
        # This function should be call in a loop
        # Returns True while rotating

        angleDifference = abs(self.rotation - angle)

        if not (angleDifference >= 345 or angleDifference <= 15):
            if self.rotation < angle:
                if abs(self.rotation - angle) <= 180:
                    self.Rotate(speed)
                else:
                    self.Rotate(-speed)
            else:
                if abs(self.rotation - angle) <= 180:
                    self.Rotate(-speed)
                else:
                    self.Rotate(speed)
            return True
        else:
            self.StopMotors()
            return False
            
    def GoForward(self, speed):
        self.SetMotorVelocity(speed, speed)

    def StopMotors(self):
        self.SetMotorVelocity(0, 0)

    def Rotate(self, speed):
        # Reversed Positive numbers to be clockwise
        self.SetMotorVelocity(speed, -speed)

    def SetMotorVelocity(self, leftMotor: float, rightMotor: float):
        # Reverse Forward to be positive numbers
        self.leftMotor.setVelocity(-leftMotor)
        self.rightMotor.setVelocity(-rightMotor)

    def UpdatePositionData(self):
        self.gameData.UpdatePositionData()
        self.position = self.gameData.GetPosition(self.name)
        self.rotation = Utils.ProcessDataOrientation(self.gameData.GetRotation(self.name))
        self.lackOfProgressTimer.Update(self.position)

    def OnStart(self):
        raise NotImplementedError

    def OnUpdate(self):
        raise NotImplementedError

