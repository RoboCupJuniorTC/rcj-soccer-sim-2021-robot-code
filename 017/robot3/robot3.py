# rcj_soccer_player controller - ROBOT B3
#----------------------------------------------------------------- DO NOT CHANGE OR DELETE
import sys
from pathlib import Path
sys.path.append(str(Path('.').absolute().parent))

from team_017_libraries.robot1 import rcj_soccer_robot
#-----------------------------------------------------------------------------------------
#----------------------------------------------------------------IMPORT BUILT_IN LIBRARIES
# Feel free to import built-in libraries here

#----------------------------------------------------------------- DO NOT CHANGE OR DELETE
import math

OP_GOAL = [-0.856, 0] # Opponent's goal position [x, y]
OWN_GOAL = [0.856, 0] # Own's goal position [x, y]
contador = 0
pontuacao = [0, 0]
gol_ponto = False
band_time = False
band_import = False
dist_gol = 0.4
goal_time = 0
STOP_NEAR_GOALKEEPER = True
chut_band = 0
KICK_INTENSITY_DEFAULT = 5
MIRROR_FLAG = True
cont_band = False
area_bola = [0, 0, 0, 0]
INICIO = 0
#------------------------------------------------------------------------------------------

class MyRobot(rcj_soccer_robot.RCJSoccerRobot):
    def run(self, contador, pontuacao, goal_time, gol_ponto, band_time, band_import, chut_band, cont_band, area_bola, INICIO):
        # ----------------------------------------------------------------------------
        if not band_import:
            if self.name[0] == 'Y':
                from team_017_libraries.robot1 import my_functions
            else:
                from team_017_libraries.robot1 import my_functions
            band_import = True
        # ----------------------------------------------------------------------------   
        while self.robot.step(rcj_soccer_robot.TIME_STEP) != -1:
            if self.is_new_data():
                data = self.get_new_data()
                # ********************************************************************
                # Codigo stardust ***********************************************
                              
                chut_band = my_functions.stardust_artilheiro(self, data, STOP_NEAR_GOALKEEPER, chut_band, KICK_INTENSITY_DEFAULT)

                # ********************************************************************


my_robot = MyRobot()
my_robot.run(contador, pontuacao, goal_time, gol_ponto, band_time, band_import, chut_band, cont_band, area_bola, INICIO)
