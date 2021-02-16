import sys
sys.path.append('/app/controllers/')
sys.path.append('.')
# rcj_soccer_player controller - ROBOT Y1

###### REQUIRED in order to import files from B1 controller
import sys
from pathlib import Path
from time import time

sys.path.append(str(Path(".").absolute().parent))
from team_007_libraries.robot1.europa.goalie import Goalie


class MyRobot(Goalie):
    def __init__(self):
        super().__init__()


my_robot = MyRobot()
my_robot.run()
