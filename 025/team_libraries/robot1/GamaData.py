import time

from controller import Robot

from team_025_libraries.robot1.DataReceiver import DataReceiver
from team_025_libraries.robot1 import Utils

from team_025_libraries.robot1.Consts import BLUEGOAL, YELLOWGOAL, GKATTACKSPOT

class GameData():
    def __init__(self, robot: Robot, timestep: int):
        self.__dataReceiver: DataReceiver = DataReceiver(robot, timestep)

        if robot.getName().startswith('B'):
            self.__currentTeam: str = "blue"
        else:
            self.__currentTeam: str = "yellow"

        self.__positionData = self.__GetDefaultPositionData()

    def GetPosition(self, object: str) -> Utils.Vector2:
        return Utils.Vector2(self.__positionData[object]["x"], self.__positionData[object]["y"])

    def GetRotation(self, object: str) -> float:
        return self.__positionData[object]["orientation"]

    def GetGameState(self) -> str:
        if self.__currentTeam == "blue":
            if self.GetPosition("ball").x > 0.5:
                return "defense"
            elif self.GetPosition("ball").x > 0.3 and self.GetPosition("ball").x < 0.5:
                return "middefense"
            else:
                return "attack"

        if self.__currentTeam == "yellow":
            if self.GetPosition("ball").x < -0.5:
                return "defense"
            elif self.GetPosition("ball").x < -0.3 and self.GetPosition("ball").x > -0.5:
                return "middefense"
            else:
                return "attack"

    def GetClosestPlayerToGoal(self) -> str:
        if self.__currentTeam == "blue":
            if (self.GetPosition("B1").x > self.GetPosition("B2").x) and (self.GetPosition("B1").x > self.GetPosition("B3").x):
                return "B1"
            elif (self.GetPosition("B2").x > self.GetPosition("B1").x) and (self.GetPosition("B2").x > self.GetPosition("B3").x):
                return "B2"
            else:
                return "B3"

        if self.__currentTeam == "yellow":
            if (self.GetPosition("Y1").x > self.GetPosition("Y2").x) and (self.GetPosition("Y1").x > self.GetPosition("Y3").x):
                return "Y1"
            elif (self.GetPosition("Y2").x > self.GetPosition("Y1").x) and (self.GetPosition("Y2").x > self.GetPosition("Y3").x):
                return "Y2"
            else:
                return "Y3"

    def GetClosestPlayerToBall(self) -> str:
        if self.__currentTeam == "blue":
            B1BallDisplacement = Utils.GetDisplacement(self.GetPosition("B1"), self.GetPosition("ball"))
            B2BallDisplacement = Utils.GetDisplacement(self.GetPosition("B2"), self.GetPosition("ball"))
            B3BallDisplacement = Utils.GetDisplacement(self.GetPosition("B3"), self.GetPosition("ball"))
            
            if (B1BallDisplacement < B2BallDisplacement) and (B1BallDisplacement < B3BallDisplacement):
                return "B1"
            elif (B2BallDisplacement < B1BallDisplacement) and (B2BallDisplacement < B3BallDisplacement):
                return "B2"
            else:
                return "B3"

        elif self.__currentTeam == "yellow":
            Y1BallDisplacement = Utils.GetDisplacement(self.GetPosition("Y1"), self.GetPosition("ball"))
            Y2BallDisplacement = Utils.GetDisplacement(self.GetPosition("Y2"), self.GetPosition("ball"))
            Y3BallDisplacement = Utils.GetDisplacement(self.GetPosition("Y3"), self.GetPosition("ball"))
            
            if (Y1BallDisplacement < Y2BallDisplacement) and (Y1BallDisplacement < Y3BallDisplacement):
                return "Y1"
            elif (Y2BallDisplacement < Y1BallDisplacement) and (Y2BallDisplacement < Y3BallDisplacement):
                return "Y2"
            else:
                return "Y3"

              

    def UpdatePositionData(self):
        if self.__dataReceiver.IsNewData():
            self.__positionData = self.__dataReceiver.GetNewData()


    def __GetDefaultPositionData(self) -> dict:
        positionData = {
            "B1": {"x": 0.0, "y": 0.0, "orientation": 0},
            "B2": {"x": 0.0, "y": 0.0, "orientation": 0},
            "B3": {"x": 0.0, "y": 0.0, "orientation": 0},

            "Y1": {"x": 0.0, "y": 0.0, "orientation": 0},
            "Y2": {"x": 0.0, "y": 0.0, "orientation": 0},
            "Y3": {"x": 0.0, "y": 0.0, "orientation": 0},

            "ball": {"x": 0.0, "y": 0.0, "orientation": 0}
        }

        return positionData
