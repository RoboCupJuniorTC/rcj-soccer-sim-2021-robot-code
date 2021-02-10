import math
import random
import struct
from typing import Tuple
from controller import Robot

TIME_STEP = 64
ROBOT_NAMES = ["B1", "B2", "B3", "Y1", "Y2", "Y3"]
N_ROBOTS = len(ROBOT_NAMES)

def get_direction(ball_angle: float) -> int:
    if ball_angle >= 345 or ball_angle <= 15:
        return 0
    return -1 if ball_angle < 180 else 1


prev_pos = {}
dist_rolled = 0
deg_rotated = 0
all_waypoints = []

class Waypoint(object):
    def __init__(self, destx, desty, speed, priority, angle, distance, movetype):
        self.destx = destx
        self.desty = desty
        self.speed = speed
        self.priority = priority
        self.angle = angle
        self.distance = distance
        self.movetype = movetype
    def __repr__(self):
        return repr((self.destx, self.desty, self.speed, self.priority, self.angle, self.distance, self.movetype))

def create_waypoint(destx, desty, speed, priority, angle, distance, movetype):
    waypoint = Waypoint(destx, desty, speed, priority, angle, distance, movetype)
    return waypoint

def return_priority(obj):
    return obj.priority

def add_coords_dest(x, y, speed, priority): # move the robot to the given coordinates
    new_waypoint = create_waypoint(x, y, speed, priority, None, None, "to_coords")
    all_waypoints.append(new_waypoint)
    all_waypoints.sort(key=return_priority, reverse=True)
    #print(all_waypoints)

def add_rotate(rot_angle, speed, priority): # rotate the robot by the given angle
    new_waypoint = create_waypoint(None, None, speed, priority, rot_angle, None, "rotate")
    all_waypoints.append(new_waypoint)
    all_waypoints.sort(key=return_priority, reverse=True)
    #print(all_waypoints)

def add_move(dist, speed, priority): # move the robot forward or backwards by the given distance
    new_waypoint = create_waypoint(None, None, speed, priority, None, dist, "move")
    all_waypoints.append(new_waypoint)
    all_waypoints.sort(key=return_priority, reverse=True)
    #print(all_waypoints)

def clearwaypoints():
    all_waypoints.clear()

class RCJSoccerRobot:
    def __init__(self):
        self.robot = Robot()
        self.name = self.robot.getName()
        self.team = self.name[0]
        self.player_id = int(self.name[1])
        self.player_id_string = self.name[1]
        self.data_current = None
        self.data_previous = None
        self.attack_powers = {"2":0, "3":0}

        self.receiver = self.robot.getDevice("receiver")
        self.receiver.enable(TIME_STEP)

        self.left_motor = self.robot.getDevice("left wheel motor")
        self.right_motor = self.robot.getDevice("right wheel motor")

        self.left_motor.setPosition(float('+inf'))
        self.right_motor.setPosition(float('+inf'))

        self.left_motor.setVelocity(0.0)
        self.right_motor.setVelocity(0.0)


    def attack_power(self, rname):
        ball_pos = self.data_current['ball']
        robot_pos = self.data_current[rname]
        ball_angle, robot_angle = self.get_angles(ball_pos, robot_pos)
        ang, move_dir, distance = self.getpointinfo(rname, self.data_current, ball_pos['x'], ball_pos['y'])

        """TODO"""
        if self.team == 'B':
            if robot_pos['x'] < ball_pos['x']:
                return 0
        else:
            if robot_pos['x'] > ball_pos['x']:
                return 0

        
        if 0<= abs(ball_angle) <=30:
            sector_value = 10
        elif 30< abs(ball_angle) <=90:
            sector_value = 20
        elif 90< abs(ball_angle) <=150:
            sector_value = 30
        elif 150< abs(ball_angle) <=180:
            sector_value = 40
        else:
            sector_value = 0   
        attack_value = (((1-distance)*100)-sector_value)

        return attack_value

    def other_striker_name(self):
        #stirker is either '2' or '3'
        return str(2+((self.player_id+1)%2))

    def am_i_striker(self):
        mypower = self.attack_powers[str(self.player_id)]
        otherpower = self.attack_powers[self.other_striker_name()]
        if mypower == 0:
            return False
        elif mypower >= 30:
            return True
        elif mypower > otherpower:
            return True
        else:
            return False

    def parse_supervisor_msg(self, packet: str) -> dict:
        struct_fmt = 'ddd' * N_ROBOTS + 'dd'
        unpacked = struct.unpack(struct_fmt, packet)
        data = {}
        for i, r in enumerate(ROBOT_NAMES):
            data[r] = {
                "x": unpacked[3 * i],
                "y": unpacked[3 * i + 1],
                "orientation": unpacked[3 * i + 2]
            }
        data["ball"] = {
            "x": unpacked[3 * N_ROBOTS],
            "y": unpacked[3 * N_ROBOTS + 1]
        }
        return data

    def get_new_data(self) -> dict:
        packet = self.receiver.getData()
        self.receiver.nextPacket()
        return self.parse_supervisor_msg(packet)

    def is_new_data(self) -> bool:
        return self.receiver.getQueueLength() > 0

    def get_angles(self, ball_pos: dict, robot_pos: dict) -> Tuple[float, float]:
        robot_angle: float = robot_pos['orientation']
        angle = math.atan2(ball_pos['y'] - robot_pos['y'], ball_pos['x'] - robot_pos['x'])
        if angle < 0:
            angle = 2 * math.pi + angle
        if robot_angle < 0:
            robot_angle = 2 * math.pi + robot_angle
        robot_ball_angle = math.degrees(angle + robot_angle)
        robot_ball_angle -= 90
        if robot_ball_angle > 360:
            robot_ball_angle -= 360
        return robot_ball_angle, robot_angle

    def kickoffcheck(self, data):
        global prev_pos
        if (len(prev_pos) == 0):
            #print("no previous position").
            pass
        else:
            #[key, xdiff, ydiff, x, y]
            diff_coords = []
            for key in data:
                if (key == 'ball'):
                    continue
                item = data[key]
                previtem = prev_pos[key]
                diff_coords.append([key, abs(item['x'] - previtem['x']), abs(item['y'] - previtem['y']), item['x'], item['y']])
            repositioned = []
            for item in diff_coords:
                x = item[3]
                y = item[4]
                # orientation = round(data[item[0]]['orientation'], 3)
                # and (orientation == 1.57 or orientation == -1.57) a legelején valamiért mindegyiknek ennyi, de ennek nézése nélkül is működik
                if ((item[1] > 0.01 or item[2] > 0.01)):
                    if((-0.375 <= x and x <= -0.225) or (0.225 <= x and x <= 0.375) or (-0.275 <= x and x <= -0.125) or (0.125 <= x and x <= 0.275) or (0.025 <= x and x <= 0.175) or (-0.175 <= x and x <= -0.025)):
                        if((0.225 <= y and y <= 0.375) or (-0.075 <= y and y <= 0.075) or (-0.375 <= y and y <= -0.225) or (-0.075 <= y and y <= 0.075)):
                            repositioned.append(item[0])
            if (len(repositioned) > 0 and len(repositioned) != 6):
                #print("LACK OF PROGRESS: ", repositioned) #lack of progress
                pass
            if (len(repositioned) == 6 and (data['ball']['x'] > -0.001 and data['ball']['x'] < 0.001) and (data['ball']['y'] > -0.001 and data['ball']['y'] < 0.001)):
                return 1
            return 0

    def getballangle(self, name, data):
        ball_pos = data['ball'] # {'x', 'y'}
        angle, move_direction, distance = self.getpointinfo(name, data, ball_pos['x'], ball_pos['y'])
        return angle, move_direction, distance

    def getpointinfo(self, name, data, x, y):
        robot_pos = data[name] # {'x', 'y', 'orientation'}

        rel_ballpos_x = robot_pos['x'] - x
        rel_ballpos_y = robot_pos['y'] - y
        robot_angle = math.degrees(robot_pos['orientation'])

        distance = math.sqrt(rel_ballpos_x ** 2 + rel_ballpos_y ** 2)
        alpha = math.degrees(math.asin( rel_ballpos_x / distance ))

        if rel_ballpos_y > 0:
            if rel_ballpos_x > 0:
                rel_ball_angle = alpha
            else:
                rel_ball_angle = 360 + alpha
        else:
            if rel_ballpos_x > 0:
                rel_ball_angle = 180 - alpha
            else:
                rel_ball_angle = 180 - alpha
        rel_ball_angle -= 180

        # -360 <-> 360 fok között
        angle360 = rel_ball_angle - robot_angle

        angle90, move_direction = self.reduceangle(angle360)

        return angle90, move_direction, distance

    def reduceangle(self, angle360):
        # -180 <-> 180 fok közé szorítás
        if angle360 < -180:
            angle180 = 360 + angle360
        elif angle360 > 180:
            angle180 = -360 + angle360
        else:
            angle180 = angle360

        # -90 <-> 90 fok közé szorítás
        if angle180 > 90:
            move_direction = -1
            angle90 = -180 + angle180
        elif angle180 < -90:
            move_direction = -1
            angle90 = 180 + angle180
        else:
            move_direction = 1
            angle90 = angle180
        
        return angle90, move_direction

    def kickoffercheck(self, name, data):
        balldistances = {}
        for robot in data:
            if (robot == 'ball'):
                continue
            _, _, distance = self.getballangle(robot, data)
            balldistances[robot] = distance
        kickoffer = min(balldistances, key=balldistances.get)
        if (kickoffer == name):
            return True
        return False

    def travel(self, name, data, x, y, speed):
        robot_pos = data[name]
        robotx = robot_pos['x']
        roboty = robot_pos['y']
        pointangle, point_move_direction, point_distance = self.getpointinfo(name, data, x, y)

        if (not (-10 < pointangle and 10 > pointangle)):
            #nagy szögeltérésnél forduljon
            #print("hola :)")
            left_speed = pointangle / abs(pointangle) * speed/2
            right_speed = pointangle / abs(pointangle) * -speed/2
        else:
            #kis eltérésnél proporsonal
            #print("kk")
            left_speed = (-speed + (pointangle*0.3)) * point_move_direction
            right_speed = (-speed - (pointangle*0.3)) * point_move_direction
        if (abs(robotx - x) < 0.01 and abs(roboty - y) < 0.01):
            #ha odaér megáll
            #print("Itt vagyok :DD")
            left_speed = 0
            right_speed = 0

        if abs(left_speed) > 10 or abs(right_speed) > 10:
            #ha bármelyik sebesség nagyobb, mint 10 visszaosztja őket, hogy 10-nél kisebbek legyenek
            #a jobb bal sebesség arányának megtartásával, osztó sose lesz 0, nem kell kikötés 0-ra
            if abs(left_speed) > abs(right_speed):
                if left_speed > 0:
                    correctional_multiplier = 10/left_speed
                else:
                    correctional_multiplier = -10/left_speed
            else:
                if right_speed > 0:
                    correctional_multiplier = 10/right_speed
                else:
                    correctional_multiplier = -10/right_speed
            left_speed = left_speed * correctional_multiplier
            right_speed = right_speed * correctional_multiplier

        #left_speed = (- speed + (pointangle * 0.2)) * point_move_direction     # régi 
        #right_speed = (- speed - (pointangle * 0.2)) * point_move_direction    # régi

        if (abs(robotx - x) < 0.01 and abs(roboty - y) < 0.01):
            return True, 0, 0
        return False, left_speed, right_speed

    def rotate(self, name, data, angle, speed):
        global deg_rotated
        global prev_pos
        robot_pos = data[name]
        robot_angle = math.degrees(robot_pos['orientation'])
        prev_robot_pos = prev_pos[name]
        prev_robot_angle = math.degrees(prev_robot_pos['orientation'])
        if (angle > 0):
            turn_direction = 1
        else:
            turn_direction = -1

        diffdeg = abs(abs(robot_angle) - abs(prev_robot_angle))
        deg_rotated += diffdeg

        left_speed = turn_direction * speed
        right_speed = - turn_direction * speed

        if ((abs(angle) - deg_rotated) < 0.01):
            deg_rotated = 0
            return True, 0, 0
        return False, left_speed, right_speed

    def move(self, name, data, dist, speed):
        global dist_rolled
        global prev_pos
        robot_pos = data[name]
        prev_robot_pos = prev_pos[name]
        robotx = robot_pos['x']
        roboty = robot_pos['y']
        prev_robotx = prev_robot_pos['x']
        prev_roboty = prev_robot_pos['y']
        if (dist > 0):
            move_direction = 1
        else:
            move_direction = -1
        
        diffx = abs(robotx - prev_robotx)
        diffy = abs(roboty - prev_roboty)

        dist_rolled += math.sqrt(diffx**2 + diffy**2)
        
        left_speed = speed * move_direction * -1
        right_speed = speed * move_direction * -1
        if (abs(dist) - abs(dist_rolled) < 0.001):
            dist_rolled = 0
            return True, 0, 0
        return False, left_speed, right_speed

    def randkickofftrickshot(self, name, data):
        if (name[0] == 'B'):
            enemyteam = 'Y'
        else:
            enemyteam = 'B'
        trickshot_number = random.randint(2, 3)
        #print("Trickshot ", trickshot_number)
        trickshot_number = 3
        if (trickshot_number == 1000):
            add_coords_dest(0.05, 0.05, 7, 0)
            add_coords_dest(0.08, 0, 7, 0)
        elif (trickshot_number == 2):
            add_rotate(60, 7, 0)
            add_move(0.085, 7, 0)
            add_rotate(25, 7, 0)
            add_move(-0.1, 9, 0)
        elif (trickshot_number == 3):
            add_move(0.02, 7, 10)
            if (data[enemyteam + '3']['y'] < 0):
                if (enemyteam == 'Y'):
                    add_rotate(2, 4, 10)
                else:
                    add_rotate(-2, 4, 10)
            else:
                if (enemyteam == 'B'):
                    add_rotate(2, 4, 10)
                else:
                    add_rotate(-2, 4, 10)
            add_move(0.1, 9, 10)

    def run(self):
        raise NotImplementedError

class ORKASorccerBot(RCJSoccerRobot):
    def runGoalie(self):
        if self.team=='Y':
            team = -1 
        else:
            team = 1
        while self.robot.step(TIME_STEP) != -1:
            if self.is_new_data():
                data = self.get_new_data()
                robot_pos = data[self.name]
                ball_pos = data['ball']
                ball_angle, robot_angle = self.get_angles(ball_pos, robot_pos)
                direction = get_direction(ball_angle)
                right_speed = 0
                left_speed = 0

                x1 = 0.556 * team
                y1 = 0
                ball_x = ball_pos['x']
                ball_y = ball_pos['y']

                celpont_y = ((ball_y)*ball_x + (0.75*team-ball_x)*ball_y - (ball_y)*0.556*team) /(0.75*team-ball_x)
                celpont_x = 0.556 * team
                if celpont_y>0.3:
                    celpont_y = 0.41
                    celpont_x = (ball_y*ball_x+(0.75*team-ball_x)*ball_y-0.3*(0.75*team-ball_x))/ball_y
                elif celpont_y<-0.3:
                    celpont_y = -0.41
                    celpont_x = (ball_y*ball_x+(0.75*team-ball_x)*ball_y+0.3*(0.75*team-ball_x))/ball_y

                pointangle, point_move_direction, point_distance = self.getpointinfo(self.name, data, celpont_x, celpont_y)

                left_speed = (-7 + (pointangle*0.2)) * point_move_direction
                right_speed = (-7 - (pointangle*0.2)) * point_move_direction

                if (abs(robot_pos['x'] - x1) < 0.001 and abs(robot_pos['y'] - y1) < 0.001):
                    left_speed = 0
                    right_speed = 0

                if abs(left_speed) >= 10 or abs(right_speed) >= 10:
                    #ha bármelyik sebesség nagyobb, mint 10 visszaosztja őket, hogy 10-nél kisebbek legyenek
                    #a jobb bal sebesség arányának megtartásával, osztó sose lesz 0, nem kell kikötés 0-ra
                    if abs(left_speed) > abs(right_speed):
                        if left_speed > 0:
                            correctional_multiplier = 9.99/left_speed
                        else:
                            correctional_multiplier = -9.99/left_speed
                    else:
                        if right_speed > 0:
                            correctional_multiplier = 9.99/right_speed
                        else:
                            correctional_multiplier = -9.99/right_speed
                    left_speed = left_speed * correctional_multiplier
                    right_speed = right_speed * correctional_multiplier

                self.left_motor.setVelocity(left_speed)
                self.right_motor.setVelocity(right_speed)
            else:
                pass

    def runStriker(self):
        name = self.name
        veryfirstkickoff = True
        tick = 0
        elert = False

        if self.name[0] == 'B':
            team = 1
        else:
            team = -1
        
        while self.robot.step(TIME_STEP) != -1:
            tick+=1

            if (len(all_waypoints) > 0):
                travelling = True
            else:
                travelling = False

            if self.is_new_data():
                #kapunk-e új adatot
                self.data_previous = self.data_current
                self.data_current = self.get_new_data()  #data = self.get_new_data()
                data = self.data_current
                if self.data_previous==None:
                    self.data_previous = self.data_current

                robot_pos = data[self.name]
                ball_pos = data['ball']
                ball_angle, robot_angle = self.get_angles(ball_pos, robot_pos)
                direction = get_direction(ball_angle)
                robotatkickoff = False
                
                if (travelling):
                    #print(all_waypoints)
                    if (all_waypoints[0].movetype == "to_coords"):
                        finished, left_speed, right_speed = self.travel(self.name, data, all_waypoints[0].destx, all_waypoints[0].desty, all_waypoints[0].speed)
                    elif (all_waypoints[0].movetype == "rotate"):
                        finished, left_speed, right_speed = self.rotate(self.name, data, all_waypoints[0].angle, all_waypoints[0].speed)
                    elif (all_waypoints[0].movetype == "move"):
                        finished, left_speed, right_speed = self.move(self.name, data, all_waypoints[0].distance, all_waypoints[0].speed)

                    if (finished):
                        all_waypoints.pop(0)
                    self.left_motor.setVelocity(left_speed)
                    self.right_motor.setVelocity(right_speed)
                
                if (self.kickoffcheck(data) == 1 or veryfirstkickoff == True):
                    clearwaypoints()
                    self.left_motor.setVelocity(0)
                    self.right_motor.setVelocity(0)

                    #TODO: trickshot & kapus a kapuba
                    robotatkickoff = self.kickoffercheck(self.name, data)
                    #trickshotok
                    if (robotatkickoff):
                        #print(self.name, "AT KICKOFF")
                        self.randkickofftrickshot(self.name, data)
                elif (len(all_waypoints) == 0 or all_waypoints[0].priority != 10):
                    #game
                    #támadó játék
                    self.attack_powers['2'] = self.attack_power(self.team+'2')
                    self.attack_powers['3'] = self.attack_power(self.team+'3')

                    robot_pos = self.data_current[self.name] #data[self.name]
                    robotx = robot_pos['x']
                    roboty = robot_pos['y']

                    clearwaypoints()
                    if self.am_i_striker():
                        #csatár
                        add_coords_dest(ball_pos['x'], ball_pos['y'], 10, 0)
                    else:
                        if self.player_id == 2:
                            add_coords_dest(ball_pos['x']+0.1, ball_pos['y']+0.05, 10, 0)
                        else:
                            if tick%2 == 0:
                                add_coords_dest(0.3 * team, 0, 9, 0)
                            else:
                                add_coords_dest(0.2 * team, 0, 9, 0)
                global prev_pos
                prev_pos = data
                veryfirstkickoff = False
            else:
                #print("no data")
                pass

    def run(self):
        if self.player_id==1:
            self.runGoalie()
        else:
            self.runStriker()

my_robot = ORKASorccerBot()
my_robot.run()
