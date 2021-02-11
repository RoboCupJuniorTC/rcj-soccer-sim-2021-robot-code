# rcj_soccer_player controller - ROBOT B3

###### REQUIRED in order to import files from B1 controller
import sys
from pathlib import Path
sys.path.append(str(Path('.').absolute().parent))

from robot1 import rcj_soccer_robot, utils
######


import math
class empty():
    pass

class MyRobot(rcj_soccer_robot.RCJSoccerRobot):
    def run(self):
        flag=0
        while self.robot.step(rcj_soccer_robot.TIME_STEP) != -1:
            if self.is_new_data():
                data = self.get_new_data()

                
                robot_pos = data[self.name]
                
                if robot_pos['x']>0 and flag==0:
                    goal = empty()
                    goal.x = -0.8
                    goal.y = 0
                    side=1
                    flag=1
                if robot_pos['x']<0 and flag==0:
                    goal = empty()
                    goal.x = 0.8
                    goal.y = 0
                    side=-1
                    flag=1
                ball_pos = data['ball']

               
                ball_angle, robot_angle = self.get_angles(ball_pos, robot_pos)

                
                direction = utils.get_direction(ball_angle)
                ball_distance=  math.sqrt((((ball_pos['y'] - robot_pos['y']) ** 2) +((ball_pos['x'] - robot_pos['x']) ** 2)))
                ball_goal_dis=  math.sqrt(((ball_pos['x'] + 0.8) ** 2))
                robot_goal_dis= math.sqrt(((robot_pos['x'] - (-1*goal.x)) ** 2))  
                if robot_goal_dis>=ball_goal_dis:
                    head=0
                else: 
                    head=1   
                
                if side==-1:
                    if(robot_goal_dis <= 0.3):
                        if((robot_angle * 57.3) > 358 or (robot_angle * 57.3)  < 2):
                            if  ball_angle > 90 and ball_angle < 270 :
                                 left_speed = 10
                                 right_speed = 10
                            else:
                                 left_speed = - 10
                                 right_speed = -10
                            
                            
                        elif ((robot_angle * 57.3)<= 358 and (robot_angle * 57.3) >= 180):
                           
                            left_speed = (robot_angle) * 0.2
                            right_speed = (robot_angle) * -0.2
                           
                        elif ((robot_angle * 57.3)>= 5 and (robot_angle * 57.3) < 180):
                           
                            left_speed = (robot_angle) * -2
                            right_speed = (robot_angle) * 2         
                 
                    elif(robot_goal_dis > 0.3):
        
                        if((robot_angle * 57.3) < 88 ):
                            if (abs(90-(robot_angle*57.3)) <90):
                                left_speed = (robot_angle) * 2
                                right_speed = (robot_angle) *- 2
                            else:
                                left_speed =10
                                right_speed = -10 
                              
                        elif ( (robot_angle * 57.3) > 92 ):
                            left_speed = (robot_angle) *-2
                            right_speed = (robot_angle) *2 
                            print(' in 4 ')  
                        else:
                            left_speed = 10
                            right_speed = 10
                             
                else :
                    if(robot_goal_dis <= 0.3):
                        if((robot_angle * 57.3) > 358 or (robot_angle * 57.3)  < 2):
                            if  ball_angle > 90 and ball_angle < 270 :
                                 left_speed = 10
                                 right_speed = 10
                            else:
                                 left_speed = -10
                                 right_speed = -10
                            
                            
                        elif ((robot_angle * 57.3)<= 358 and (robot_angle * 57.3) >= 180):
                           
                            left_speed = (robot_angle) * 0.2
                            right_speed = (robot_angle) * -0.2
                           
                        elif ((robot_angle * 57.3)>= 5 and (robot_angle * 57.3) < 180):
                           
                            left_speed = (robot_angle) * -3
                            right_speed = (robot_angle) * 3
                            
             
                 
                    elif(robot_goal_dis > 0.3):
        
                        if((robot_angle * 57.3) < 268 ):
                            if (abs(270-(robot_angle*57.3)) <90):
                                left_speed = (robot_angle) * 0.2
                                right_speed = (robot_angle) * -0.2
                            else:
                                left_speed = 10
                                right_speed = -10  
                              
                        elif ( (robot_angle * 57.3) > 272 ):
                            left_speed = (robot_angle) * -0.2
                            right_speed = (robot_angle) * 0.2 
                              
                        else:
                            left_speed = 10
                            right_speed = 10
                            
                       
                
                self.left_motor.setVelocity(left_speed)
                self.right_motor.setVelocity(right_speed)


my_robot = MyRobot()
my_robot.run()
