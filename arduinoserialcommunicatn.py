"""
Created on Sun Apr  2 01:38:43 2020

@author: Shivani Kushwah 
"""
#police scanner

import serial
import signal
import time
from datetime import date,datetime



arduino = serial.Serial('COM3', 9600) #, timeout=.1) # wait for Arduino
while True:
    data = arduino.readline().decode('ascii')[:-2] #the last bit gets rid of the new-line chars
    if(data):
        #print(data)
        file=open(r'C:\Users\hp\Desktop\cardid.txt','w')
        file.write('\n'+data)#WRITES CONTENTS AS IT IS IN TXT FILE
        file.close()
        break

print("SCANNED")
        


import police
