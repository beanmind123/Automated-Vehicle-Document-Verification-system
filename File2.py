# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 18:36:11 2020

@author: Shubham Bhargav
"""
#registration_card_db_connect.py


from __future__ import print_function
import pyzbar.pyzbar as pyzbar
import numpy as np
import cv2
import time
import base64
import hashlib
from Crypto.Cipher import AES
from Crypto import Random
import datetime
from datetime import date,datetime
import mysql.connector

#print("\n\nScan your RC QR")
conn=mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="auto_doc_verify")
mycursor=conn.cursor()
 
BLOCK_SIZE = 16
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
unpad = lambda s: s[:-ord(s[len(s) - 1:])]
 
#password = input("Enter encryption password: ")
password="Mydreamlife@8989"
vehicle_number="MP09CP7317" 

#rto
def encrypt(raw, password):
    private_key = hashlib.sha256(password.encode("utf-8")).digest()
    raw = pad(raw)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(private_key, AES.MODE_CBC, iv)
    return base64.b64encode(iv + cipher.encrypt(raw))
 
 
def decrypt(enc, password):
    private_key = hashlib.sha256(password.encode("utf-8")).digest()
    enc = base64.b64decode(enc)
    iv = enc[:16]
    cipher = AES.new(private_key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(enc[16:]))
 
# get the webcam:  
cap = cv2.VideoCapture(0)

cap.set(3,640)
cap.set(4,480)
#160.0 x 120.0
#176.0 x 144.0
#320.0 x 240.0
#352.0 x 288.0
#640.0 x 480.0
#1024.0 x 768.0
#1280.0 x 1024.0
time.sleep(2)

def decode(im) :
    # Find barcodes and QR codes
    decodedObjects = pyzbar.decode(im)
    # Print results
    for obj in decodedObjects:
        print()
        #print('Type : ', obj.type)
        #print('Data : ', obj.data,'\n')     
    return decodedObjects


font = cv2.FONT_HERSHEY_SIMPLEX

#while(cap.isOpened()):
    # Capture frame-by-frame
def read_qr():
    for i in range(1):
        ret, frame = cap.read()
    # Our operations on the frame come here
        im = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
         
        decodedObjects = decode(im)
        u=""

        for decodedObject in decodedObjects: 
            points = decodedObject.polygon
     
        # If the points do not form a quad, find convex hull
            if len(points) > 4 : 
                hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
                hull = list(map(tuple, np.squeeze(hull)))
            else : 
                hull = points;
         
        # Number of points in the convex hull
            n = len(hull)     
        # Draw the convext hull
            for j in range(0,n):
                cv2.line(frame, hull[j], hull[ (j+1) % n], (255,0,0), 3)

            x = decodedObject.rect.left
            y = decodedObject.rect.top

            #print(x, y)

            #print('Type : ', decodedObject.type)
            #print('Data : ', decodedObject.data,'\n')

            u=decodedObject.data
            barCode = str(decodedObject.data)
            cv2.putText(frame, barCode, (x, y), font, 1, (0,255,255), 2, cv2.LINE_AA)
               
    # Display the resulting frame
        cv2.imshow('frame',frame)
        key = cv2.waitKey(100)
        if key & 0xFF == ord('q'):
            break
        elif key & 0xFF == ord('s'): # wait for 's' key to save 
            cv2.imwrite('Capture.png', frame)
        

# When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
    return decodedObject.data
    #print(u,"lappas")
    #return u

def registration_card():
    a=read_qr()
    
    #u=a.decode('ASCII')
    #print(u)
    u=decrypt(a,password)
    u=u.decode('ASCII')
    #print(u)# vehicle num
    if(u==vehicle_number):
        rc=1
    else:
        rc=0
    mycursor.execute("Select expiry_date from insurance where number='MP09CP7317'")
    u=mycursor.fetchall()
    for i in u:
        fdate=i[0]
        #print(fdate)
        
    if(fdate<date.today()):
        insurance=0
    else:
        insurance=1
    #print(rc,insurance)
    return rc,insurance # store in central database
#print(val)
rc,insur=registration_card()

