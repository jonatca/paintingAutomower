import sys
import json
import os
#def comb_lines(width, lenght):  # the lines on a soccer field
#    side = [(0, 0), (width, 0)]
#    offset = 0.25 # width of comber
#    #width of one comb is 5.5 m
#    #hej
   
sys.path.append("/home/kandidatarbete/450/src/userInput")
current_file = __file__
parent_dir = os.path.dirname(current_file)
# grand_parent_dir = os.path.dirname(parent_dir)
sibling_dir = os.path.join(parent_dir, "userInput")
child_file = os.path.join(sibling_dir, "paintDimension.json")
child_file_rel = os.path.relpath(child_file, current_file)

def get_user_input():
    with open(child_file_rel) as paintDimensions:
        user_input = json.load(paintDimensions)
    width = round(float(user_input["shortside"]), 4)
    lenght = round(float(user_input["longside"]), 4)
    print("width: ", width)
    print("lenght: ", lenght)
    num_comb_lines = round(float(user_input["numCombLines"]), 4)

    width_combing = lenght / num_comb_lines 
    length_combing = width
    width_comb = any
    num_combs_per_area = width_combing / width_comb
    
    # köra upp på första "ruta" sen ner på andra sen upp på tredje osv. 
    # alternativt upp första ner andra sen upp första igen fast en bredd tidigare
    # minsta antal trips över planen?: (längden på planen / bredden på kammen)
    # vad göra om ej jämnt delbar bredd på ruta, gå mer överlapp nära kanten

    first_trip = {"start": (0, 0), "end": (width, 0), "type": "line"}
    goto_next ={"start": (width, 0), "end": (width, (width_combing+width_comb)), "type": "line"}
    snd_trip = {"start": (width, (width_combing+width_comb)), "end": (0, (width_combing+width_comb)), "type": "line"}
