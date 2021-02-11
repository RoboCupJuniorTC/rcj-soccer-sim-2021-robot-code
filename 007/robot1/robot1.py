# rcj_soccer_player controller - ROBOT Y1

###### REQUIRED in order to import files from B1 controller
import sys
from pathlib import Path
from time import time

sys.path.append(str(Path(".").absolute().parent))
from robot1.europa.goalie import Goalie


class MyRobot(Goalie):
    def __init__(self):
        super(MyRobot, self).__init__(blue=self.team.startswith("B"))


my_robot = MyRobot()
my_robot.run()
