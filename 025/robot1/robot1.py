import sys
from pathlib import Path
sys.path.append(str(Path('.').absolute().parent))
sys.path.append('/app/controllers')

# rcj_soccer_player controller - ROBOT B1

import math
import time

from team_025_libraries.robot1.SoccerRobot import SoccerRobot
from team_025_libraries.robot1 import Utils

from team_025_libraries.robot1.Consts import BLUEGOAL, YELLOWGOAL, TIMESTEP, BLUEPENALTYAREA, GKATTACKSPOT, GKDEFENSESPOT


class Goalkeeper(SoccerRobot):
    def OnStart(self):
        #print("Starting Robot")
        self.GKATTACKSPOT = GKATTACKSPOT
        if self.name.startswith('Y'):
            self.GKATTACKSPOT *= -1
        
        self.GKDEFENSESPOT = GKDEFENSESPOT
        if self.name.startswith('Y'):
            self.GKDEFENSESPOT *= -1

    def OnUpdate(self):
        #time.sleep(0.05)
        self.UpdatePositionData()

        #print(Utils.GetDisplacement(self.position, self.gameData.GetPosition("ball")))
        #print(self.lackOfProgressTimer.timeToLackOfProgress)

        #Anti Lack Of Progress
        if self.lackOfProgressTimer.timeToLackOfProgress < 8:
            self.GoToPosition(self.gameData.GetPosition("ball"), 10)
            return


        if self.gameData.GetGameState() == "attack":
            #Be prepered in front of own panalty area
            if not self.GoToPosition(Utils.Vector2(self.GKATTACKSPOT.x, Utils.Clamp(self.gameData.GetPosition("ball").y, -0.3, 0.3)), 10):
                self.RotateTo(Utils.GetAngleBetweenVector2(self.position, self.gameData.GetPosition("ball")), 6)
    
        if self.gameData.GetGameState() == "middefense":
            #Wait in place whera can be a ball
            if not self.GoToPosition(Utils.Vector2(self.GKATTACKSPOT.x, Utils.Clamp(self.gameData.GetPosition("ball").y, -0.3, 0.3)), 10):
                self.RotateTo(Utils.GetAngleBetweenVector2(self.position, self.gameData.GetPosition("ball")), 6)
            #If ball is close to GK and also it is in front of kick a ball out
            if Utils.GetDisplacement(self.position, self.gameData.GetPosition("ball")) < 0.3 and self.gameData.GetPosition("ball").x < self.position.x:
                self.GoToPosition(self.gameData.GetPosition("ball"), 10)

        if self.gameData.GetGameState() == "defense":
            self.GoToPosition(Utils.Vector2(self.GKDEFENSESPOT.x, self.gameData.GetPosition("ball").y), 10)


    def __GoToShootPosition(self):
        pass



    def __GoalKeeping(self):
        if abs(BLUEGOAL.x - self.position.x) >= 0.03:
            self.GoToPosition(BLUEGOAL, 10)
        elif abs(self.rotation - 90) >= 15:
            self.RotateTo(90, 5)
        else:
            if self.position.y - self.positionData["ball"]["y"] < 0:
                if not self.RotateTo(90, 5):
                    self.GoForward(-10)
            elif self.position.y - self.positionData["ball"]["y"] > 0:
                if not self.RotateTo(90, 5):
                    self.GoForward(10)


        
Stiker = Goalkeeper()

Stiker.OnStart()

while Stiker.robot.step(TIMESTEP) != -1:
    Stiker.OnUpdate()
