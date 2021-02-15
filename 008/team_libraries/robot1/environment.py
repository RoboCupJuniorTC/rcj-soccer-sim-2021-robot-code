from . import helveticmath
from .rcj_soccer_robot import TIME_STEP
import math


class Environment():
    def __init__(self, helveticrobot):
        # Save helveticrobot
        self.helveticrobot = helveticrobot

        # Prepare vars
        self.last = None
        self.ball_speed = 0

        penalty_area_main_laser_line_x = self.helveticrobot.side * 0.5
        self. penalty_area_main_laser_line = (
            {"x": penalty_area_main_laser_line_x, "y": -0.45}, {"x": penalty_area_main_laser_line_x, "y": 0.45})
        self.penalty_area_main_laser_line_intersect_pos = None

        penalty_area_upper_laser_line_x_1 = self.helveticrobot.side * 0.5
        penalty_area_upper_laser_line_x_2 = self.helveticrobot.side * 1
        self.penalty_area_upper_laser_line = (
            {"x": penalty_area_upper_laser_line_x_1, "y": 0.45}, {"x": penalty_area_upper_laser_line_x_2, "y": 0.45})
        self.penalty_area_upper_laser_line_intersect_pos = None

        penalty_area_lower_laser_line_x_1 = self.helveticrobot.side * 0.5
        penalty_area_lower_laser_line_x_2 = self.helveticrobot.side * 1
        self.penalty_area_lower_laser_line = (
            {"x": penalty_area_lower_laser_line_x_1, "y": -0.45}, {"x": penalty_area_lower_laser_line_x_2, "y": -0.45})
        self.penalty_area_lower_laser_line_intersect_pos = None

        self.center_line = (
            {"x": 0, "y": -1}, {"x": 0, "y": 1})
        self.center_line_intersect_pos = None

        # Goal line. Would be 0.2 but we’ve used 0.3 so that it reacts earlier
        self.goal_line = ({"x": 0.75 * self.helveticrobot.side, "y": -0.3},
                          {"x": 0.75 * self.helveticrobot.side, "y": 0.3})

        self.ball_direction_correct = False
        self.ball_side_correct = False

        # Progress Checkers
        self.ball_progress_checker_steps = 157
        self.ball_progress_checker_samples = [
            0 for _ in range(self.ball_progress_checker_steps)]
        self.ball_progress_checker_iterator = 0
        self.ball_healthbar = 10

    def scan(self, data):
        if self.last:
            current_ball_pos = data["ball"]
            last_ball_pos = self.last["ball"]

            self.ball_speed = helveticmath.distance(
                current_ball_pos, last_ball_pos)

            delta_x = current_ball_pos["x"] - last_ball_pos["x"]
            self.ball_direction_correct = ((self.helveticrobot.team == "B" and delta_x < 0) or (
                self.helveticrobot.team == "Y" and delta_x > 0))
            self.ball_side_correct = ((self.helveticrobot.team == "B" and current_ball_pos["x"] < 0) or (
                self.helveticrobot.team == "Y" and current_ball_pos["x"] > 0))

            # Calculate ball line (used for intersections)
            ball_line = (last_ball_pos, current_ball_pos)

            # Calculate penalty area main laser line intersection
            try:
                self.penalty_area_main_laser_line_intersect_pos = helveticmath.line_intersection(
                    self.penalty_area_main_laser_line, ball_line, True)
            except Exception:
                self.penalty_area_main_laser_line_intersect_pos = None

            # Calculate penalty area upper laser line intersection
            try:
                self.penalty_upper_laser_line_intersect_pos = helveticmath.line_intersection(
                    self.penalty_area_upper_laser_line, ball_line, True)
            except Exception:
                self.penalty_upper_laser_line_intersect_pos = None

            # Calculate penalty area lower laser line intersection
            try:
                self.penalty_lower_laser_line_intersect_pos = helveticmath.line_intersection(
                    self.penalty_area_lower_laser_line, ball_line, True)
            except Exception:
                self.penalty_lower_laser_line_intersect_pos = None

            # Calculate center line intersection
            try:
                self.center_line_intersect_pos = helveticmath.line_intersection(
                    self.center_line, ball_line, False)

                if abs(self.center_line_intersect_pos["y"]) > 0.65:
                    self.center_line_intersect_pos["y"] = self.center_line_intersect_pos["y"] - (abs(
                        self.center_line_intersect_pos["y"]) - 0.65) * (-1 if self.center_line_intersect_pos["y"] > 0 else 1)
            except Exception:
                self.center_line_intersect_pos = None

            # Process progress checker
            self.ball_progress_checker_track(data["ball"])

        self.last = data

    def ball_progress_checker_track(self, position):
        if not self.last:
            return

        delta = helveticmath.distance(self.last["ball"], position)

        self.ball_progress_checker_samples[self.ball_progress_checker_iterator %
                                           self.ball_progress_checker_steps] = delta
        self.ball_progress_checker_iterator += 1

        s = sum(self.ball_progress_checker_samples)

        if self.ball_progress_checker_iterator < self.ball_progress_checker_steps:
            self.ball_healthbar = 10
        else:
            self.ball_healthbar = s * 10 - 5

        if self.ball_healthbar < 0 or self.ball_healthbar > 10:
            self.ball_healthbar = 10
