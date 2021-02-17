import sys
from pathlib import Path
sys.path.append(str(Path('.').absolute().parent))
sys.path.append('/app/controllers')

# rcj_soccer_player controller - ROBOT B1

# Feel free to import built-in libraries
import math

# You can also import scripts that you put into the folder with controller
from team_008_libraries.robot1.rcj_soccer_robot import RCJSoccerRobot, TIME_STEP
from team_008_libraries.robot1 import helveticrobot
from team_008_libraries.robot1 import utils

my_robot = helveticrobot.Helveticrobot()
my_robot.run()
