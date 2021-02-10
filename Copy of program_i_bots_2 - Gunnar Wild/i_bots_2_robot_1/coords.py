## goal_pos
TOR_POS_MIDDLE = {"x" : 0.74, "y" : 0}

own_goal_pos = {"x" : -0.75, "y" : 0}

center_pos = {"x" : 0, "y" : 0}

## spielfeld coords
#def field_coords (ball_pos: dict) -> float:
#    one_a_ball = {}
#    one_a_ball = ball_pos["x"] >= 0.53 and ball_pos["x"] <= 0.75 and ball_pos["y"] <= -0.2 
    
#    one_b = {}
#    one_b = ball_pos["x"] >= 0.27 and ball_pos["x"] <= 0.53 and ball_pos["y"] <= -0.2

#    one_c = {}
#    one_c = ball_pos["x"] >= 0 and ball_pos["x"] <= 0.27 and ball_pos["y"] <= -0.2

#    one_d = {}
#    one_d = ball_pos["x"] <= 0 and ball_pos["x"] >= -0.27 and ball_pos["y"] <= -0.2 

#    one_e = {}    
#    one_e = ball_pos["x"] <= -0.27 and ball_pos["x"] >= -0.53  and ball_pos["y"] <= -0.2

#    one_f = {}
#    one_f = ball_pos["x"] <= -0.53 and ball_pos["x"] >= -0.75  and ball_pos["y"] <= -0.2
   

#    two_a = ball_pos["x"] >= 0.53 and ball_pos["x"] <= 0.75 and ball_pos["y"] <= 0.2 and ball_pos["y"] >= -0.2
#    two_b = ball_pos["x"] >= 0.27 and ball_pos["x"] <= 0.53 and ball_pos["y"] <= 0.2 and ball_pos["y"] >= -0.2
#    two_c = ball_pos["x"] >= 0 and ball_pos["x"] <= 0.27 and ball_pos["y"] <= 0.2 and ball_pos["y"] >= -0.2
#    two_d = ball_pos["x"] <= 0 and ball_pos["x"] >= -0.27 and ball_pos["y"] <= 0.2 and ball_pos["y"] >= -0.2
#    two_e = ball_pos["x"] <= -0.27 and ball_pos["x"] >= -0.53 and ball_pos["y"] <= 0.2 and ball_pos["y"] >= -0.2
#    two_f = ball_pos["x"] <= -0.53 and ball_pos["x"] >= -0.75 and ball_pos["y"] <= 0.2 and ball_pos["y"] >= -0.2

#    three_a = ball_pos["x"] >= 0.53 and ball_pos["x"] <= 0.75 and ball_pos["y"] >= 0.2
#    three_b = ball_pos["x"] >= 0.27 and ball_pos["x"] <= 0.53 and ball_pos["y"] >= 0.2
#    three_c = ball_pos["x"] >= 0 and ball_pos["x"] <= 0.27 and ball_pos["y"] >= 0.2
#    three_d = ball_pos["x"] <= 0 and ball_pos["x"] >= -0.27 and ball_pos["y"] >= 0.2
#    three_e = ball_pos["x"] <= -0.27 and ball_pos["x"] >= -0.53 and ball_pos["y"] >= 0.2
#    three_f = ball_pos["x"] <= -0.53 and ball_pos["x"] >= -0.75 and ball_pos["y"] >= 0.2
    
#    anamy_field = ball_pos["x"] >= 0

    ###############################
    #    :    :    :    :    :    # 
    # 1a : 1b : 1c : 1d : 1e : 1f #   
    #    :    :    :    :    :    # 
#####-----------------------------#####
#   §    :    :    :    :    :    §   #  
#   § 2a : 2b : 2c : 2d : 2e : 2f §   #  
#   §    :    :    :    :    :    §   #  
#####-----------------------------#####
    #    :    :    :    :    :    # 
    # 3a : 3b : 3c : 3d : 3e : 3f # 
    #    :    :    :    :    :    # 
    ###############################
