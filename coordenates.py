# -*- coding: utf-8 -*-
"""
Created on Wed Jun 13 20:05:04 2018

@author: pi
"""

import json

def getCoordenates():
    try:
        with open('./savedCoordenate', 'r') as coordenates:
            data = json.load(coordenates)
    except:
        return None
    x = data['x']
    y = data['y']
    return x, y

def saveCoordenates(x, y):
    saved = {'x': x, 'y': y}
    with open('./savedCoordenate', 'w') as coordenates:
        json.dump(saved, coordenates)

{"imprimir_archivo": "/home/pi/Downloads/Programacion/mati.gcode"}
