import mysql.connector
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="auto_doc_verify"
)

cursor = mydb.cursor()


file=open(r'C:\Users\hp\Desktop\cardid.txt','r')
for f in file:
    pass#print(f.lstrip(),end="")#PRINTS CONTENT AS IT IS AS STORE IN FILE SAME SPACES TAKEN
i=f.lstrip()


cursor.execute("select R_C,insurance,license_auth from central_database where rfid_number ='"+i+"'")
rows = cursor.fetchall()
results = len(rows)
if results > 0:
    row = rows[0]
    rc,insur,lic=row[0],row[1],row[2]
    if rc and insur and lic:
        from tkinter import *
        root = Tk()
        

        def com():
            q=("SELECT number ,owner_name ,model_name ,colour,rfid_number,type  from vehicle_info where rfid_number='"+i+"'")
            cursor.execute(q)
            rows = cursor.fetchall()
            results = len(rows)
            if results > 0:
                row = rows[0]
                veh_no,owner_name ,model_name ,colour  ,rfid ,tp = row[0],row[1], row[2],row[3], row[4] ,row[5]

                Label(text=tp,font=30).grid(row=1,column=2)
                Label(text=veh_no,font=30).grid(row=2,column=2)
                Label(text=colour,font=30).grid(row=3,column=2)
                Label(text=rc,font=30).grid(row=4,column=2)
                Label(text=insur,font=30).grid(row=5,column=2)
                Label(text=lic,font=30).grid(row=6,column=2)
                
            
        #width x height
        root.geometry("600x500")
        root.maxsize(600,500)
        root.minsize(600,500)

        root.title("RTO")
        #HEADING
        Label(text="VEHICLE INFO",font=("",18,"bold"),pady=30).grid(row=0,column=1)
        #LABLES CREATED
        Label(text="VEHICLE TYPE ",font=("",12,"bold"),pady=20).grid(row=1,column=0)
        Label(text="VEHICLE NUMBER",font=("",12,"bold"),pady=20).grid(row=2,column=0)
        Label(text="VEHICLE COLOR",font=("",12,"bold"),pady=20).grid(row=3,column=0)

        #ENTRY CREATED FOR INPUT
        #TYPE OF ENTRY IS STORED
        vctype = StringVar()
        vcnumber = StringVar()
        vccolor = StringVar()


        #check box
        Label(text="Registration Card",font=("",12,"bold"),pady=10).grid(row=4,column=0)
        Label(text="Insurance",font=("",12,"bold"),pady=10).grid(row=5,column=0)
        Label(text="License",font=("",12,"bold"),pady=10).grid(row=6,column=0)

        #final button which will work
        Button(text="Press here for information",command=com).grid(row=7,column=1)

        root.mainloop()


q=("SELECT number ,owner_name ,model_name ,r_c  ,insurance	,license    ,challan_amount ,colour	,rfid  from challan where rfid='"+i+"'")
cursor.execute(q)
rows = cursor.fetchall()
results = len(rows)
if results > 0:
    row = rows[0]
    veh_no,owner_name ,model_name ,rc  ,insur,lic  ,challan_amount ,colour  ,rfid  = row[0],row[1], row[2],row[3], row[4] ,row[5],row[6], row[7] ,row[8]

    if rc and insur and lic:
        print("Valid")

    else:
        cursor.execute("SELECT type,email_id from vehicle_info where rfid_number= '"+i+"'")
        t=cursor.fetchall()
        tm=t[0]
        tt=tm[0]
        ml=tm[1]
        print("\n\nPANEL\n\n")
        
        from tkinter import *
        import mysql.connector
        root = Tk()
        def com():
            Label(text=challan_amount,font=30).grid(row=1,column=3)
            Label(text=veh_no,font=30).grid(row=2,column=3)
            Label(text=model_name,font=30).grid(row=3,column=3)
            Label(text=colour,font=30).grid(row=4,column=3)
            Label(text=tt,font=30).grid(row=5,column=3)
            Label(text=rc,font=30).grid(row=6,column=3)
            Label(text=insur,font=30).grid(row=7,column=3)
            Label(text=lic,font=30).grid(row=8,column=3)
            
        #width x height
        root.geometry("1000x600")
        root.maxsize(1000,600)
        root.minsize(1000,600)

        root.title("RTO")
        #HEADING
        Label(text="VEHICLE INFO",font=("",18,"bold"),pady=30).grid(row=0,column=2)
        #LABLES CREATED
        Label(text="CHALLAN AMOUNT",font=("",12,"bold"),pady=20).grid(row=1,column=0)
        Label(text="VEHICLE NUMBER",font=("",12,"bold"),pady=20).grid(row=2,column=0)
        Label(text="VEHICLE MODEL",font=("",12,"bold"),pady=20).grid(row=3,column=0)
        Label(text="VEHICLE COLOR",font=("",12,"bold"),pady=20).grid(row=4,column=0)
        Label(text="VEHICLE TYPE",font=("",12,"bold"),pady=20).grid(row=5,column=0)

        #ENTRY CREATED FOR INPUT
        #TYPE OF ENTRY IS STORED
        vctype = StringVar()
        vcnumber = StringVar()
        vccolor = StringVar()


        #check box
        Label(text="Registration Card",font=("",12,"bold"),pady=10).grid(row=6,column=0)
        Label(text="Insurance",font=("",12,"bold"),pady=10).grid(row=7,column=0)
        Label(text="License",font=("",12,"bold"),pady=10).grid(row=8,column=0)

        #final button which will work
        Button(text="Press here for information",command=com).grid(row=9,column=2)

        root.mainloop()
        print('mailing')
        import smtplib
        sender_email="beanmind2611@gmail.com"
        rec_email=ml
        password='allcapital@2611'#input(str("enter the password : "))
        message=("Number = "+ str(veh_no) + "\n amount = "+str(challan_amount))
        server=smtplib.SMTP('smtp.gmail.com',587)
        server.ehlo()
        server.starttls()
        server.login(sender_email,password)
        #print("Login success")
        server.sendmail(sender_email,rec_email,message)
        print("Challan generated and mailed to mailid with due date", ml)
                        
