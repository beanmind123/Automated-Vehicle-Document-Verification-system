"""
Created on Sun Apr  5 01:03:44 2020

@author: Shubham Bhargav
"""
from tkinter import *
root=Tk()
root.state('zoomed')
label=Label(root,text="Please Look Into The Camera For A While!! \n \n Your Licence Is Being Verified....",bg="ORANGE",fg="LIGHT GREEN",width=80,height=400,font="Times 24 bold italic")
label.pack()
root.after(3000,root.destroy)
root.mainloop()
