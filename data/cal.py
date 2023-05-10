#read in data from 

import json
import os
import sys
import numpy as np


def read_json(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    ang_list = []
    for i in range(3, 7):
        ang = calc_angle(i, data)
        ang_list.append(ang)

    ang_mean = np.mean(ang_list)
    print(ang_mean)
    return ang_mean

def calc_angle(offset, data):
    x0 = data["x_gps"][offset]
    y0 = data["y_gps"][offset]
    x1 = data["x_gps"][-offset]
    y1 = data["y_gps"][-offset]
    ang1 = np.arctan2(y1-y0, x1-x0)
    return ang1

if __name__ == "__main__":
    filename = "20230510130826.json"
    ang_mean1 = read_json(filename)
    filename = "20230510130412.json"
    ang_mean2 = read_json(filename)
    filename = "20230510130013.json"
    ang_mean3 = read_json(filename)
    ang_mean = np.mean([ang_mean1, ang_mean2, ang_mean3])
    print(ang_mean)



