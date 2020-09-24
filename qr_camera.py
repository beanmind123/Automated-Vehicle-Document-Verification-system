"""
Created on Sun Apr  5 08:03:44 2020

@author: Shubham Bhargav
"""
from tkinter import *
root=Tk()
root.state('zoomed')
v=Label(root,text="Place The QR Code Of Your Registration Card Straight Before Camera!! \n \n Verifying Your Registartion Card And Insuarance....",bg="GREY",fg="RED",width=80,height=400,font="Times 24 bold italic")
#u.config(fontsize='44')
v.pack()
root.after(3005,root.destroy)
#root.destroy()
root.mainloop()
