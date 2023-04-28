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

#after_end = turn270flag(width, 0, 'x') + [line1] + turn270()
# This file can only be exceuted from the calculations directory or by rosrun am_driver main.py
def get_paint_order():
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

    shortside_down = {"end": (width, 0),"after_end": turn270flag(width,0,'x'), "type": "line"}
    longside_right = {"end": (width, lenght), "type": "line"}
    shortside_up = {"end": (0, lenght), "type": "line"}
    longside_left = {"end": (0, 0), "type": "line"}
    line_to_penalty_area_right_1 = {"end": (width / 2 - penalty_area_width / 2, 0), "type": "line"}
    line_to_goal_box_right_1 = {"end": (width / 2 + goal_box_width / 2, 0), "type": "line"}
    line_to_penalty_dot_right = {"end": (width / 2, penalty_dot_length), "type": "line"}
    line_to_circle_penalty_area_right = {"end": (width / 2 +  penalty_arc_radius/2, penalty_area_height), "type": "line"}
    line_to_circle_penalty_area_right2 = {"end": (width / 2 -  penalty_arc_radius/2, penalty_area_height), "type": "line"}
    line_to_midline = {"end": (0, lenght/2), "type": "line"}
    midline_dot = {"start": (0, lenght/2), "end": (width/2, lenght / 2), "type": "line"}
    midline_rest = {"start": (width/2, lenght / 2), "end": (width, lenght / 2), "type": "line"}
    line_to_mid_circle = { "end": (width/2 + center_circle_diameter, lenght / 2), "type": "line" }
    line_to_penalty_area_left = { "end": (width/2 + penalty_area_width/2, lenght - penalty_area_height), "type": "line" }
    line_to_goal_box_left2 = { "end": (width / 2 + goal_box_width / 2, lenght),"type": "line" }
    line_to_penalty_area_left2 = { "end": (width / 2 - penalty_area_width / 2, lenght),"type": "line" }
    line_to_circle_penalty_area_left = {"end": (width / 2 +  penalty_arc_radius/2, lenght - penalty_area_height), "type": "line"}
    line_to_circle_penalty_area_left2 = {"end": (width / 2 -  penalty_arc_radius/2, lenght - penalty_area_height), "type": "line"}
    line_to_penalty_dot_left = {"end": (width / 2, lenght - penalty_dot_length), "type": "line"}
   
   
    goal_box_right_1 = {
        "start": (width / 2 - goal_box_width / 2, goal_box_height),
        "end": (width / 2 - goal_box_width / 2, 0),
        "type": "line",
    }
    # change y to x
    goal_box_right_2 = {
        "start": (width / 2 + goal_box_width / 2, goal_box_height),
        "end": (width / 2 - goal_box_width / 2, goal_box_height),
        "type": "line",
    }
    goal_box_right_3 = {
        "start": (width / 2 + goal_box_width / 2, 0),
        "end": (width / 2 + goal_box_width / 2, goal_box_height),
        "type": "line",
    }
    goal_box_left_1 = {
        "start": (width / 2 - goal_box_width / 2, lenght- goal_box_height),
        "end": (width / 2 - goal_box_width / 2, lenght),
        "type": "line",
    }
    goal_box_left_2 = {
        "start": (width / 2 + goal_box_width / 2, lenght - goal_box_height),
        "end": (width / 2 - goal_box_width / 2, lenght - goal_box_height),
        "type": "line",
    }
    goal_box_left_3 = {
        "start": (width / 2 + goal_box_width / 2, lenght),
        "end": (width / 2 + goal_box_width / 2, lenght- goal_box_height),
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
        "start": (width / 2 + center_circle_diameter / 2, lenght / 2),
        "end": (width / 2 - center_circle_diameter / 2, lenght / 2),
        "center": (width / 2, lenght / 2),
        "radius": center_circle_diameter / 2,
        "type": "circle",
        "direction": "positive"
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
    test_circle = {
        "end": (1, 1),
        "center": (1, 0),
        "radius": 1,
        "type": "circle",
        "direction": "positive",
    }
    len_square = 4
    test_line1 = {
        "end": (len_square, 0),
        "type": "line",
    }
    test_line2 = {
        "end": (len_square, -len_square) ,
        "type": "line",
    }
    test_line3 = {
        "end": (0, len_square) ,
        "type": "line",
    }
    test_line4 = {
        "end": (0, 0) ,
        "type": "line",
    }

    

    paint_order = [
        # test_circle
        test_line1,
        test_line2,
        # test_line3,
        # test_line4,
        # test_line2
        # shortside_down,
        # longside_right,
        # shortside_up,
        # longside_left,
        # line_to_penalty_area_right_1,
        # penalty_area_right_1,
        # penalty_area_right_2,
        # penalty_area_right_3,
        # line_to_goal_box_right_1,
        # goal_box_right_3,
        # goal_box_right_2,
        # goal_box_right_1,
        # line_to_penalty_dot_right,
        # line_to_circle_penalty_area_right,
        # line_to_circle_penalty_area_right2,
        # line_to_midline,
        # midline_dot,
        # midline_rest,
        # line_to_mid_circle,
        # #center_circle,
        # line_to_penalty_area_left,
        # penalty_area_left_3,
        # line_to_goal_box_left2,
        # goal_box_left_3,
        # goal_box_left_2,
        # goal_box_left_1,
        # line_to_penalty_area_left2,
        # penalty_area_left_1,
        # penalty_area_left_2,
        # line_to_circle_penalty_area_left,
        # line_to_circle_penalty_area_left2,
        # line_to_penalty_dot_left



        
        #goal_box_left_1,
        #goal_box_left_2,
        #goal_box_left_3,
        #penalty_area_right_1,
       # penalty_area_right_2,
        #penalty_area_right_3,
       # penalty_area_left_1,
       # penalty_area_left_2,
       # penalty_area_left_3,
       # center_circle,
       # corner_arc_right_up,
       # corner_arc_left_down,
       # corner_arc_left_up,
    ]
    #shortside_down = {
     #   "end": (0,-2),
      #  "type": "line",
       # "after_end": turn270flag(0,-2,'-y')

    #}
    
    
    #paint_order = [shortside_down]
    print("paint_order", paint_order)
    return paint_order
def turn270(x, y, travel_dir):
    if travel_dir == 'x':
        x1 = x+1
        y1 = y
        x2 = x
        y2 = y-1
        x3 = x
        y3 = y
    elif travel_dir == 'y':
        x1 = x
        y1 = y+1    
        x2 = x+1
        y2 = y
        x3 = x
        y3 = y
    return  [{
        "start": (x, y),
        "end": (x1, y1),
        "type": "line",
    },
    {
        "start": (x1, y1),
        "end": (x,y-1),
        "center": (x+1,y-1),
        "radius": 1,
        "type": "circle",
        "direction": "negative"
        },
        {
        "start": (x,y-1),
        "end":(x,y),
        "type": "line"
        },]

def turn270flag(x, y, travel_dir):
    if travel_dir == 'x':
        x1 = x-1
        y1 = y-1
        x2 = x-1
        y2 = y
        x3 = x
        y3 = y+1
        x4 = x+1
        y4 = y+1

        x5 = x
        y5 = y-1
        x6 = x+1
        y6 = y    
    elif travel_dir == '-x':
        x1 = x+1
        y1 = y+1
        x2 = x+1
        y2 = y
        x3 = x
        y3 = y-1
        x4 = x-1
        y4 = y-1

        x5 = x
        y5 = y+1
        x6 = x-1
        y6 = y
    elif travel_dir == 'y':
        x1 = x+1
        y1 = y-1
        x2 = x
        y2 = y-1
        x3 = x-1
        y3 = y
        x4 = x-1
        y4 = y+1

        x5 = x+1
        y5 = y
        x6 = x
        y6 = y+1
    elif travel_dir == '-y':
        x1 = x-1
        y1 = y+1
        x2 = x
        y2 = y+1
        x3 = x+1
        y3 = y
        x4 = x+1
        y4 = y-1

        x5 = x-1
        y5 = y
        x6 = x
        y6 = y-1



    return  [
        {
        "end": (x1,y1),
        "center": (x5,y5),
        "radius": 1,
        "type": "circle",
        "direction": "negative"
        },
        {
        "end":(x2,y2),
        "type": "line"
        },
        {
         "end":(x3,y3),
         "center":(x,y),
         "radius": 1,
         "type": "circle",
         "direction": "negative"
         },
         {
         "end": (x4,y4),
         "type": "line"
         },
         {
         "end": (x,y),
         "center":(x6,y6),
         "radius": 1,
         "type": "circle",
         "direction": "negative"
         }

        
        
        ]

    #elif travel_dir == 'y':
     #   x1 = x
      #  y1 = y+1    
       # x2 = x+1
        #y2 = y
        #x3 = x
        #y3 = y


# def get_turn():
#     [{
#         "start": (0, 0),
#         "end": (1,0),
#         "type": "line",
#     },
#     {
#         "start": (1, 0),
#         "end": (0,-1),
#         "center": (1,-1),
#         "radius": 1,
#         "type": "circle",
#         "direction": "negative"
#     },
#     {
#         "start": (0,-1),
#         "end":(0,0),
#         "type": "line"
#     }]