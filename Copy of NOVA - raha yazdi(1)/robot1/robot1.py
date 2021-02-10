# rcj_soccer_player controller - ROBOT B1

# Feel free to import built-in libraries
import math


from rcj_soccer_robot import RCJSoccerRobot, TIME_STEP
import utils

class empty():
    pass
class MyRobot(RCJSoccerRobot):
    def run(self):
        flag=0
        while self.robot.step(TIME_STEP) != -1:
            if self.is_new_data():
                data = self.get_new_data()

                
                robot_pos = data[self.name]
                
                if robot_pos['x']>0 and flag==0:
                    goal = empty()
                    goal.x = -0.8
                    goal.y = 0
                    flag=1
                if robot_pos['x']<0 and flag==0:
                    goal = empty()
                    goal.x = 0.8
                    goal.y = 0
                    flag=1 
                
                    
                
                ball_pos = data['ball']
                
               

                kick = empty()
                kick.x = 0
                kick.y = 0
                kick.radius = 0.13

                ball = empty()
                ball.x = ball_pos['x']
                ball.y = ball_pos['y']

                robot = empty()
                robot.x = robot_pos['x']
                robot.y = robot_pos['y']
                bigger_length = math.sqrt(
                    ((goal.y-ball.y) ** 2) + ((goal.x-ball.x) ** 2))
                
                
                offsetX=((kick.radius) * (goal.x-ball.x))/bigger_length
                offsetY=((kick.radius) * (goal.y-ball.y))/bigger_length
                
                kick.x = ball.x - offsetX
                kick.y = ball.y - offsetY
                
                

                
                error_dist =  math.sqrt(((kick.y-robot.y) ** 2) + ((kick.x-robot.x) ** 2))
                a_num = (kick.y - ball.y)/(kick.x-ball.x)
                b_num = kick.y - a_num * kick.x

                
                error_line = abs(a_num * robot.x +b_num -robot.y)/math.sqrt(a_num **2 +1)
                
                if(error_dist < 0.1):
                    
                    
                    kick_angle, robot_angle = self.get_angles(ball_pos, robot_pos)
    
                    
                    direction = utils.get_direction(kick_angle)
                
                else:
                
                    kick_pos={'x':kick.x,'y':kick.y}
                    kick_angle, robot_angle = self.get_angles(kick_pos, robot_pos)
    
                    
                    direction = utils.get_direction(kick_angle)
                
                

              
                if direction == 0:
                    left_speed = -10
                    right_speed = -10
                else:
                    left_speed = direction * 6
                    right_speed = direction * -6

                
                self.left_motor.setVelocity(left_speed)
                self.right_motor.setVelocity(right_speed)


my_robot = MyRobot()
my_robot.run()
