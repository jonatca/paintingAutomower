import sys
import json
import os
#def comb_lines(width, lenght):  # the lines on a soccer field
#    side = [(0, 0), (width, 0)]
#    offset = 0.25 # width of comber
#    #width of one comb is 5.5 m
#    #hej
   
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
    num_combs_per_area = width_combing / width_comb
    
    # köra upp på första "ruta" sen ner på andra sen upp på tredje osv. 
    # alternativt upp första ner andra sen upp första igen fast en bredd tidigare
    # minsta antal trips över planen?: (längden på planen / bredden på kammen)
    # vad göra om ej jämnt delbar bredd på ruta, gå mer överlapp nära kanten

    #def list_of_goals():
        

    list = []
    i = 0
    for k in range(0,num_comb_lines//4):
        trip = {"start": (0, 0), "end": (width, (k+i)*width_combing), "type": "line"}
        goto_next = {"start": (width, 0), "end": (width, ((k+i+1)*width_combing)), "type": "line"}
        trip2 = {"start": (width, ((k+i+1)*width_combing)), "end": (0, ((k+i+1)*width_combing)), "type": "line"}
        goto_next2 = {"start": (0, ((k+i+1)*width_combing)), "end": (0, ((k+i+2)*width_combing)), "type": "line"}
        i += 1
        list.append(trip)
        list.append(goto_next)
        list.append(trip2)
        list.append(goto_next2)
    
    comb_cut_order = list    
    #first_trip = {"start": (0, 0), "end": (width, 0), "type": "line"}
    #goto_next1 ={"start": (width, 0), "end": (width, (width_combing)), "type": "line"}
    #snd_trip = {"start": (width, (width_combing)), "end": (0, (width_combing)), "type": "line"}
    #goto_next2 = {"start": (0, (width_combing)), "end": (0, (2*width_combing)), "type": "line"}
    #thrd_trip = {"start": (0, (2*width_combing)), "end": (width, (2*width_combing)), "type": "line"}
    
    #comb_cut_order = [first_trip, 
     #                 goto_next1,
      #                snd_trip,
      #                goto_next2,
      #                thrd_trip
      #                ]
    return comb_cut_order
