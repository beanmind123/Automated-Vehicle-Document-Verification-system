"""
Created on Sun Apr 05 11:45:30 2020

@author: Shubham Bhargav
"""

from tkinter import *
root=Tk()
rc=1#ye values jo function return karenge 0 ya 1 wali wo hai
root.state('zoomed')
insurance=1 #ye values jo function return karenge 0 ya 1 wali wo hai
licence=1 #ye values jo function return karenge 0 ya 1 wali wo hai
if(rc==0):
    r='\u274c' #ye unicode ko store kara hai
else:
    r='\u2713'
if(insurance==0):
    ins='\u274c'
else:
    ins='\u2713'
if(licence==0):
    li='\u274c'
else:
    li='\u2713'

if(rc&insurance&licence==1):
    u=Label(root,text=r+"REGISTRATION CARD\n"+ins+"INSURANCE\n"+li+"LICENCE\n\n\n\n"+"YOUR DRIVE IS LEGAL\n",fg="ORANGE",bg="LIGHT GREEN",width=80,height=400,font="Times 24 bold italic")
else:
    u=Label(root,text=r+"REGISTRATION CARD\n"+ins+"INSURANCE\n"+li+"LICENCE\n\n\n\n"+"PLEASE USE VALID DOCUMENTS TO AVOID ANY LEGAL ACTIONS",fg="ORANGE",bg="LIGHT GREEN",width=80,height=400,font="Times 24 bold italic")
#print("HERE")
u.pack()
root.after(15000,root.destroy)
root.mainloop()
#u='\u2713'
#print(u)
#print('\u2713')
#print('\u274c'
