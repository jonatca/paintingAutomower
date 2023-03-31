import sys
import json
import os

#använd egen filepath till userInput
sys.path.append("/Users/emili/OneDrive/Dokument/GitHub/paintingAutomower/userInput")
current_file = __file__
parent_dir = os.path.dirname(current_file)
# grand_parent_dir = os.path.dirname(parent_dir)
sibling_dir = os.path.join(parent_dir, "userInput")
child_file = os.path.join(sibling_dir, "paintDimension.json")
child_file_rel = os.path.relpath(child_file, current_file)

def get_comb_cut_order():
    with open(child_file_rel) as paintDimensions:
        user_input = json.load(paintDimensions)
    width = round(float(user_input["shortside"]), 4)
    lenght = round(float(user_input["longside"]), 4)
    print("width: ", width)
    print("lenght: ", lenght)
    num_comb_lines = round(int(user_input["numCombLines"]), 4)

    width_combing = lenght / num_comb_lines 
    length_combing = width 
    width_comb = 0.3
    num_combs_per_area = int(width_combing / width_comb)
    
    # köra upp på första "ruta" sen ner på andra sen upp på tredje osv. 
    # alternativt upp första ner andra sen upp första igen fast en bredd tidigare
    # minsta antal trips över planen?: (längden på planen / bredden på kammen)
    # vad göra om ej jämnt delbar bredd på ruta, få mer överlapp nära kanten
    
    #Lägga till målpunkter i lista comb_cut_order. loopa målpunkter för
    #TODO Få det att funka för både udda och jämnt num_comb_lines 
    comb_cut_order = []
    for k in range(num_combs_per_area):
        for i in range(num_comb_lines):
            if not i % 2:
                x1_e = 0
                x2_e = width
                y1_e = i*width_combing + k*width_comb
                y2_e = y1_e
                trip_e = {"start": (x1_e, y1_e), "end": (x2_e, y2_e), "type": "line"}
                comb_cut_order.append(trip_e)
                to_next_e = {"start": (x2_e, y2_e), "end": (x2_e, y2_e+width_combing), "type": "line"}
                comb_cut_order.append(to_next_e)
            else:
                x1_o = width
                x2_o = 0
                y1_o = i*width_combing + k*width_comb
                y2_o = y1_o
                trip_o = {"start": (x1_o, y1_o), "end": (x2_o, y2_o), "type": "line"}
                comb_cut_order.append(trip_o)
                if i != (num_comb_lines-1):
                    to_next_o = {"start": (x2_o, y2_o), "end": (x2_o, y2_o+width_combing), "type": "line"}
                    comb_cut_order.append(to_next_o)
                else:
                    to_start = {"start": (x2_o, y2_o), "end": (0, 0+k*width_comb), "type": "line"}
                    comb_cut_order.append(to_start)

    
    return comb_cut_order
