#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 21:15:47 2018

@author: jack
"""
import sys
from glob import glob
#import logging
from threading import Event
import serial
import queue
import time
import json
import numpy as np
#from coordenates import getCoordenates, saveCoordenates
from datetime import datetime
import os

n = 10

class rpi(object):
    def __init__(self, debug=True):
        self._debug = debug    
        
        self.commands = {'Temperatura': 'M105', 
                    'home': {'all': 'G28', 'x': 'G28 X', 'y': 'G28 Y', 'z': 'G28 Z'},
                    'calentar_boq': 'M104 S{}', 
                    'enfriar': ['M104 S0', 'M140 S0'], 
                    'calentar_cama': 'M140 S{}', 
                    'apagar_motores': 'M84', 
                    'relative_move': 'G91',
                    'relative_absolute': 'G90',
                    'mover_x': 'G1 X{}', 
                    'mover_y': 'G1 Y{}', 
                    'mover_z': 'G1 Z{}', 
                    'mover_e': 'G1 E{}', 
                    'stop': ['G91', 'G1 Z10', 'G28 X', 'G28 Y'], 
                    'pause': ['G91', 'G1 Z10', 'G28 X', 'G28 Y'], 
                    'resume': ['G91', 'G1 Z-10', 'G1 X{x}', 'G1 Y{y}'],
                    }
        """ Variables que domina el usuario:
            self.parameters['status']
            self.parameters['Imprimiendo']['archivo']
            
            
        
        """
        self.parameters = { 'status': 'stop',  # priting, pause, stop
                            'Percent': 0,
                            'Temperatura': {'extrusor': 0, 
                                    'extrusor_meta': 0, 
                                    'cama': 0, 
                                    'cama_meta': 0}, 
                            'Imprimiendo': {'archivo': '',      # filename
                                    'tiempo': '00:00',  # [hora:min] de impresion
                                    'porcentaje': 0,    # float 23.4%
                                    'posicionZ': 0,     # int
                                    'totalZ': 0}}       # int

        
        pathArduino = glob('/dev/ttyUSB*')
        self.Arduino = serial.Serial(pathArduino[0], 115200, timeout=1)
        self.Arduino.close()
        self.Arduino.open()

        self.aw = ''
        self.s = ''

        print('Estado del puerto: {isOpen}\nNombre del dispositivo: {name}\n'.format(isOpen=self.Arduino.isOpen(), name=self.Arduino.name))

        
        """ Queue """
        self.queueCommands = []
        self.arduinoRead  = queue.Queue()
        self.arduinoWrite = queue.Queue()
        self.functionExec = queue.Queue()
        # retardo para establecer la conexion serial
#        time.sleep(2)
        self.busy = Event()
        self.priting = []
        
#        """ Threading """
#        self.thread = []
#        self.thread.append(Thread(target=self._ArduinoRead))
#        self.thread.append(Thread(target=self._ArduinoWrite))
#        self.thread.append(Thread(target=self._requestTemperature))
#        self.thread.append(Thread(target=self._functionExec))
#        
#        for thread in self.thread:
#            thread.start()
        
    def _ArduinoRead(self):
        """read the incoming messages from the arduino"""
        if self.Arduino.in_waiting > 0:
            data = self.Arduino.readline()
            data = str(data)
            if len(data) != 0:
                if len(data.split('/')) == 3: # si es temperatura?
                    # tiene 2 slash que corresponde a una
                    # respuesta de temperatura
                    t = [None] * 4
                    d = data.split('/')
                    t[0] = float(d[0].split(':')[-1])
                    t[1] = float(d[1].split('B')[0])
                    t[2] = float(d[1].split(':')[-1])
                    t[3] = float(d[2].split('@')[0])
#                    print(t)
                    
                    self.parameters['Temperatura']['extrusor'] = t[0]
                    self.parameters['Temperatura']['extrusor_meta'] = t[1]
                    self.parameters['Temperatura']['cama'] = t[2]
                    self.parameters['Temperatura']['cama_meta'] = t[3]
                    
                    
#                        self.fileWrite.put_nowait(string)
                elif data[:2] == 'ok':
                    self.busy.set()
                    if len(self.queueCommands) > 0:
                        self.queueCommands.pop(0)
                
                if self._debug:
#                    print('Lectura del arduino: {}'.format(data))
                    a = datetime.now()
                    self.s += '{:02d}-{:02d}-{:02d}-{:06d}: {}\n'.format(a.hour, a.minute, a.second, a.microsecond, data)
#                    print(data)
                    with open('../ArduinoRead.log', 'w') as f:
                        f.write(self.s)
            
    def _ArduinoWrite(self):
        """Write the commands to the arduino"""
        if not self.arduinoWrite.empty():
            string = self.arduinoWrite.get()
            # Escribe el '/n' por si no lo tiene
            if not string[-1] == '\n':
                string += '\n'

            if self._debug:
                print('Escritura arduino: {}'.format(string[:-1]))
                a = datetime.now()
                self.aw += '{:02d}-{:02d}-{:02d}-{:06d}: '.format(a.hour, a.minute, a.second, a.microsecond) + string
                with open('../ArduinoWrite.log', 'w') as f:
                    f.write(self.aw)
                    
            # espera a que se ha liberado el arduino
            self.Arduino.write(str.encode(string))
#                if not string[:-1] == 'M105':
#                    self.queueCommands.append(string)
                        
#        except:
#            raise Exception('Muerto el proceso Arduino Write')


    def _requestTemperature(self):
        """Request the temperature every one second"""
        if self.parameters['Imprimiendo']['archivo'] == '' or self.parameters['status'] == 'pause':
            self.arduinoWrite.put(self.commands['Temperatura'])
#            print('pedi T')
        
    def get_temp(self):
        t = []
        t.append(self.parameters['Temperatura']['extrusor'])
        t.append(self.parameters['Temperatura']['extrusor_meta'])
        t.append(self.parameters['Temperatura']['cama'])
        t.append(self.parameters['Temperatura']['cama_meta'])
        
        return t
    
    def control_wo_print(self, command, subcommand=None, undercommand=None):
        print('command: {}\nsubcommand: {}\nundercommand: {}'.format(command,subcommand,undercommand))
        if command == 'home':
            self.arduinoWrite.put('relative_move')
            self.arduinoWrite.put(self.commands[command.lower()][subcommand.lower()])
#            self.arduinoWrite.put('relative_absolute')
        elif command == 'apagar_motores':
            self.arduinoWrite.put('relative_move')
            self.arduinoWrite.put(self.commands[command.lower()])
#            self.arduinoWrite.put('relative_absolute')
        elif command[:4] == 'move':
            self.arduinoWrite.put('relative_move')
            self.arduinoWrite.put(self.commands[command.lower()].format(subcommand))
#            self.arduinoWrite.put('relative_absolute')
        elif command[:4] == 'cale':
            self.arduinoWrite.put('relative_move')
            self.arduinoWrite.put(self.commands[command.lower()].format(subcommand))
#            self.arduinoWrite.put('relative_absolute')
        else:
            self.arduinoWrite.put('relative_move')
            [self.arduinoWrite.put(c) for c in self.commands[command]]
#            self.arduinoWrite.put('relative_absolute')
        #self.commands[]

    def getPercent(self, linesGCode):
        distance, x, y, z, newX, newY, newZ = 0, 0, 0, 0, 0, 0, 0
        [X, Y, Z] = [[0], [0], [0]]
        for i, line in enumerate(linesGCode):
            line = line[:-1]
            if 'Layer height' in line:
                num = float(line.split(':')[-1])
                z, Z[0], newZ = [num, num, num]
        flag = False
        initflag = True
        for i, line in enumerate(linesGCode):
            line = line[:-1]
            if line[0] == ';':
#                if line == ';TYPE:SKIRT\r' and flag:
#                    flag = False
                continue
            if flag:
                continue
            if len(line.split(';')) > 1:
                line = line.split(';')[0]
            if line[-1] == '\r':
                line = line[:-1]
            while line[-1] == ' ':
                line = line[:-1]
            # si es un comando no se suma
            if line[0] == 'M':
                continue
            line = line.split(' ')
            f = True
            for l in line:
                if l[0] == 'X':
                    newX = float(l[1:])
                    f = False
                elif l[0] == 'Y':
                    newY = float(l[1:])
                    f = False
                elif l[0] == 'Z':
                    newZ = float(l[1:])
                    f = False
            if f:
                continue
            if initflag:
                initflag = False
                x, y, z = newX, newY, newZ
                X[0], Y[0], Z[0] = newX, newY, newZ
                continue
            distance += np.sqrt(np.power(x - newX, 2) + np.power(y - newY, 2) + np.power(z - newZ, 2))
            x, y, z = newX, newY, newZ
            X.append(x)
            Y.append(y)
            Z.append(z)
        self.distanceTotal = distance
        self.totalZ = Z[-1]
        self.parameters['Imprimiendo']['totalZ'] = self.totalZ
        # sin esto tira un error
        from mpl_toolkits.mplot3d import Axes3D
        import matplotlib.pyplot as plt
        
        fig = plt.figure(figsize=[15,15])
        ax = fig.gca(projection='3d')
        ax.plot(X, Y, Z)
#        plt.axis('off')
        plt.grid()
        ax.set_zlim(0, 190)
        ax.set_ylim(0, 190)
        ax.set_xlim(0, 190)
        plt.savefig("./figura_actual.png")
        plt.close('all')
        print ('Done percent!!')
    
    def Priting(self, dt):
        self.distanceTotal = 0
        path = self.parameters['Imprimiendo']['archivo']
        with open(path, 'r') as gcode:
            linesGCode = gcode.readlines()
            
        self.parameters['Imprimiendo']['archivo'] = os.path.basename(self.parameters['Imprimiendo']['archivo']).split('.')[0]
#        Thread(target=self.getPercent, args=(linesGCode)).start()
        self.getPercent(linesGCode)
        # esto me entregara self.distanceTotal
        lineDistance, x, y, z, newX, newY, newZ = 0, 0, 0, 0, 0, 0, 0
        start = time.time()
        for i, line in enumerate(linesGCode):
            line = line[:-1]
            if line[0] == ';':
                continue
            if len(line.split(';')) > 1:
                line = line.split(';')[0]
            while line[-1] == ' ':
                line = line[:-1]
            if line[-1] == '\r':
                line = line[:-1]
            lineprocess = line.split(' ')
            f = False
            for l in lineprocess:
                if l[0] == 'X':
                    newX = float(l[1:])
                    f = True
                elif l[0] == 'Y':
                    newY = float(l[1:])
                    f = True
                elif l[0] == 'Z':
                    newZ = float(l[1:])
                    f = True
            if f:
                lineDistance += np.sqrt(np.power(x - newX, 2) + np.power(y - newY, 2) + np.power(z - newZ, 2))
            
                x, y, z = newX, newY, newZ
                self.x, self.y, self.z = newX, newY, newZ
                self.parameters['Imprimiendo']['posicionZ'] = self.z
            percent = 100 * lineDistance / (self.distanceTotal + 1e-5)
            self.parameters['Imprimiendo']['porcentaje'] = percent
            seconds = time.time() - start
            hours = np.int32(seconds // 3600)
            minutes = np.int32((seconds % 3600) // 60)
            self.parameters['Imprimiendo']['tiempo'] = '{:02d}:{:02d}'.format(hours, minutes)
            self.priting.append((n, line, lineDistance, percent))
            if self.parameters['status'] == 'pause':
                while True:
                    if self.parameters['status'] != 'pause':
                        time.sleep(.05)
                        break
            elif self.parameters['status'] == 'stop':
                self.parameters['Imprimiendo']['archivo'] = ''
                
                break
            self.arduinoWrite.put_nowait(line)
            self.queueCommands.append(line)
            if (i % 5) == 0:
                self.arduinoWrite.put_nowait(self.commands['Temperatura'])
            if len(self.queueCommands) >= 1:
                self.busy.wait()
            self.busy.clear()
#            print 'busy.clear, queue command: {}'.format(len(self.queueCommands))
        print ('Done put variables')
        self.parameters['Imprimiendo']['archivo'] = ''
            #no hace nada hasta que el ultimo comando es hecho
#            while self.parameters['Imprimiendo']['status'] == 'pause':
#                pass
#            
#            if self._debug:
#                print('Se va a enviar la siguiente linea de comando al arduino: {}'.format(line))
#            while True:
#                try:
#                    self.arduinoWrite.put((n, line))
#                    self.busy.wait()
#                    break
#                except:
#                    print 'arduinoWrite is Full'
            
            
#            if self.distanceTotal != 0:
#                percent = 100 * lineDistance / self.distanceTotal
#                self.parameters['Imprimiendo']['porcentaje'] = percent
#                print('{:%}'.format(self.parameters['Imprimiendo']['porcentaje'] / 100))

if __name__ == '__main__':
    self = rpi()
    while True:
        time.sleep(1)
#    self.arduinoWrite.put_nowait((n // 2, 'G28\n'))
#    time.sleep(30)
#    a = []
#    while not self.arduinoWrite.empty():
#        a.append(self.arduinoWrite.get_nowait()[-1])
    
