import utils
import helveticmath


class Job:
    def __init__(self, helveticrobot):
        # Prepare vars
        self.helveticrobot = helveticrobot

    def run(self, data):
        pass


class StrikerJob(Job):
    def __init__(self, helveticrobot):
        super().__init__(helveticrobot)

    def run(self, data):
        # Get the position of our robot
        robot_pos = data[self.helveticrobot.name]
        ball_pos = data["ball"]

        # Get the position of the ball
        target_position = ball_pos

        if self.helveticrobot.environment.ball_side_correct:
            if not self.helveticrobot.environment.ball_direction_correct:
                # When the ball is in the opposite side but is moving to our own side
                # HOWEVER: Out of the strikers not losing control, the robot nearest to the ball should continue kicking the ball
                ball_distance = helveticmath.distance(robot_pos, ball_pos)
                strikers = list(dict.keys(self.helveticrobot.mates_metas))
                nearest_striker_not_losing_control_meta = None
                for s in strikers:
                    s_meta = self.helveticrobot.mates_metas[s]
                    if s_meta["job"] == "striker":
                        if not s_meta["losing_control"]:
                            if not nearest_striker_not_losing_control_meta:
                                nearest_striker_not_losing_control_meta = s_meta
                            else:
                                if s_meta["ball_distance"] < nearest_striker_not_losing_control_meta["ball_distance"]:
                                    nearest_striker_not_losing_control_meta = s_meta

                if nearest_striker_not_losing_control_meta and nearest_striker_not_losing_control_meta["name"] == self.helveticrobot.name:
                    target_position = ball_pos
                elif ball_distance < 0.15 and not self.helveticrobot.fp_meta["losing_control"]:
                    target_position = ball_pos
                else:
                    target_position = self.helveticrobot.environment.center_line_intersect_pos

        if ((not self.helveticrobot.environment.ball_side_correct) and
                (not self.helveticrobot.fp_meta["in_control"]) and
                helveticmath.distance(robot_pos, ball_pos) < 0.1 and
                helveticmath.distance(target_position, ball_pos) < 0.1 and
                self.helveticrobot.fp_meta["ball_line_goal_line_intersect_pos"]):
            target_position = {
                "x": robot_pos["x"] - 1 * self.helveticrobot.side, "y": robot_pos["y"]}

        # Print the shit
        # print(self.helveticrobot.team_mates)

        # Get angle between the robot and the ball
        # and between the robot and the north
        ball_angle, robot_angle = self.helveticrobot.get_angles(
            target_position, robot_pos)

        # Compute the speed for motors
        direction = utils.get_direction(ball_angle)

        # If the robot has the ball right in front of it, go forward,
        # rotate otherwise
        if direction == 0:
            left_speed = -10
            right_speed = -10
        elif direction == 2:
            left_speed = 10
            right_speed = 10
        else:
            left_speed = direction * 4
            right_speed = direction * -4

        # Set the speed to motors
        self.helveticrobot.left_motor.setVelocity(left_speed)
        self.helveticrobot.right_motor.setVelocity(right_speed)


class GoalkeeperJob(Job):
    def __init__(self, helveticrobot):
        super().__init__(helveticrobot)

        # Prepare vars
        self.goalkeeper_pos = {"x": 0.55 * helveticrobot.side, "y": 0}
        self.suicide_pos = {"x": 0.8 * helveticrobot.side, "y": 0}

    def run(self, data):
        # Get the position of our robot
        robot_pos = data[self.helveticrobot.name]
        ball_pos = data["ball"]

        if self.helveticrobot.environment.ball_side_correct:
            target_y = ball_pos["y"]
            max_y = 0.3
            if target_y > max_y:
                target_y = max_y
            elif target_y < -max_y:
                target_y = -max_y

            target_position = {
                "x": self.goalkeeper_pos["x"], "y": target_y}
        else:
            # Get the position of the ball
            target_positions = []
            if self.helveticrobot.environment.penalty_area_main_laser_line_intersect_pos:
                target_positions.append(
                    self.helveticrobot.environment.penalty_area_main_laser_line_intersect_pos)
            if self.helveticrobot.environment.penalty_area_upper_laser_line_intersect_pos:
                target_positions.append(
                    self.helveticrobot.environment.penalty_area_upper_laser_line_intersect_pos)
            if self.helveticrobot.environment.penalty_area_lower_laser_line_intersect_pos:
                target_positions.append(
                    self.helveticrobot.environment.penalty_area_lower_laser_line_intersect_pos)

            target_position = utils.get_nearest_position(
                robot_pos, target_positions)

            if self.helveticrobot.fp_meta["ball_rank"] == 0 and self.helveticrobot.fp_meta["in_control"]:
                target_position = ball_pos

            if (self.helveticrobot.fp_meta["losing_control"] and
                    self.helveticrobot.fp_meta["ball_distance"] < 0.1):
                if self.helveticrobot.fp_meta["ball_line_goal_line_intersect_pos"]:
                    target_position = {
                        "x": robot_pos["x"] - 1 * self.helveticrobot.side, "y": robot_pos["y"]}
                else:
                    target_position = ball_pos

            if not target_position:
                target_y = ball_pos["y"] - 0.1 * \
                    (1 if ball_pos["y"] > 1 else -1)

                target_y = target_y * 0.5

                target_x = self.goalkeeper_pos["x"]
                if abs(ball_pos["x"]) > abs(target_x):
                    target_x = ball_pos["x"] + 0.1 * self.helveticrobot.side

                target_position = {
                    "x": target_x, "y": target_y}

        if self.helveticrobot.environment.ball_healthbar < 2:
            if self.helveticrobot.environment.ball_side_correct or abs(ball_pos["x"]) < 0.5:
                target_position = self.goalkeeper_pos

        # Print the shit
        # print(self.helveticrobot.team_mates)

        # Get angle between the robot and the ball
        # and between the robot and the north
        ball_angle, robot_angle = self.helveticrobot.get_angles(
            target_position, robot_pos)

        # Compute the speed for motors
        direction = utils.get_direction(ball_angle)

        # If the robot has the ball right in front of it, go forward,
        # rotate otherwise
        if direction == 0:
            left_speed = -10
            right_speed = -10
        elif direction == 2:
            left_speed = 10
            right_speed = 10
        else:
            left_speed = direction * 4
            right_speed = direction * -4

        # Set the speed to motors
        self.helveticrobot.left_motor.setVelocity(left_speed)
        self.helveticrobot.right_motor.setVelocity(right_speed)
