import sys
import json
import os

sys.path.append("/home/kandidatarbete/450/src/userInput")
current_file = __file__
parent_dir = os.path.dirname(current_file)
sibling_dir = os.path.join(parent_dir, "userInput")
child_file = os.path.join(sibling_dir, "paintDimension.json")
child_file_rel = os.path.relpath(child_file, current_file)

# This file can only be exceuted from the calculations directory or by rosrun am_driver main.py
def get_user_input():
    with open(child_file_rel) as paintDimensions:
        user_input = json.load(paintDimensions)
    width = round(float(user_input["shortside"]), 4)
    lenght = round(float(user_input["longside"]), 4)
    penalty_area_width = round(float(user_input["penaltyAreaWidth"]), 4)
    penalty_area_height = round(float(user_input["penaltyAreaHeight"]), 4)
    goal_box_height = round(float(user_input["goalBoxHeight"]), 4)
    goal_box_width = round(float(user_input["goalBoxWidth"]), 4)
    penalty_dot_length = round(float(user_input["penaltyDotLength"]), 4)
    center_circle_diameter = round(float(user_input["centerCircleDiameter"]), 4)
    corner_arc_radius = round(float(user_input["cornerArcRadius"]), 4)
    penalty_arc_radius = round(float(user_input["penaltyArcRadius"]), 4)
    num_comb_lines = round(float(user_input["numCombLines"]), 4)

    shortside_right = {"start": (0, 0), "end": (width, 0)}
    longside_up = {"start": (width, 0), "end": (width, lenght)}
    shortside_left = {"start": (width, lenght), "end": (0, lenght)}
    longside_down = {"start": (0, lenght), "end": (0, 0)}
    midline = {"start": (0, lenght / 2), "end": (width, lenght / 2)}
    goal_box_right_1 = {
        "start": (0, width / 2 - goal_box_width / 2),
        "end": (goal_box_height, width / 2 - goal_box_width / 2),
    }
    goal_box_right_2 = {
        "start": (goal_box_height, width / 2 - goal_box_width / 2),
        "end": (goal_box_height, width / 2 + goal_box_width / 2),
    }
    goal_box_right_3 = {
        "start": (goal_box_height, width / 2 + goal_box_width / 2),
        "end": (0, width / 2 + goal_box_width / 2),
    }
    goal_box_left_1 = {
        "start": (width, width / 2 - goal_box_width / 2),
        "end": (width - goal_box_height, width / 2 - goal_box_width / 2),
    }
    goal_box_left_2 = {
        "start": (width - goal_box_height, width / 2 - goal_box_width / 2),
        "end": (width - goal_box_height, width / 2 + goal_box_width / 2),
    }
    goal_box_left_3 = {
        "start": (width - goal_box_height, width / 2 + goal_box_width / 2),
        "end": (width, width / 2 + goal_box_width / 2),
    }
    penalty_area_height_right_1 = {
        "start": (0, width / 2 - penalty_area_width / 2),
        "end": (penalty_area_height, width / 2 - penalty_area_width / 2),
    }
    penalty_area_height_right_2 = {
        "start": (penalty_area_height, width / 2 - penalty_area_width / 2),
        "end": (penalty_area_height, width / 2 + penalty_area_width / 2),
    }
    penalty_area_height_right_3 = {
        "start": (penalty_area_height, width / 2 + penalty_area_width / 2),
        "end": (0, width / 2 + penalty_area_width / 2),
    }
    penalty_area_height_left_1 = {
        "start": (width, width / 2 - penalty_area_width / 2),
        "end": (width - penalty_area_height, width / 2 - penalty_area_width / 2),
    }
    penalty_area_height_left_2 = {
        "start": (width - penalty_area_height, width / 2 - penalty_area_width / 2),
        "end": (width - penalty_area_height, width / 2 + penalty_area_width / 2),
    }
    penalty_area_height_left_3 = {
        "start": (width - penalty_area_height, width / 2 + penalty_area_width / 2),
        "end": (width, width / 2 + penalty_area_width / 2),
    }

    paint_order = [shortside_right, longside_up, shortside_left, longside_down]
    # lines_json = {
    #     "shortside_right": shortside_right,
    #     "longside_up": longside_up,
    #     "shortside_left": shortside_left,
    #     "longside_down": longside_down,
    #     "midline": midline,
    #     "goal_box_right_1": goal_box_right_1,
    #     "goal_box_right_2": goal_box_right_2,
    #     "goal_box_right_3": goal_box_right_3,
    #     "goal_box_left_1": goal_box_left_1,
    #     "goal_box_left_2": goal_box_left_2,
    #     "goal_box_left_3": goal_box_left_3,
    #     "penalty_area_height_right_1": penalty_area_height_right_1,
    #     "penalty_area_height_right_2": penalty_area_height_right_2,
    #     "penalty_area_height_right_3": penalty_area_height_right_3,
    #     "penalty_area_height_left_1": penalty_area_height_left_1,
    #     "penalty_area_height_left_2": penalty_area_height_left_2,
    #     "penalty_area_height_left_3": penalty_area_height_left_3,
    # }
    return paint_order
