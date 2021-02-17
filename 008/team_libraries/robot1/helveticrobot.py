import sys
from pathlib import Path
sys.path.append(str(Path('.').absolute().parent))
sys.path.append('/app/controllers')

# rcj_soccer_player controller - ROBOT B1

# Feel free to import built-in libraries
import math

# You can also import scripts that you put into the folder with controller
from team_008_libraries.robot1.rcj_soccer_robot import RCJSoccerRobot, TIME_STEP
from team_008_libraries.robot1 import utils, job, helveticmath, environment


class Helveticrobot(RCJSoccerRobot):
    def __init__(self):
        super().__init__()

        # Prepare vars
        self.side = 1 if self.team == "B" else -1
        self.goal_pos = {"x": 0.73 * self.side, "y": 0}

        # Prepare the job instances
        self.striker_job = job.StrikerJob(self)
        self.goalkeeper_job = job.GoalkeeperJob(self)

        # Prepare environment scanner
        self.environment = environment.Environment(self)
        self.mates_metas = None
        self.fp_meta = None

    def run(self):
        while self.robot.step(TIME_STEP) != -1:
            if self.is_new_data():
                data = self.get_new_data()

                # Analyze positions
                self.mates_metas = self.analyze_positions(data)
                self.fp_meta = self.mates_metas[self.name]

                # Get the according job instance
                job = None
                if self.fp_meta["job"] == "striker":
                    job = self.striker_job
                elif self.fp_meta["job"] == "goalkeeper":
                    job = self.goalkeeper_job

                self.environment.scan(data)

                job.run(data)

    def analyze_positions(self, data):
        mates_metas = {}
        mates_names = [self.team + str(m) for m in range(1, 4)]

        # Setup basic metas for bots
        for mate_name in mates_names:
            mates_metas[mate_name] = self.analyze_position(mate_name, data)

        self.determine_ball_ranks(mates_metas, data)
        self.determine_jobs(mates_metas, data)

        return mates_metas

    def determine_ball_ranks(self, mates_metas, data):
        # Determine jobs
        left_names = list(dict.keys(mates_metas))

        for i in range(len(left_names)):
            goalkeeper_name = None
            for ln in left_names:
                if goalkeeper_name is None:
                    goalkeeper_name = ln
                else:
                    gk_ball_distance = mates_metas[goalkeeper_name]["ball_distance"]
                    l_ball_distance = mates_metas[ln]["ball_distance"]
                    if l_ball_distance < gk_ball_distance:
                        goalkeeper_name = ln
            mates_metas[goalkeeper_name]["ball_rank"] = i
            left_names.remove(goalkeeper_name)

    def determine_jobs(self, mates_metas, data):
        # Determine jobs
        left_names = list(dict.keys(mates_metas))

        # Determine the goalkeeper
        goalkeeper_name = self.determine_goalkeeper(left_names, data)
        mates_metas[goalkeeper_name]["job"] = "goalkeeper"
        left_names.remove(goalkeeper_name)

        # Determine the first striker
        striker1_name = self.determine_striker(left_names, data)
        mates_metas[striker1_name]["job"] = "striker"
        left_names.remove(striker1_name)

        # Determine the second striker
        striker2_name = self.determine_striker(left_names, data)
        mates_metas[striker2_name]["job"] = "striker"
        left_names.remove(striker2_name)

    def analyze_position(self, name, data):
        # One nearest to the goal: Goalkeeper
        # One nearest to the ball (not goalkeeper): Striker
        # Third one: Striker

        ball_line = (data[name], data["ball"])
        try:
            ball_line_goal_line_intersect_pos = helveticmath.line_intersection(self.environment.goal_line, ball_line, True)
        except Exception:
            ball_line_goal_line_intersect_pos = None

        return {
            "name": name,
            "position": data[name],
            "ball_distance": helveticmath.distance(data[name], data["ball"]),
            "in_control": (data["ball"]["x"] - data[name]["x"]) * self.side < 0,
            "losing_control": not (data["ball"]["x"] - (data[name]["x"] + 0.0375 * self.side)) * self.side < 0,
            "ball_line": ball_line,
            "ball_line_goal_line_intersect_pos": ball_line_goal_line_intersect_pos
        }

    def determine_goalkeeper(self, left_names, data):
        goalkeeper_name = None
        for ln in left_names:
            if goalkeeper_name is None:
                goalkeeper_name = ln
            else:
                gkdata = data[goalkeeper_name]
                ldata = data[ln]
                gkdistance = helveticmath.distance(self.goal_pos, gkdata)
                ldistance = helveticmath.distance(self.goal_pos, ldata)
                if ldistance < gkdistance:
                    goalkeeper_name = ln
        return goalkeeper_name

    def determine_striker(self, left_names, data):
        striker = None
        balldata = data["ball"]
        for ln in left_names:
            if striker is None:
                striker = ln
            else:
                gkdata = data[striker]
                ldata = data[ln]
                gkdistance = helveticmath.distance(balldata, gkdata)
                ldistance = helveticmath.distance(balldata, ldata)
                if ldistance < gkdistance:
                    striker = ln
        return striker
