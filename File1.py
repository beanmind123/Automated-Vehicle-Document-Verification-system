"""
Created on Fri Mar 13 19:33:11 2020
updated on Sun Apr 05 11:28:30 2020 

@author: Shivani Kushwah, Shyam Kumawat
"""
import face_camera
from cv2 import *
import mysql.connector
import face_recognition
import os
import glob
import stat
import time
import sys
from datetime import date,datetime,timedelta

import numpy as np

shiva_image = face_recognition.load_image_file(r'C:\Users\hp\Desktop\fresh\dataset\s5.jpg')
shiva_face_encoding = face_recognition.face_encodings(shiva_image)[0]

#sharma_image = face_recognition.load_image_file(r'C:\Users\hp\Desktop\trainps\p3.jpg')
#sharma_face_encoding = face_recognition.face_encodings(sharma_image)[0]

#shubham_image = face_recognition.load_image_file(r'C:\Users\hp\Desktop\shubham.jpg')
#shubham_face_encoding = face_recognition.face_encodings(shubham_image)[0]

#shyam_image = face_recognition.load_image_file(r'C:\Users\hp\Desktop\shyam.jpg')
#shyam_face_encoding = face_recognition.face_encodings(shyam_image)[0]

#bhavi_image = face_recognition.load_image_file(r'C:\Users\hp\Desktop\bhavi.jpg')
#bhavi_face_encoding = face_recognition.face_encodings(bhavi_image)[0]

known_face_encodings = [
    shiva_face_encoding#,
    #sharma_face_encoding,
    #shubham_face_encoding,
    #shyam_face_encoding,
    #bhavi_face_encoding
    ]

known_face_lnumber = [
    "234shubham"#,
    #"sharma345",
    #"123shiva",
    #"456shyam",
    #"shamb567"
    ]


#print("MATCHING FACE AND GETTING LICENSE NUMBER")
#Intitializing variables
face_locations = []
face_encodings = []
face_lnumber = []
process_this_frame = True


# initialize the camera
cam = VideoCapture(0)   # 0 -> index of camera
ret, frame = cam.read()
# resize vedio to 1/4 size
small_frame = cv2.resize(frame, (0,0), fx=0.25, fy=0.25)
#bgr to rgb
rgb_small_frame = small_frame[:,:,::-1]

#only process every other frame to save time
if process_this_frame:
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
    lnumber = []
    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        num = "not match"

        #if True in matches:
        #    first_match_index = matches.index(True)

        #    name= known_face_lnumber[first_match_index]

        # OR small differ
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            num= known_face_lnumber[best_match_index]
            lnumber.append(num)
    process_this_frame = not process_this_frame
            

#display result
for (t,r,b,l), num in zip(face_locations, lnumber):
    t*=4
    r*=4
    b*=4
    l*=4

    cv2.rectangle(frame, (l,t),(r,b),(0,0,255),2)
    font= cv2.FONT_HERSHEY_DUPLEX
    cv2.putText(frame, num, (l+6,b-6),font , 1.0,(255,255,255),1)
    cv2.imshow("frame",frame)
    cv2.waitKey(1500)
    fetchedlnum=num

cam.release()
cv2.destroyAllWindows()

#the fetched liscense number is here in fetchedlnum which need to be matched from the qr decrypted liscense num.
#print(fetchedlnum)



#DETAILS STORED WHEN ENGINE STARTS

#CLEAR WHEN ENGINE STOPS

#fetch lnumbers details further

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="auto_doc_verify"
)

cursor = mydb.cursor()
qry=("SELECT license_type,expiry_date,email from license WHERE license_number = '"+fetchedlnum+"'")
cursor.execute(qry)

rows = cursor.fetchall()
results = len(rows)
if results > 0:
    row = rows[0]
    ltype,exdate,eml = row[0],row[1], row[2]
    license_ex=exdate
    #print("expiry date = ",exdate)
    #print("license type = ",ltype,"\nexpiry date = ",exdate,"\nemail = ",eml)
    #print(date.today())
    if ( license_ex<date.today() ):
        lupdate=0
    else:
        lupdate=1



#unsafe to call directly rather import the file but used this now
#exec(open('shubham.py').read())

import qr_camera    
from shubham import rc,insur,vehicle_number
#print(rc,insur,lupdate)

q= "SELECT rfid_number,owner_name,type,model_name,colour,email_id from vehicle_info where number = '" + vehicle_number +"'" 
cursor.execute(q)
rows = cursor.fetchall()
results = len(rows)
if results > 0:
    row = rows[0]
    rfid,oname,v_type,model_name,clr,eml = row[0],row[1], row[2],row[3],row[4],row[5]

#print(rfid,oname,v_type,model_name,clr,eml )



stmt = "INSERT INTO central_database (number ,R_C ,insurance,license,license_auth,rfid_number) VALUES ('"+ vehicle_number +"','"+str(rc)+"','"+str(insur)+"','"+fetchedlnum+"','"+str(lupdate)+"','"+ rfid+"')"
cursor.execute(stmt)

mydb.commit()



if (rc and insur and lupdate):
    import last_driver_C
else:
    #nikalo challan amt due date bhi
    if rc==0 :
        amt=500
        duedate= timedelta(days=10)+date.today()
    if lupdate==0:
        amt=1000
        duedate= timedelta(days=10)+date.today()
    if insur==0:
        amt=500
        duedate= timedelta(days=10)+date.today()
    else:
        amt=5000
        duedate= timedelta(days=10)+date.today()
        
            
    #Challan details bhi yahi pe insert###due_date,colour,rfid
    #print(duedate)    
    stmt = "INSERT INTO challan (number,owner_name,model_name,r_c,insurance,license,challan_amount,colour,rfid) VALUES('"+ vehicle_number +"','"+oname+"','"+model_name+"','"+    str(rc)+"','"+str(insur)+"','"+str(lupdate)+"','"+str(amt)+"','"+clr+"','"+ rfid+"')"
    cursor.execute(stmt)
    mydb.commit()
    
    cursor.close()
    from tkinter import *
    root=Tk()
    root.state('zoomed')

    if(rc==0):
        r='\u274c' #ye unicode ko store kara hai
    else:
        r='\u2713'
    if(insur==0):
        ins='\u274c'
    else:
        ins='\u2713'
    if(lupdate==0):
        li='\u274c'
    else:
        li='\u2713'

    u=Label(root,text=r+"REGISTRATION CARD\n"+ins+"INSURANCE\n"+li+"LICENCE\n\n\n\n"+"PLEASE USE VALID DOCUMENTS TO AVOID ANY LEGAL ACTIONS",fg="ORANGE",bg="LIGHT GREEN",width=80,height=400,font="Times 24 bold italic")
    u.pack()
    root.after(5000,root.destroy)
    root.mainloop()





print("SUCCESS")






















    
    
    





    
