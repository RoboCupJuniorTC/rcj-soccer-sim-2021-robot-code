import sys
from pathlib import Path
sys.path.append(str(Path('.').absolute().parent))
sys.path.append('/app/controllers')

import math

from team_029_libraries.robot1.rcj_soccer_robot import RCJSoccerRobot, TIME_STEP
from team_029_libraries.robot1 import utils
x=0
rangodist=.25
class MyRobot(RCJSoccerRobot):
    
    def run(self):
        while self.robot.step(TIME_STEP) != -1:
            if self.is_new_data():
                data = self.get_new_data()
                robot_pos = data[self.name] 
                                                              
                
                global x
                if x == 0:
                    x=x+1
                    if self.name == 'B1'or self.name == 'B2' or self.name == 'B3':
                        
                        team=0
                        robot_pos1 = data['B1']
                        robot_pos2 = data['B2']
                        robot_pos3 = data['B3'] 
                        Neu_posx = 0.54
                        Neu_posy = 0      
                    else:
                        team=1
                        robot_pos1 = data['Y1']
                        robot_pos2 = data['Y2']
                        robot_pos3 = data['Y3']
                        Neu_posx = -0.54
                        Neu_posy = 0           
                ball_pos = data['ball']
                
                ball_angle, robot_angle = self.get_angles(ball_pos, robot_pos)
                
                if ball_angle < 0:
                    ball_angle += 360
                direction = utils.get_direction(ball_angle)
                
                dist1=  math.sqrt((ball_pos['y'] - robot_pos1['y'])*(ball_pos['y'] - robot_pos1['y'])+(ball_pos['x'] - robot_pos1['x'])*(ball_pos['x'] - robot_pos1['x']))
              
                if dist1<rangodist:
                    if direction == 0: 
                        diff=ball_angle
                        if diff > 180:
                            diff=diff-360
                            left_speed2 = -10-(diff*.6)
                            right_speed2 = -10
                            left_speed= left_speed2
                            right_speed =right_speed2
                            
                        else:
                            left_speed2 = -10
                            right_speed2 = -10+(diff*.6)
                            left_speed= left_speed2
                            right_speed =right_speed2
                           
                    else:
                        left_speed = direction * 10
                        right_speed = direction * -10
                else:
                     if team == 0:
                         if ball_pos['x']<.47:
                             Neu_posx= .54
                         else:
                             Neu_posx= .67
                             
                         if ball_pos['y']>-.3 and ball_pos['y']<.3:
                             Neu_posy=ball_pos['y']
                         elif ball_pos['y']>.3:
                             Neu_posy=.3
                         else:
                             Neu_posy=-.3
                     else:
                         if ball_pos['x']>-.47:
                             Neu_posx= -.54
                         else:
                             Neu_posx= -.67
                             
                         if ball_pos['y']>-.3 and ball_pos['y']<.3:
                             Neu_posy=ball_pos['y']
                         elif ball_pos['y']>.3:
                             Neu_posy=.3
                         else:
                             Neu_posy=-.3
                     NeuZone_angle = self.get_NZangles(robot_pos, Neu_posx, Neu_posy)
                     direction2 = utils.get_direction(NeuZone_angle)
                     if direction2 == 0: 
                          left_speed= -10
                          right_speed =-10
                     else:                           
                          left_speed= direction2*10
                          right_speed =direction2*-10

                self.left_motor.setVelocity(left_speed)
                self.right_motor.setVelocity(right_speed)
                

my_robot = MyRobot()
my_robot.run()
