import sys
from pathlib import Path
sys.path.append(str(Path('.').absolute().parent))
sys.path.append('/app/controllers')

# rcj_soccer_player controller - ROBOT B1

# Feel free to import built-in libraries
import math

# You can also import scripts that you put into the folder with controller
from team_009_libraries.robot1.rcj_soccer_robot import RCJSoccerRobot, TIME_STEP
from team_009_libraries.robot1 import utils

class MyRobot(RCJSoccerRobot):
    
    def run(self):
        
        def normalize(vector):
            mag = math.sqrt(vector['x']**2 + vector['y']**2)
            return {'x':vector['x']/mag,'y':vector['y']/mag}
        
        def to_point(robot_pos, point, chase):
            point_angle, _ = self.get_angles(point, robot_pos)
            
            direction = utils.get_direction(point_angle)
            
            if direction == 0:
                left_speed = -10
                right_speed = -10
            else:
                left_speed = (direction * 10) - chase*10
                right_speed = (direction * -10) - chase*10
            
            if left_speed > 10:
                left_speed = 10
            if left_speed < -10:
                left_speed = -10
                
            if right_speed > 10:
                right_speed = 10
            if right_speed < -10:
                right_speed = -10
            
            return left_speed, right_speed
        
        def to_angle(robot_pos, point):
            done = False
            point_angle, _ = self.get_angles(point, robot_pos)
            
            direction = utils.get_direction(point_angle)
            
            if direction == 0:
                left_speed = 0
                right_speed = 0
                done = True
            else:
                left_speed = direction * 10
                right_speed = direction * -10
                
            return left_speed, right_speed, done
        
        state = 0
        if self.name[0] == "Y":
            home = {'x':-0.5,'y':0.0}
        else:
            home = {'x':0.5,'y':0.0}
        
        time = 0
        
        ball_pos = {'x':0.0,'y':0.0}
        ball_v = {'x':0.0,'y':0.0}
        
        while self.robot.step(TIME_STEP) != -1:
            if self.is_new_data():
                data = self.get_new_data()
 
                # Get the position of our robot
                # max robot velocity = 0.0064
                robot_pos = data[self.name]
                # Get the position of the ball
                ball_v = {'x':data['ball']['x']-ball_pos['x'],'y':data['ball']['y']-ball_pos['y']}
                ball_pos = data['ball']
                
                """
                # Get angle between the robot and the ball
                # and between the robot and the north
                ball_angle, robot_angle = self.get_angles(ball_pos, robot_pos)

                # Compute the speed for motors
                direction = utils.get_direction(ball_angle)

                # If the robot has the ball right in front of it, go forward,
                # rotate otherwise
                if direction == 0:
                    left_speed = -5
                    right_speed = -5
                else:
                    left_speed = direction * 4
                    right_speed = direction * -4
                """
                
                angle = -math.pi/2
                
                # go to point
                if state==0:
                    left_speed, right_speed = to_point(robot_pos, home, 0)
                    if math.sqrt(math.pow(robot_pos['x']-home['x'],2)+math.pow(robot_pos['y']-home['y'],2)) <= 0.01:
                        state = 1
                        
                # turn forward
                elif state==1:
                    point = {'x' : robot_pos['x']+math.cos(angle), 'y' :  robot_pos['y']-0.01-math.sin(angle)}
                    left_speed, right_speed, done = to_angle(robot_pos, point)
                    if done:
                        state = 2
                        
                # go to ball's position 1s before it gets there
                elif state==2:
                    time += 1
                    if robot_pos['y'] > ball_pos['y']:
                        left_speed = 10
                        right_speed = 10
                    if robot_pos['y'] < ball_pos['y']:
                        left_speed = -10
                        right_speed = -10
                    
                    if time > 300:
                        time = 0
                        state = 0
                
                # Set the speed to motors
                self.left_motor.setVelocity(left_speed)
                self.right_motor.setVelocity(right_speed)


my_robot = MyRobot()
my_robot.run()
