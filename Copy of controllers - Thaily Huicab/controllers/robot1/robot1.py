# rcj_soccer_player controller - ROBOT B1

# Feel free to import built-in libraries
import math

# You can also import scripts that you put into the folder with controller
from rcj_soccer_robot import RCJSoccerRobot, TIME_STEP
import utils

#azul pos R1
# 
# 

class MyRobot(RCJSoccerRobot):
    def run(self):
        while self.robot.step(TIME_STEP) != -1:
            if self.is_new_data():
                data = self.get_new_data()
              
                robot_pos = data[self.name]
                
                if self.name == 'B1'or self.name == 'B2' or self.name == 'B3':
                    print('Equipo Azul' )
                    robot_pos1 = data['B1']
                    robot_pos2 = data['B2']
                    robot_pos3 = data['B3']
                    
                    Neu_posx = 0.43
                    Neu_posy = -0.006
                else:
                    print('Equipo Amarillo' )
                    
                    robot_pos1 = data['Y1']
                    robot_pos2 = data['Y2']
                    robot_pos3 = data['Y3']
                    Neu_posx = -0.43
                    Neu_posy = 0.006
                # Get the position of the ball
                ball_pos = data['ball']

                # Get angle between the robot and the ball
                # and between the robot and the north
                ball_angle, robot_angle = self.get_angles(ball_pos, robot_pos)
                
                # Compute the speed for motors
                if ball_angle < 0:
                    ball_angle += 360
                direction = utils.get_direction(ball_angle)
               
                dist1=  math.sqrt((ball_pos['y'] - robot_pos['y'])*(ball_pos['y'] - robot_pos['y'])+(ball_pos['x'] - robot_pos['x'])*(ball_pos['x'] - robot_pos['x']))
                dist2=  math.sqrt((ball_pos['y'] - robot_pos['y'])*(ball_pos['y'] - robot_pos['y'])+(ball_pos['x'] - robot_pos['x'])*(ball_pos['x'] - robot_pos['x']))
                dist3=  math.sqrt((ball_pos['y'] - robot_pos['y'])*(ball_pos['y'] - robot_pos['y'])+(ball_pos['x'] - robot_pos['x'])*(ball_pos['x'] - robot_pos['x']))
                
                if dist1<dist2 and dist1<dist3:
                    pelotita=1
                elif dist2<dist1 and dist2<dist3:
                    pelotita=2
                elif dist3<dist1 and dist3<dist2:
                    pelotita=3
                else:
                    pelotita=1
                # If the robot has the ball right in front of it, go forward,
                # rotate otherwise
                
                #nearball = utils.get_nearball()
                #print('La pelota1 la tiene', nearball)
                
                if pelotita == 1 and dist1<.52: 
                    if direction == 0: 
                        diff=ball_angle
                        if diff > 180:
                            diff=diff-360
                            left_speed2 = -10-(diff*.6)
                            right_speed2 = -10
                            left_speed= left_speed2
                            right_speed =right_speed2
                            #print('dist1:', dist1, 'left_speed2:', left_speed2, 'right_speed2 :', right_speed2 )
    
                        else:
                            left_speed2 = -10
                            right_speed2 = -10+(diff*.6)
                            left_speed= left_speed2
                            right_speed =right_speed2
                            #print('dist1:', dist1,'ball_angle', ball_angle, 'left_speed2:', left_speed2, 'right_speed2 :', right_speed2 )
    
                    else:
                        left_speed = direction * 10
                        right_speed = direction * -10
                else:                     
                     NeuZone_angle = self.get_NZangles(robot_pos, Neu_posx, Neu_posy)
                     direction2 = utils.get_direction(NeuZone_angle)
                    #print('zona neutra', 'NeuAngle:', NeuZone_angle,'dir2:', direction2)
                     if direction2 == 0: 
                          left_speed= -10
                          right_speed =-10
                     else:                           
                          left_speed= direction2*10
                          right_speed =direction2*-10

                # Set the speed to motors
                self.left_motor.setVelocity(left_speed)
                self.right_motor.setVelocity(right_speed)


my_robot = MyRobot()
my_robot.run()