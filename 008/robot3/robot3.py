import sys
from pathlib import Path
sys.path.append(str(Path('.').absolute().parent))
sys.path.append('/app/controllers')

from team_008_libraries.robot1 import helveticrobot

my_robot = helveticrobot.Helveticrobot()
my_robot.run()
