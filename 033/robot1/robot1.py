# rcj_soccer_player controller - ROBOT B1

# Feel free to import built-in libraries
import math

# You can also import scripts that you put into the folder with controller
from rcj_soccer_robot import RCJSoccerRobot, TIME_STEP
import utils
      
class MyRobot(RCJSoccerRobot):    
    def run(self):
        a = 0
        yo = 0
        yo2 = 0
        da = 0
        dyn = 0
        bstate = 0
        left_speed=0
        right_speed=0
        while self.robot.step(TIME_STEP) != -1:    
            if self.is_new_data():
                data = self.get_new_data()
                
                # Get the position of our robot
                robot_pos = data[self.name]
                b3_pos = data['B3']
                # Get the position of the ball
                ball_pos = data['ball']
                b_dist = math.sqrt(pow((robot_pos['x']-ball_pos['x']),2) + pow(robot_pos['y'] - ball_pos['y'],2))
                b3_dist = math.sqrt(pow((b3_pos['x']-ball_pos['x']),2) + pow(b3_pos['y'] - ball_pos['y'],2))
                # Get angle between the robot and the ball
                # and between the robot and the north
                ba, ra = self.get_angles(ball_pos, robot_pos)
                #print(math.degrees(robot_angle))
                # Compute the speed for motors
                direction = utils.get_direction(ba)
                directionb = utils.get_directionb(ba)
                
                # starting time
                #start = time.time()
               # while (time.time()-start)<500:
                    
                
                if a == 0:
                    side = math.degrees(ra)
                    a = 1
                    #print(side, 'yellow') 
                    
                if side > 180:
                    tra = 360-math.degrees(ra)
                else:
                    tra = (180-math.degrees(ra))%360
                    
                ab = (tra + ba) % 360
                
                
                if ball_pos['y']<-0.2:
                    if ball_pos['x'] < 0:
                        bstate = 1
                    else:
                        bstate = 2
                elif ball_pos['y']>0.2:
                    if ball_pos['x'] > 0:
                        bstate = 3
                    else:
                        bstate = 4
                else:
                    bstate = 0
                
                
                if side > 180:
                    if ball_pos['x']>0 and ball_pos['y']>0:
                        dyn = 3
                    elif ball_pos['x']>0 and ball_pos['y']<0:
                        dyn = 2
                    elif ball_pos['x']<0 and ball_pos['y']<0:
                        dyn = 1
                    elif ball_pos['x']<0 and ball_pos['y']>0:
                        dyn = 4
                else:
                    if ball_pos['x']<0 and ball_pos['y']<0:
                        dyn = 3
                    elif ball_pos['x']<0 and ball_pos['y']>0:
                        dyn = 2
                    elif ball_pos['x']>0 and ball_pos['y']>0:
                        dyn = 1
                    elif ball_pos['x']>0 and ball_pos['y']<0:
                        dyn = 4
                        
                if side > 180:   #blue
                    if dyn == 3 or dyn == 4:
                        yo=0
                        yo2=0
                        if (b_dist < 0.25):
                            if ba <= 90+da or ba >= 270-da:     #front
                                if tra<360 and tra>180:
                                    #print('bre')
                                    if ab > 250 and ab < 290:  #########
                                        if ab>270:
                                            if tra > 220 and tra < 240:
                                                left_speed = -10
                                                right_speed = -10
                                            else:
                                                if tra > 230 or tra < 50:
                                                    left_speed = 5
                                                    right_speed = -5
                                                else:
                                                    left_speed = -5
                                                    right_speed = 5     
                                        else:
                                             if tra > 300 and tra < 320:
                                                 left_speed = -10
                                                 right_speed = -10
                                             else:
                                                 if tra > 310 or tra < 130:
                                                     left_speed = 5
                                                     right_speed = -5
                                                 else:
                                                     left_speed = -5
                                                     right_speed = 5  
                                             
                                    else: 
                                        if tra<285 and tra>260:
                                            left_speed = -10
                                            right_speed = -10
                                            da = 50
                                        elif tra > 270 or tra < 90:
                                            left_speed = 5
                                            right_speed = -5
                                        else:
                                            left_speed = -5
                                            right_speed = 5
                                else:   #v
                                    da = 0  
                                    #print('yoo')
                                    
                                    if ba <= 90 or ba >= 270:
                                        if direction == 0:
                                            if robot_pos['y'] < 0 and robot_pos['x'] > 0.62 and (tra > 270 or tra < 90) and b_dist < 0.2:
                                                left_speed = 10
                                                right_speed = 10
                                            elif robot_pos['y'] > 0 and robot_pos['x'] > 0.62 and tra < 270 and tra > 90 and b_dist < 0.2:
                                                left_speed = 10
                                                right_speed = 10
                                            else:
                                                left_speed = -10
                                                right_speed = -10 
                                            if robot_pos['y'] < 0 and robot_pos['x'] < -0.62 and (tra < 270 and tra > 90) and b_dist < 0.2:
                                                left_speed = 10
                                                right_speed = 10
                                            elif robot_pos['y'] > 0 and robot_pos['x'] <- 0.62 and (tra > 270 or tra < 90) and b_dist < 0.2:
                                                left_speed = 10
                                                right_speed = 10
                                            else:
                                                left_speed = -10
                                                right_speed = -10
                                        else: 
                                            left_speed = direction * 10
                                            right_speed = direction * -10
                                    elif ba > 90 and ba < 270:
                                        if directionb == 0:
                                            if robot_pos['y'] < 0 and robot_pos['x'] > 0.62 and tra < 270 and tra > 90 and b_dist < 0.2:
                                                left_speed = -10
                                                right_speed = -10
                                            elif robot_pos['y'] > 0 and robot_pos['x'] > 0.62 and (tra > 270 or tra < 90) and b_dist < 0.2:
                                                left_speed = -10
                                                right_speed = -10
                                            else:
                                                left_speed = 10
                                                right_speed = 10
                                            if robot_pos['y'] < 0 and robot_pos['x'] < -0.62 and (tra > 270 or tra < 90) and b_dist < 0.2:
                                                left_speed = -10
                                                right_speed = -10
                                            elif robot_pos['y'] > 0 and robot_pos['x'] < -0.62 and (tra < 270 and tra > 90) and b_dist < 0.2:
                                                left_speed = -10
                                                right_speed = -10
                                            else:
                                                left_speed = 10
                                                right_speed = 10
                                        else:
                                            left_speed = directionb * 10
                                            right_speed = directionb * -10
                                    
                                
                                    
                            elif ba > 90-da and ba < 270+da:      #back
                                if tra<180 and tra>0:
                                    #print('hey')
                                    if ab > 250 and ab < 290:
                                        if ab>270:
                                            if tra > 40 and tra < 60:
                                                left_speed = 10
                                                right_speed = 10
                                            else:
                                                if tra > 50 and tra < 230:
                                                    left_speed = 5
                                                    right_speed = -5
                                                else:
                                                    left_speed = -5
                                                    right_speed = 5    
                                        else:
                                            if tra > 120 and tra < 140:
                                                left_speed = 10
                                                right_speed = 10
                                            else:
                                                if tra > 130 and tra < 310:
                                                    left_speed = 5
                                                    right_speed = -5
                                                else:
                                                    left_speed = -5
                                                    right_speed = 5 
                                             
                                    else: 
                                        if tra<100 and tra>80:
                                            left_speed = 10
                                            right_speed = 10
                                            da = -50
                                        elif tra > 90 and tra < 270:
                                            left_speed = 5
                                            right_speed = -5
                                        else:
                                            left_speed = -5
                                            right_speed = 5
                                else:
                                    da = 0
                              
                                    if ba <= 90 or ba >= 270:
                                        if direction == 0:
                                            if robot_pos['y'] < 0 and robot_pos['x'] > 0.62 and (tra > 270 or tra < 90) and b_dist < 0.2:
                                                left_speed = 10
                                                right_speed = 10
                                            elif robot_pos['y'] > 0 and robot_pos['x'] > 0.62 and tra < 270 and tra > 90 and b_dist < 0.2:
                                                left_speed = 10
                                                right_speed = 10
                                            else:
                                                left_speed = -10
                                                right_speed = -10 
                                            if robot_pos['y'] < 0 and robot_pos['x'] < -0.62 and (tra < 270 and tra > 90) and b_dist < 0.2:
                                                left_speed = 10
                                                right_speed = 10
                                            elif robot_pos['y'] > 0 and robot_pos['x'] <- 0.62 and (tra > 270 or tra < 90) and b_dist < 0.2:
                                                left_speed = 10
                                                right_speed = 10
                                            else:
                                                left_speed = -10
                                                right_speed = -10
                                        else: 
                                            left_speed = direction * 10
                                            right_speed = direction * -10
                                    elif ba > 90 and ba < 270:
                                        if directionb == 0:
                                            if robot_pos['y'] < 0 and robot_pos['x'] > 0.62 and tra < 270 and tra > 90 and b_dist < 0.2:
                                                left_speed = -10
                                                right_speed = -10
                                            elif robot_pos['y'] > 0 and robot_pos['x'] > 0.62 and (tra > 270 or tra < 90) and b_dist < 0.2:
                                                left_speed = -10
                                                right_speed = -10
                                            else:
                                                left_speed = 10
                                                right_speed = 10
                                            if robot_pos['y'] < 0 and robot_pos['x'] < -0.62 and (tra > 270 or tra < 90) and b_dist < 0.2:
                                                left_speed = -10
                                                right_speed = -10
                                            elif robot_pos['y'] > 0 and robot_pos['x'] < -0.62 and (tra < 270 and tra > 90) and b_dist < 0.2:
                                                left_speed = -10
                                                right_speed = -10
                                            else:
                                                left_speed = 10
                                                right_speed = 10
                                        else:
                                            left_speed = directionb * 10
                                            right_speed = directionb * -10
           
                        else:
                            da = 0
                            #print('yoo')
                            
                            if ba <= 90 or ba >= 270:
                                if direction == 0:
                                    if robot_pos['y'] < 0 and robot_pos['x'] > 0.62 and (tra > 270 or tra < 90) and b_dist < 0.2:
                                        left_speed = 10
                                        right_speed = 10
                                    elif robot_pos['y'] > 0 and robot_pos['x'] > 0.62 and tra < 270 and tra > 90 and b_dist < 0.2:
                                        left_speed = 10
                                        right_speed = 10
                                    else:
                                        left_speed = -10
                                        right_speed = -10 
                                    if robot_pos['y'] < 0 and robot_pos['x'] < -0.62 and (tra < 270 and tra > 90) and b_dist < 0.2:
                                        left_speed = 10
                                        right_speed = 10
                                    elif robot_pos['y'] > 0 and robot_pos['x'] <- 0.62 and (tra > 270 or tra < 90) and b_dist < 0.2:
                                        left_speed = 10
                                        right_speed = 10
                                    else:
                                        left_speed = -10
                                        right_speed = -10
                                else: 
                                    left_speed = direction * 10
                                    right_speed = direction * -10
                            elif ba > 90 and ba < 270:
                                if directionb == 0:
                                    if robot_pos['y'] < 0 and robot_pos['x'] > 0.62 and tra < 270 and tra > 90 and b_dist < 0.2:
                                        left_speed = -10
                                        right_speed = -10
                                    elif robot_pos['y'] > 0 and robot_pos['x'] > 0.62 and (tra > 270 or tra < 90) and b_dist < 0.2:
                                        left_speed = -10
                                        right_speed = -10
                                    else:
                                        left_speed = 10
                                        right_speed = 10
                                    if robot_pos['y'] < 0 and robot_pos['x'] < -0.62 and (tra > 270 or tra < 90) and b_dist < 0.2:
                                        left_speed = -10
                                        right_speed = -10
                                    elif robot_pos['y'] > 0 and robot_pos['x'] < -0.62 and (tra < 270 and tra > 90) and b_dist < 0.2:
                                        left_speed = -10
                                        right_speed = -10
                                    else:
                                        left_speed = 10
                                        right_speed = 10
                                else:
                                    left_speed = directionb * 10
                                    right_speed = directionb * -10
                                
                    elif dyn == 1 and ball_pos['x'] > -0.62:
                        yo = 0 
                        if tra > 80 and tra < 100:
                            if (robot_pos['x']-ball_pos['x'])>0.2:
                                left_speed = -10
                                right_speed = -10
                            else:
                                left_speed = 10
                                right_speed = 10  
                            if ba > 300 or ba < 60:
                                left_speed = -10
                                right_speed = -10   
                        else:
                            if tra > 90 and tra < 270:
                                left_speed = 5
                                right_speed = -5
                            else:
                                left_speed = -5
                                right_speed = 5  
                    elif ball_pos['x'] < -0.62 and ball_pos['y'] < 0.3:      #####################################
                        if tra > 80 and tra < 100 and yo == 0:
                            if robot_pos['x'] < -0.68 or robot_pos['x'] > -0.65:
                                if robot_pos['x'] < -0.67:
                                    left_speed = 6
                                    right_speed = 6
                                else:
                                    left_speed = -6
                                    right_speed = -6
                            else:
                                yo = 1
                                left_speed = 0
                                right_speed = 0
                        else:
                            if tra > 90 and tra < 270:
                                left_speed = 5
                                right_speed = -5
                            else:
                                left_speed = -5
                                right_speed = 5
                        if yo == 1:
                            if tra >170 and tra < 190:
                                if robot_pos['y']<0.2 or robot_pos['y'] > 0.25:
                                    if robot_pos['y'] > 0.216:
                                        left_speed = -6
                                        right_speed = -6
                                    else:
                                        left_speed = 6
                                        right_speed = 6
                                else:
                                    yo = 2
                                    left_speed = 0
                                    right_speed = 0
                            else:
                                if tra > 180 and tra < 360:
                                    left_speed = 5
                                    right_speed = -5
                                else:
                                    left_speed = -5
                                    right_speed = 5
                        if yo == 2:
                            if tra > 147 and tra < 167:
                                left_speed = 0
                                right_speed = 0
                                if ba > 345 or ba < 15:
                                    left_speed = -10
                                    right_speed = -10
                            else:
                                if tra > 157 and tra < 337:
                                    left_speed = 5
                                    right_speed = -5
                                else:
                                    left_speed = -5
                                    right_speed = 5
                    elif dyn == 2:
                        yo2=0
                        if tra > 80 and tra < 100 and yo == 0:
                            if robot_pos['x'] < 0.185 or robot_pos['x'] > 0.215:
                                if robot_pos['x'] < 0.208:
                                    left_speed = 6
                                    right_speed = 6
                                else:
                                    left_speed = -6
                                    right_speed = -6
                            else:
                                yo = 1
                                left_speed = 0
                                right_speed = 0
                            if ab > 250 and ab < 290:
                                left_speed = 0
                                right_speed = 0
                        else:
                            if tra > 90 and tra < 270:
                                left_speed = 5
                                right_speed = -5
                            else:
                                left_speed = -5
                                right_speed = 5
                        if yo == 1:
                            if tra >170 and tra < 190:
                                if robot_pos['y']<-0.03 or robot_pos['y'] > 0.03:
                                    if robot_pos['y'] > 0:
                                        left_speed = -6
                                        right_speed = -6
                                    else:
                                        left_speed = 6
                                        right_speed = 6
                                else:
                                    yo = 2
                                    left_speed = 0
                                    right_speed = 0
                            else:
                                if tra > 180 and tra < 360:
                                    left_speed = 5
                                    right_speed = -5
                                else:
                                    left_speed = -5
                                    right_speed = 5
                        if yo == 2:
                            if tra > 80 and tra < 100:
                                if ba > 330 or ba < 30:
                                    left_speed = -10
                                    right_speed = -10
                                else:
                                    if robot_pos['x'] < 0.185 or robot_pos['x'] > 0.215:
                                        if robot_pos['x'] < 0.208:
                                            left_speed = 6
                                            right_speed = 6
                                        else:
                                            left_speed = -6
                                            right_speed = -6
                                    else:
                                        left_speed = -6
                                        right_speed = -6
                                if ab > 250 and ab < 290:
                                    left_speed = -10
                                    right_speed = -10
                            else:
                                if tra > 90 and tra < 270:
                                    left_speed = 5
                                    right_speed = -5
                                else:
                                    left_speed = -5
                                    right_speed = 5
                else:        ####################yellow#########################
                    if dyn == 3 or dyn == 4:
                        yo=0
                        yo2=0
                        if (b_dist < 0.25):
                            if ba <= 90+da or ba >= 270-da:     #front
                                if tra<360 and tra>180:
                                    #print('bre')
                                    if ab > 250 and ab < 290:  #########
                                        if ab>270:
                                            if tra > 220 and tra < 240:
                                                left_speed = -10
                                                right_speed = -10
                                            else:
                                                if tra > 230 or tra < 50:
                                                    left_speed = 5
                                                    right_speed = -5
                                                else:
                                                    left_speed = -5
                                                    right_speed = 5     
                                        else:
                                             if tra > 300 and tra < 320:
                                                 left_speed = -10
                                                 right_speed = -10
                                             else:
                                                 if tra > 310 or tra < 130:
                                                     left_speed = 5
                                                     right_speed = -5
                                                 else:
                                                     left_speed = -5
                                                     right_speed = 5  
                                             
                                    else: 
                                        if tra<285 and tra>260:
                                            left_speed = -10
                                            right_speed = -10
                                            da = 50
                                        elif tra > 270 or tra < 90:
                                            left_speed = 5
                                            right_speed = -5
                                        else:
                                            left_speed = -5
                                            right_speed = 5
                                else:   #v
                                    da = 0  
                                    #print('yoo')
                                    
                                    if ba <= 90 or ba >= 270:
                                        if direction == 0:
                                            if robot_pos['y'] < 0 and robot_pos['x'] < -0.62 and (tra < 270 and tra > 90) and b_dist < 0.2:
                                                left_speed = 10
                                                right_speed = 10
                                            elif robot_pos['y'] > 0 and robot_pos['x'] < -0.62 and (tra > 270 or tra < 90) and b_dist < 0.2:
                                                left_speed = 10
                                                right_speed = 10
                                            else:
                                                left_speed = -10
                                                right_speed = -10 
                                            if robot_pos['y'] < 0 and robot_pos['x'] > 0.62 and (tra > 270 or tra < 90) and b_dist < 0.2:
                                                left_speed = 10
                                                right_speed = 10
                                            elif robot_pos['y'] > 0 and robot_pos['x'] > 0.62 and (tra < 270 and tra > 90) and b_dist < 0.2:
                                                left_speed = 10
                                                right_speed = 10
                                            else:
                                                left_speed = -10
                                                right_speed = -10
                                        else: 
                                            left_speed = direction * 10
                                            right_speed = direction * -10
                                    elif ba > 90 and ba < 270:
                                        if directionb == 0:
                                            if robot_pos['y'] < 0 and robot_pos['x'] < -0.62 and (tra > 270 or tra < 90) and b_dist < 0.2:
                                                left_speed = -10
                                                right_speed = -10
                                            elif robot_pos['y'] > 0 and robot_pos['x'] < -0.62 and (tra < 270 and tra > 90) and b_dist < 0.2:
                                                left_speed = -10
                                                right_speed = -10
                                            else:
                                                left_speed = 10
                                                right_speed = 10
                                            if robot_pos['y'] < 0 and robot_pos['x'] > 0.62 and (tra < 270 and tra > 90) and b_dist < 0.2:
                                                left_speed = -10
                                                right_speed = -10
                                            elif robot_pos['y'] > 0 and robot_pos['x'] > 0.62 and (tra > 270 or tra < 90) and b_dist < 0.2:
                                                left_speed = -10
                                                right_speed = -10
                                            else:
                                                left_speed = 10
                                                right_speed = 10
                                        else:
                                            left_speed = directionb * 10
                                            right_speed = directionb * -10
                                    
                                
                                    
                            elif ba > 90-da and ba < 270+da:      #back
                                if tra<180 and tra>0:
                                    #print('hey')
                                    if ab > 250 and ab < 290:
                                        if ab>270:
                                            if tra > 40 and tra < 60:
                                                left_speed = 10
                                                right_speed = 10
                                            else:
                                                if tra > 50 and tra < 230:
                                                    left_speed = 5
                                                    right_speed = -5
                                                else:
                                                    left_speed = -5
                                                    right_speed = 5    
                                        else:
                                            if tra > 120 and tra < 140:
                                                left_speed = 10
                                                right_speed = 10
                                            else:
                                                if tra > 130 and tra < 310:
                                                    left_speed = 5
                                                    right_speed = -5
                                                else:
                                                    left_speed = -5
                                                    right_speed = 5 
                                             
                                    else: 
                                        if tra<100 and tra>80:
                                            left_speed = 10
                                            right_speed = 10
                                            da = -50
                                        elif tra > 90 and tra < 270:
                                            left_speed = 5
                                            right_speed = -5
                                        else:
                                            left_speed = -5
                                            right_speed = 5
                                else:
                                    da = 0
                              
                                    if ba <= 90 or ba >= 270:
                                        if direction == 0:
                                            if robot_pos['y'] < 0 and robot_pos['x'] < -0.62 and (tra < 270 and tra > 90) and b_dist < 0.2:
                                                left_speed = 10
                                                right_speed = 10
                                            elif robot_pos['y'] > 0 and robot_pos['x'] < -0.62 and (tra > 270 or tra < 90) and b_dist < 0.2:
                                                left_speed = 10
                                                right_speed = 10
                                            else:
                                                left_speed = -10
                                                right_speed = -10 
                                            if robot_pos['y'] < 0 and robot_pos['x'] > 0.62 and (tra > 270 or tra < 90) and b_dist < 0.2:
                                                left_speed = 10
                                                right_speed = 10
                                            elif robot_pos['y'] > 0 and robot_pos['x'] > 0.62 and (tra < 270 and tra > 90) and b_dist < 0.2:
                                                left_speed = 10
                                                right_speed = 10
                                            else:
                                                left_speed = -10
                                                right_speed = -10
                                        else: 
                                            left_speed = direction * 10
                                            right_speed = direction * -10
                                    elif ba > 90 and ba < 270:
                                        if directionb == 0:
                                            if robot_pos['y'] < 0 and robot_pos['x'] < -0.62 and (tra > 270 or tra < 90) and b_dist < 0.2:
                                                left_speed = -10
                                                right_speed = -10
                                            elif robot_pos['y'] > 0 and robot_pos['x'] < -0.62 and (tra < 270 and tra > 90) and b_dist < 0.2:
                                                left_speed = -10
                                                right_speed = -10
                                            else:
                                                left_speed = 10
                                                right_speed = 10
                                            if robot_pos['y'] < 0 and robot_pos['x'] > 0.62 and (tra < 270 and tra > 90) and b_dist < 0.2:
                                                left_speed = -10
                                                right_speed = -10
                                            elif robot_pos['y'] > 0 and robot_pos['x'] > 0.62 and (tra > 270 or tra < 90) and b_dist < 0.2:
                                                left_speed = -10
                                                right_speed = -10
                                            else:
                                                left_speed = 10
                                                right_speed = 10
                                        else:
                                            left_speed = directionb * 10
                                            right_speed = directionb * -10
           
                        else:
                            da = 0
                            #print('yoo')
                            
                            if ba <= 90 or ba >= 270:
                                if direction == 0:
                                    if robot_pos['y'] < 0 and robot_pos['x'] < -0.62 and (tra < 270 and tra > 90) and b_dist < 0.2:
                                        left_speed = 10
                                        right_speed = 10
                                    elif robot_pos['y'] > 0 and robot_pos['x'] < -0.62 and (tra > 270 or tra < 90) and b_dist < 0.2:
                                        left_speed = 10
                                        right_speed = 10
                                    else:
                                        left_speed = -10
                                        right_speed = -10 
                                    if robot_pos['y'] < 0 and robot_pos['x'] > 0.62 and (tra > 270 or tra < 90) and b_dist < 0.2:
                                        left_speed = 10
                                        right_speed = 10
                                    elif robot_pos['y'] > 0 and robot_pos['x'] > 0.62 and (tra < 270 and tra > 90) and b_dist < 0.2:
                                        left_speed = 10
                                        right_speed = 10
                                    else:
                                        left_speed = -10
                                        right_speed = -10
                                else: 
                                    left_speed = direction * 10
                                    right_speed = direction * -10
                            elif ba > 90 and ba < 270:
                                if directionb == 0:
                                    if robot_pos['y'] < 0 and robot_pos['x'] < -0.62 and (tra > 270 or tra < 90) and b_dist < 0.2:
                                        left_speed = -10
                                        right_speed = -10
                                    elif robot_pos['y'] > 0 and robot_pos['x'] < -0.62 and (tra < 270 and tra > 90) and b_dist < 0.2:
                                        left_speed = -10
                                        right_speed = -10
                                    else:
                                        left_speed = 10
                                        right_speed = 10
                                    if robot_pos['y'] < 0 and robot_pos['x'] > 0.62 and (tra < 270 and tra > 90) and b_dist < 0.2:
                                        left_speed = -10
                                        right_speed = -10
                                    elif robot_pos['y'] > 0 and robot_pos['x'] > 0.62 and (tra > 270 or tra < 90) and b_dist < 0.2:
                                        left_speed = -10
                                        right_speed = -10
                                    else:
                                        left_speed = 10
                                        right_speed = 10
                                else:
                                    left_speed = directionb * 10
                                    right_speed = directionb * -10
                                
                    elif dyn == 1 and ball_pos['x'] < 0.62:
                        yo = 0 
                        if tra > 80 and tra < 100:
                            if (ball_pos['x']-robot_pos['x']) > 0.2:
                                left_speed = -10
                                right_speed = -10
                            else:
                                left_speed = 10
                                right_speed = 10  
                            if ba > 300 or ba < 60:
                                left_speed = -10
                                right_speed = -10   
                        else:
                            if tra > 90 and tra < 270:
                                left_speed = 5
                                right_speed = -5
                            else:
                                left_speed = -5
                                right_speed = 5  
                    elif ball_pos['x'] > 0.62 and ball_pos['y'] < 0.3:      #####################################
                        if tra > 80 and tra < 100 and yo == 0:
                            if robot_pos['x'] > 0.68 or robot_pos['x'] > -0.65:
                                if robot_pos['x'] > 0.67:
                                    left_speed = 6
                                    right_speed = 6
                                else:
                                    left_speed = -6
                                    right_speed = -6
                            else:
                                yo = 1
                                left_speed = 0
                                right_speed = 0
                        else:
                            if tra > 90 and tra < 270:
                                left_speed = 5
                                right_speed = -5
                            else:
                                left_speed = -5
                                right_speed = 5
                        if yo == 1:
                            if tra >170 and tra < 190:
                                if robot_pos['y']<0.2 or robot_pos['y'] > 0.25:
                                    if robot_pos['y'] < 0.216:
                                        left_speed = -6
                                        right_speed = -6
                                    else:
                                        left_speed = 6
                                        right_speed = 6
                                else:
                                    yo = 2
                                    left_speed = 0
                                    right_speed = 0
                            else:
                                if tra > 180 and tra < 360:
                                    left_speed = 5
                                    right_speed = -5
                                else:
                                    left_speed = -5
                                    right_speed = 5
                        if yo == 2:
                            if tra > 147 and tra < 167:
                                left_speed = 0
                                right_speed = 0
                                if ba > 345 or ba < 15:
                                    left_speed = -10
                                    right_speed = -10
                            else:
                                if tra > 157 and tra < 337:
                                    left_speed = 5
                                    right_speed = -5
                                else:
                                    left_speed = -5
                                    right_speed = 5
                    elif dyn == 2:
                        yo2=0
                        if tra > 80 and tra < 100 and yo == 0:
                            if robot_pos['x'] > -0.185 or robot_pos['x'] < -0.215:
                                if robot_pos['x'] > -0.208:
                                    left_speed = 6
                                    right_speed = 6
                                else:
                                    left_speed = -6
                                    right_speed = -6
                            else:
                                yo = 1
                                left_speed = 0
                                right_speed = 0
                            if ab > 250 and ab < 290:
                                left_speed = 0
                                right_speed = 0
                        else:
                            if tra > 90 and tra < 270:
                                left_speed = 5
                                right_speed = -5
                            else:
                                left_speed = -5
                                right_speed = 5
                        if yo == 1:
                            if tra > 170 and tra < 190:
                                if robot_pos['y']<-0.03 or robot_pos['y'] > 0.03:
                                    if robot_pos['y'] < 0:
                                        left_speed = -6
                                        right_speed = -6
                                    else:
                                        left_speed = 6
                                        right_speed = 6
                                else:
                                    yo = 2
                                    left_speed = 0
                                    right_speed = 0
                            else:
                                if tra > 180 and tra < 360:
                                    left_speed = 5
                                    right_speed = -5
                                else:
                                    left_speed = -5
                                    right_speed = 5
                        if yo == 2:
                            if tra > 80 and tra < 100:
                                if ba > 330 or ba < 30:
                                    left_speed = -10
                                    right_speed = -10
                                else:
                                    if robot_pos['x'] > -0.185 or robot_pos['x'] < -0.215:
                                        if robot_pos['x'] > -0.208:
                                            left_speed = 6
                                            right_speed = 6
                                        else:
                                            left_speed = -6
                                            right_speed = -6
                                    else:
                                        left_speed = -6
                                        right_speed = -6
                                if ab > 250 and ab < 290:
                                    left_speed = -10
                                    right_speed = -10
                            else:
                                if tra > 90 and tra < 270:
                                    left_speed = 5
                                    right_speed = -5
                                else:
                                    left_speed = -5
                                    right_speed = 5
                                                
                self.left_motor.setVelocity(left_speed)
                self.right_motor.setVelocity(right_speed)


my_robot = MyRobot()
my_robot.run()
