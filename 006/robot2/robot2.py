import sys
from pathlib import Path
sys.path.append(str(Path('.').absolute().parent))
sys.path.append('/app/controllers')

# rcj_soccer_player controller - ROBOT B3

###### REQUIRED in order to import files from B1 controller
import sys
from pathlib import Path
sys.path.append(str(Path('.').absolute().parent))
# You can now import scripts that you put into the folder with your
# robot B1 controller
from team_006_libraries.robot1 import rcj_soccer_robot, utils
######

# Feel free to import built-in libraries
import math
ballposB = -0.01
ballposY = 0.01
tor_posB = {'y': 0.0, 'x': -0.75}
tor_posY = {'y': 0.0, 'x': 0.75}
x = 0

class MyRobot(rcj_soccer_robot.RCJSoccerRobot):
    def run(self):
        team = self.team
        while self.robot.step(rcj_soccer_robot.TIME_STEP) != -1:
            if self.is_new_data():
                data = self.get_new_data()
                left_speed = 0
                right_speed = 0
                # Get the position of our robot
                robot_pos = data[self.name]
                # Get the position of the ball
                if team == 'B':
                    tor_pos = tor_posB
                    ballpos = ballposB

                    ball_pos = data['ball']
                    x = (ball_pos['x'] - robot_pos['x'])
                    tor_pos = {'y': 0.0, 'x': -0.75}
                    # Get angle between the robot and the ball
                    # and between the robot and the north
                    ball_angle, robot_angle = self.get_angles(ball_pos, robot_pos)
                    robot_ori = data[self.name]['orientation']
                
                    direction = utils.get_direction(ball_angle)
                    print ('Rotation',robot_ori) 
                    #print ('BALL' ,ball_pos) 
                    Sperrzone = 0
                    sCheck = 0
                
                    if ball_pos['y'] <= -0.01:
                        sCheck = 5
                
                
                
                    if ball_pos['y'] >= 0.01:
                        sCheck = 3
                
                    if x < 0:
                        x = x - 9.0
                
                    if x > 0:
                        x = x + 9.0
                
                    if direction == 0 and sCheck == 5:
                        left_speed = -10
                        right_speed = -10
                        #print ('Push')
                    
                    if direction != 0 and sCheck == 5:
                        left_speed = direction * 10
                        right_speed = direction * -10
                        # print ('Push_Search') 
                    
                    if sCheck == 3 and robot_ori <= -1.4 and robot_ori >= -1.7:
                        left_speed = x
                        right_speed = x 
                    
                    # print ('Follow')
                        
                    if sCheck == 3 and robot_ori >= -1.4 or robot_ori <= -1.7:
                        left_speed = 3
                        right_speed = -3
                    # print ('Follow_Search')
                     
                    if direction == 0 and ball_pos['y'] <= 0.1 and ball_pos['y'] >= -0.1 and ball_pos['x'] <= 0.1 and ball_pos['x'] >= -0.1:
                        left_speed = -10
                        right_speed = -10 
                        print ('Mid_Go')
                    
                    if direction != 0 and ball_pos['y'] <= 0.1 and ball_pos['y'] >= -0.1 and ball_pos['x'] <= 0.1 and ball_pos['x'] >= -0.1:
                        left_speed = direction * 10
                        right_speed = direction * -10
                        print ('Mid_Search')
                        
                    if robot_pos['x'] >= 0.45 and ball_pos['x'] >= 0.45:
                        Sperrzone = 1 
                    # print ('Danger_Home')
                     
                    if robot_pos['x'] <= -0.55 and ball_pos['y'] >= 0.1 and ball_pos['x'] <= -0.55:
                        Sperrzone = 2    
                    # print ('danger_Away')
                    
                    if Sperrzone == 1: 
                        left_speed = direction * 10
                        right_speed = direction * -10  
                    # print ('Zone_Home')
                    
                    if Sperrzone == 2: 
                        left_speed = direction * 10
                        right_speed = direction * -10
                        #print ('Zone_Away')      
                
                    # Set the speed to motors
                    self.left_motor.setVelocity(left_speed)
                    self.right_motor.setVelocity(right_speed)

                if team == 'Y':
                    tor_pos = tor_posY
                    ballpos = ballposY

                ball_pos = data['ball']
                x = (ball_pos['x'] - robot_pos['x'])
                tor_pos = {'y': 0.0, 'x': -0.75}
                # Get angle between the robot and the ball
                # and between the robot and the north
                ball_angle, robot_angle = self.get_angles(ball_pos, robot_pos)
                robot_ori = data[self.name]['orientation']
                
                direction = utils.get_direction(ball_angle)
                print ('Rotation',robot_ori) 
                #print ('BALL' ,ball_pos) 
                Sperrzone = 0
                sCheck = 0
                
                if ball_pos['y'] <= -0.01:
                    sCheck = 5
                
                
                
                if ball_pos['y'] >= 0.01:
                    sCheck = 3
                
                if x < 0:
                    x = x - 9.0
                
                if x > 0:
                    x = x + 9.0
                
                if direction == 0 and sCheck == 5:
                    left_speed = -10
                    right_speed = -10
                    #print ('Push')
                    
                if direction != 0 and sCheck == 5:
                    left_speed = direction * 10
                    right_speed = direction * -10
                   # print ('Push_Search') 
                    
                if sCheck == 3 and robot_ori <= -1.4 and robot_ori >= -1.7:
                    left_speed = x
                    right_speed = x 
                    
                   # print ('Follow')
                        
                if sCheck == 3 and robot_ori >= -1.4 or robot_ori <= -1.7:
                    left_speed = 3
                    right_speed = -3
                   # print ('Follow_Search')
                     
                if direction == 0 and ball_pos['y'] <= 0.1 and ball_pos['y'] >= -0.1 and ball_pos['x'] <= 0.1 and ball_pos['x'] >= -0.1:
                    left_speed = -10
                    right_speed = -10 
                    print ('Mid_Go')
                    
                if direction != 0 and ball_pos['y'] <= 0.1 and ball_pos['y'] >= -0.1 and ball_pos['x'] <= 0.1 and ball_pos['x'] >= -0.1:
                    left_speed = direction * 10
                    right_speed = direction * -10
                    print ('Mid_Search')
                        
                if robot_pos['x'] >= 0.45 and ball_pos['x'] >= 0.45:
                    Sperrzone = 1 
                   # print ('Danger_Home')
                     
                if robot_pos['x'] <= -0.55 and ball_pos['y'] >= 0.1 and ball_pos['x'] <= -0.55:
                    Sperrzone = 2    
                   # print ('danger_Away')
                    
                if Sperrzone == 1: 
                    left_speed = direction * 10
                    right_speed = direction * -10  
                   # print ('Zone_Home')
                    
                if Sperrzone == 2: 
                    left_speed = direction * 10
                    right_speed = direction * -10
                    #print ('Zone_Away')      
                
                # Set the speed to motors
                self.left_motor.setVelocity(left_speed)
                self.right_motor.setVelocity(right_speed)


my_robot = MyRobot()
my_robot.run()
