import sys
import json
import os

sys.path.append("/home/kandidatarbete/450/src/userInput")
current_file = __file__
parent_dir = os.path.dirname(current_file)
# grand_parent_dir = os.path.dirname(parent_dir)
sibling_dir = os.path.join(parent_dir, "userInput")
child_file = os.path.join(sibling_dir, "paintDimension.json")
child_file_rel = os.path.relpath(child_file, current_file)


# This file can only be exceuted from the calculations directory or by rosrun am_driver main.py
def get_paint_order():
    with open(child_file_rel) as paintDimensions:
        user_input = json.load(paintDimensions)
    width = round(float(user_input["shortside"]), 4)
    lenght = round(float(user_input["longside"]), 4)
    print("width: ", width)
    print("lenght: ", lenght)
    penalty_area_width = round(float(user_input["penaltyAreaWidth"]), 4)
    penalty_area_height = round(float(user_input["penaltyAreaHeight"]), 4)
    goal_box_height = round(float(user_input["goalBoxHeight"]), 4)
    goal_box_width = round(float(user_input["goalBoxWidth"]), 4)
    penalty_dot_length = round(float(user_input["penaltyDotLength"]), 4)
    center_circle_diameter = round(float(user_input["centerCircleDiameter"]), 4)
    corner_arc_radius = round(float(user_input["cornerArcRadius"]), 4)
    penalty_arc_radius = round(float(user_input["penaltyArcRadius"]), 4)
    num_comb_lines = round(float(user_input["numCombLines"]), 4)

    shortside_right = {"start": (0, 0), "end": (width, 0), "type": "line"}
    longside_up = {"start": (width, 0), "end": (width, lenght), "type": "line"}
    shortside_left = {"start": (width, lenght), "end": (0, lenght), "type": "line"}
    longside_down = {"start": (0, lenght), "end": (0, 0), "type": "line"}
    midline = {"start": (0, lenght / 2), "end": (width, lenght / 2), "type": "line"}
    goal_box_right_1 = {
        "start": (width / 2 - goal_box_width / 2, 0),
        "end": (width / 2 - goal_box_width / 2, goal_box_height),
        "type": "line",
    }
    # change y to x
    goal_box_right_2 = {
        "start": (width / 2 - goal_box_width / 2, goal_box_height),
        "end": (width / 2 + goal_box_width / 2, goal_box_height),
        "type": "line",
    }
    goal_box_right_3 = {
        "start": (width / 2 + goal_box_width / 2, goal_box_height),
        "end": (width / 2 + goal_box_width / 2, 0),
        "type": "line",
    }
    goal_box_left_1 = {
        "start": (width / 2 - goal_box_width / 2, lenght),
        "end": (width / 2 - goal_box_width / 2, lenght - goal_box_height),
        "type": "line",
    }
    goal_box_left_2 = {
        "start": (width / 2 - goal_box_width / 2, lenght - goal_box_height),
        "end": (width / 2 + goal_box_width / 2, lenght - goal_box_height),
        "type": "line",
    }
    goal_box_left_3 = {
        "start": (width / 2 + goal_box_width / 2, lenght - goal_box_height),
        "end": (width / 2 + goal_box_width / 2, lenght),
        "type": "line",
    }
    penalty_area_right_1 = {
        "start": (width / 2 - penalty_area_width / 2, 0),
        "end": (width / 2 - penalty_area_width / 2, penalty_area_height),
        "type": "line",
    }
    penalty_area_right_2 = {
        "start": (width / 2 - penalty_area_width / 2, penalty_area_height),
        "end": (width / 2 + penalty_area_width / 2, penalty_area_height),
        "type": "line",
    }
    penalty_area_right_3 = {
        "start": (width / 2 + penalty_area_width / 2, penalty_area_height),
        "end": (width / 2 + penalty_area_width / 2, 0),
        "type": "line",
    }
    penalty_area_left_1 = {
        "start": (width / 2 - penalty_area_width / 2, lenght),
        "end": (width / 2 - penalty_area_width / 2, lenght - penalty_area_height),
        "type": "line",
    }
    penalty_area_left_2 = {
        "start": (width / 2 - penalty_area_width / 2, lenght - penalty_area_height),
        "end": (width / 2 + penalty_area_width / 2, lenght - penalty_area_height),
        "type": "line",
    }
    penalty_area_left_3 = {
        "start": (width / 2 + penalty_area_width / 2, lenght - penalty_area_height),
        "end": (width / 2 + penalty_area_width / 2, lenght),
        "type": "line",
    }
    center_circle = {
        "start": (width / 2 - center_circle_diameter / 2, lenght / 2),
        "end": (width / 2 + center_circle_diameter / 2, lenght / 2),
        "center": (width / 2, lenght / 2),
        "radius": center_circle_diameter / 2,
        "type": "circle",
    }
    corner_arc_right_up = {
        "start": (lenght - corner_arc_radius, 0),
        "end": (lenght, corner_arc_radius),
        "center": (lenght, 0),
        "radius": corner_arc_radius,
        "type": "circle",
    }
    corner_arc_right_down = {
        "start": (lenght - corner_arc_radius, width),
        "end": (lenght, width - corner_arc_radius),
        "center": (lenght, width),
        "radius": corner_arc_radius,
        "type": "circle",
    }
    corner_arc_left_up = {
        "start": (0, corner_arc_radius),
        "end": (corner_arc_radius, 0),
        "center": (0, 0),
        "radius": corner_arc_radius,
        "type": "circle",
    }
    corner_arc_left_down = {
        "start": (0, width - corner_arc_radius),
        "end": (corner_arc_radius, width),
        "center": (0, width),
        "radius": corner_arc_radius,
        "type": "circle",
    }

    paint_order = [
        longside_up,
        shortside_left,
        longside_down,
        shortside_right,
        midline,
        goal_box_right_1,
        goal_box_right_2,
        goal_box_right_3,
        goal_box_left_1,
        goal_box_left_2,
        goal_box_left_3,
        penalty_area_right_1,
        penalty_area_right_2,
        penalty_area_right_3,
        penalty_area_left_1,
        penalty_area_left_2,
        penalty_area_left_3,
        center_circle,
        corner_arc_right_down,
        corner_arc_right_up,
        corner_arc_left_down,
        corner_arc_left_up,
    ]
    corner_arc_left_down = {
        "start": (0, 0),
        "end": (2, 0),
        "center": (1, 0),
        "radius": 1,
        "type": "circle",
    }
    # paint_order = [corner_arc_left_down]
    return paint_order
