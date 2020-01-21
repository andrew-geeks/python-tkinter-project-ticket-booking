import random
import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
from tkinter import simpledialog
import mysql.connector
import PIL
from PIL import ImageTk,Image


app = tk.Tk() 
app.title('TripLife')
app.geometry('500x300')
app.configure(background='orange')
#tkinterGUI
#GUI--from
label=Label(app,text='From',background='pink')
label.grid(column=2,row=1)
boxvalue=StringVar()
combobox = ttk.Combobox(app,textvariable=boxvalue,values=["-Select-","Muscat", "Mumbai", "Delhi",'Bangalore'])
combobox.grid(column=2,row=2)
combobox.current(0)
#GUI--TO
label1=Label(app,text='To',background='pink')
label1.grid(column=6,row=1)
boxvalue1=StringVar()
combobox1=ttk.Combobox(app,textvariable=boxvalue1,values=["-Select-","Muscat", "Mumbai", "Delhi",'Bangalore'])
combobox1.current(0)
combobox1.grid(column=6,row=2)

#GUI--Adults--Children
adult=IntVar()
children=IntVar()
rawa=0
rawc=0
labelhead=Label(app,text='Passengers',background='pink')
labelhead.grid(column=4,row=3)
label2=Label(app,text='Adults',background='pink')
label2.grid(column=2,row=4)
adult=tk.Spinbox(app, from_=0, to=5,increment=1)
adult.grid(column=2,row=5)
label3=Label(app,text='Children',background='pink')
label3.grid(column=6,row=4)
children=tk.Spinbox(app,from_=0,to=5,increment=1)
children.grid(column=6,row=5)

#GUI -- trip
var=IntVar()
var1=IntVar()
selection=''
selection1=''
def sel1():
   global selection
   selection=str(var.get())
   print(selection)
   
Label(app, text = "Method of Travel",background='pink').grid(row=6, column=4)
Radiobutton(app, text = "OneWay", variable = var, value=1,command=sel1).grid(row=7,column=4)
Radiobutton(app, text = "RoundTrip", variable = var, value=2,command=sel1).grid(row=8,column=4)
#class
def cls():
    global selection1
    selection1=str(var1.get())
    
Label(app,text="Class",background='pink').grid(row=9,column=2)
Radiobutton(app, text='Economy', variable = var1, value=1,command=cls).grid(row=10,column=2)
Radiobutton(app, text='business', variable = var1, value=2,command=cls).grid(row=10,column=4)

def end():#function to end app-GUI
    global rawa
    global rawc
    f1=boxvalue.get()  #from value
    f2=boxvalue1.get() #to value
    a=adult.get()
    rawa=a
    b=children.get()
    rawc=b
    if f1=='-Select-' and f2=='-Select-':
        return messagebox.showerror('Error','Please select Departure & Arrival locations')
    elif f2=='-Select-':
        return messagebox.showerror("Error", "Select Arrival location")
    elif f1==f2:
        return messagebox.showerror("Error", "Invalid location entry!")
    elif f1=='-Select-':
        return messagebox.showerror('Error','Please select Departure location')
    elif rawa=='0' and rawc=='0':
        return messagebox.showerror("Error", "choose no. of passengers")
    elif selection=='':
        return messagebox.showerror("Error", "choose method of travel")
    elif selection1=='':
        return messagebox.showerror("Error", "choose class of travel") 
    else:
        app.destroy()
img=Image.open('card.jpg')
img1=Image.open('iata.png')
img1=img1.resize((110,50),Image.ANTIALIAS)
img=img.resize((110,50),Image.ANTIALIAS)
render=ImageTk.PhotoImage(img)
render1=ImageTk.PhotoImage(img1)
Label(app,image=render1).place(x=100,y=210)
Label(app,image=render).place(x=220,y=210)
tk.Button(app,text='Continue',command=end,bg='yellow').grid(column=6,row=9)
app.mainloop()
#values
f1=boxvalue.get()  #from value
f2=boxvalue1.get() #to value
sel1()    #method of travel value
print(rawa,rawc)  #adult and children value raw-adult  raw-children
#conversions(str to int)
adultnumber=int(rawa)
childnumber=int(rawc)
deptime1=''
arrtime1=''
pricead1=0
pricech1=0
tprice=0
flname=''
flag=0
totaltime=''
def database():
    global adultnumber
    global childnumber
    global adultlist
    global childlist
    global adpslist
    global chpslist
    global bnumber
    global selection
    global f1
    global f2
    global cnum
    global cvvnum
    global expmonth
    global expyear
    type1=''
    if selection=='1':
        type1='oneway'
    else:
        type1='roundtrip'
    db = mysql.connector.connect(host='localhost',user='root',passwd='isamrn37',database='triplife')
    mycursor=db.cursor()
    mycursor.execute("use triplife")
    db.commit()
    if adultnumber!=0:
        for i in range(adultnumber):
            mycursor=db.cursor()
            mycursor.execute("insert into details values (%s,%s,%s,%s, %s, %s)",(bnumber,adultlist[i],adpslist[i],type1,f1,f2))
            db.commit()
    if childnumber!=0:
        for i in range(childnumber):
            mycursor=db.cursor()
            mycursor.execute("insert into details values (%s,%s,%s,%s, %s, %s)",(bnumber,childlist[i],chpslist[i],type1,f1,f2))
            db.commit()
    db.close()
    db = mysql.connector.connect(host='localhost',user='root',passwd='isamrn37',database='triplife')
    mycursor=db.cursor()
    mycursor.execute("use triplife")
    mycursor.execute("insert into payment values (%s,%s,%s,%s)",(cnum,cvvnum,expmonth,expyear))                                                                                                                                        
    db.commit()                          
def omanair1():     
    global flag
    global flname
    global pricead1
    global pricech1
    global deptime1
    global arrtime1
    global selection1
    global tprice
    global f1
    global f2
    global totaltime
    flname='OmanAir'
    basefare=10
    if f1=='Muscat' and f2=='Mumbai':
        deptime1='01:10am'
        arrtime1='03:30am'
        totaltime='2 Hours 20 Minutes'
        pricead1=80*adultnumber
        pricech1=60*childnumber
        if selection1=='2':  #businesscls calc.
               tprice=pricead1*2+pricech1*3
        else:
            tprice=pricead1+pricech1#do like this for all
    elif f1=='Mumbai' and f2=='Muscat':
        deptime1='05:30am '
        arrtime1='08:00am'
        pricead1=80*adultnumber   #price for adult 
        pricech1=60*childnumber   #price for childe
        totaltime='2 Hours 30 Minutes'
        if selection1=='2':  #businesscls calc.
               tprice=pricead1*2+pricech1*3
        else:
            tprice=pricead1+pricech1
    elif f1=='Muscat' and f2=='Delhi':  
        deptime1='08:30am'
        arrtime1='12:00pm'
        totaltime='3 Hours 30 Minutes'
        pricead1=90*adultnumber
        pricech1=50*childnumber
        if selection1=='2':  #businesscls calc.
               tprice=pricead1*2+pricech1*3
        else:
            tprice=pricead1+pricech1
    elif f1=='Delhi' and f2=='Muscat':
        deptime1='1:00am'   
        arrtime1='4:30am'
        totaltime='3 Hours 30 Minutes'
        pricead1=93*adultnumber
        pricech1=50*childnumber
        if selection1=='2':  #businesscls calc.
               tprice=pricead1*2+pricech1*3
        else:
            tprice=pricead1+pricech1
    elif f1=='Muscat' and f2=='Bangalore': 
        deptime1='1:30am'
        arrtime1='4:45am'
        totaltime='3 Hours and 15 Minutes'
        pricead1=110*adultnumber
        pricech1=97*childnumber
        if selection1=='2':  #businesscls calc.
               tprice=pricead1*2+pricech1*3
        else:
            tprice=pricead1+pricech1
    elif f1=='Bangalore' and f2=='Muscat':  
        deptime1='6.00am'
        arrtime1='9:15am'
        totaltime='3 Hours and 15 Minutes'
        pricead1=110*adultnumber
        pricech1=97*childnumber    
        if selection1=='2':  #businesscls calc.
               tprice=pricead1*2+pricech1*3
        else:
            tprice=pricead1+pricech1
    elif tprice==0:
        flag=1
pricead2=0
pricech2=0
deptime2=''  
arrtime2=''
tprice1=0
af1=''
af2=''
def airindia1():
    global flag
    global af1
    global af2
    global pricead
    global pricech
    global deptime2
    global arrtime2
    global selection1
    global tprice1
    global flname1
    global f1
    global f2
    global totaltime
    flname1='AirIndia'
    basefare=10
    if f1=='Delhi' and f2=='Mumbai':
        deptime2='4:00pm'
        arrtime2='5:30pm'
        totaltime='1 Hour and 30 Minutes'
        pricead2=25*adultnumber
        pricech2=18*childnumber
        af1=f1
        af2=f2
        if selection1=='2':#bussiness-airindia
            tprice1=pricead2*3+pricech2*2
        else:
            tprice1=pricead2+pricech2
    elif f1=='Mumbai' and f2=='Delhi':
        deptime2='6:30om'
        arrtime2='8:00pm'
        totaltime='1 Hour 30 Minutes'
        pricead2=25*adultnumber
        pricech2=18*childnumber
        af1=f1
        af2=f2
        if selection1=='2':  #bussiness-airindia
            tprice1=pricead2*3+pricech2*2
        else:
            tprice1=pricead2+pricech2
        
    elif f1=='Mumbai' and f2=='Bangalore':
        deptime2='2:00pm'
        arrtime2='3:00pm'
        totaltime='1 Hour'
        pricead2=20*adultnumber
        pricech2=14*childnumber
        af1=f1
        af2=f2
        if selection1=='2':#bussiness-airindia
            tprice1=pricead2*3+pricech2*2
        else:
            tprice1=pricead2+pricech2
    elif f1=='Bangalore' and f2=='Mumbai':
        deptime2='3:45pm'
        arrtime2='4:50pm'
        totaltime='1 Hour 5 Minutes'
        pricead2=20*adultnumber
        pricech2=14*childnumber
        af1=f1
        af2=f2
        if selection1=='2':#bussiness-airindia
            tprice1=pricead2*3+pricech2*2
        else:
            tprice1=pricead2+pricech2#
    elif f1=='Muscat' and f2=='Mumbai':
        deptime2='01:30am'
        arrtime2='03:30am'
        totaltime='2 Hours 20 Minutes'
        pricead2=75*adultnumber
        pricech2=60*childnumber
        af1=f1
        af2=f2
        if selection1=='2':  #businesscls calc.
               tprice1=pricead2*3+pricech2*2
        else:
            tprice1=pricead2+pricech2
    if f1=='Mumbai' and f2=='Muscat':
        deptime2='05:00am'
        arrtime2='07:20am'
        totaltime='2 Hours 20 Minutes'#follow me
        pricead2=80*adultnumber
        pricech2=60*childnumber
        af1=f1
        af2=f2
        if selection1=='2':  #businesscls calc.
               tprice1=pricead2*3+pricech2*2
        else:
            tprice1=pricead2+pricech2
    elif f1=='Delhi' and f2=='Muscat':
        deptime2='12:30pm'   
        arrtime2='3:30pm'
        totaltime='3 Hours 30 Minutes'
        pricead2=90*adultnumber
        pricech2=50*childnumber
        af1=f1
        af2=f2
        if selection1=='2':  #businesscls calc.
               tprice1=pricead2*3+pricech2*2
        else:
            tprice1=pricead2+pricech2
    elif f1=='Muscat' and f2=='Delhi':
        deptime2='5:00pm'   
        arrtime2='8:30pm'
        totaltime='3 Hours 30 Minutes'
        pricead2=90*adultnumber
        pricech2=50*childnumber
        af1=f1
        af2=f2
        if selection1=='2':  #businesscls calc.
               tprice1=pricead2*3+pricech2*2
        else:
            tprice1=pricead2+pricech2
    elif f1=='Muscat' and f2=='Bangalore': 
        deptime2='3:00pm'
        arrtime2='6:15pm'
        totaltime='3 Hours and 15 Minutes'
        pricead2=105*adultnumber
        pricech2=92*childnumber
        af1=f1
        af2=f2
        if selection1=='2':  #businesscls calc.
               tprice1=pricead2*3+pricech2*2
        else:
            tprice1=pricead2+pricech2
    elif f1=='Bangalore' and f2=='Muscat': 
        deptime2='7:30pm'
        arrtime2='10:45pm'
        totaltime='3 Hours and 15 Minutes'
        pricead2=105*adultnumber
        pricech2=92*childnumber
        af1=f1
        af2=f2
        if selection1=='2':  #businesscls calc.
               tprice1=pricead2*3+pricech2*2
        else:
            tprice1=pricead2+pricech2
    elif f1=='Delhi' and f2=='Bangalore':
        deptime2='1:00pm'
        arrtime2='2:45pm'
        totaltime='1 Hour and 45 Minutes'
        pricead2=85*adultnumber
        pricech2=78*childnumber
        af1=f1
        af2=f2
        if selection1=='2':  #businesscls calc.
               tprice1=pricead2*3+pricech2*2
        else:
            tprice1=pricead2+pricech2
    elif f1=='Bangalore' and f2=='Delhi':
        deptime2='3:30pm'
        arrtime2='5:15pm'
        totaltime='1 Hour and 45 Minutes'
        pricead2=85*adultnumber
        pricech2=77*childnumber
        af1=f1
        af2=f2
        if selection1=='2':  #businesscls calc.
               tprice1=pricead2*3+pricech2*2
        else:
            tprice1=pricead2+pricech2
omanair1()
airindia1()
   
def confirmation():
    global bnumber
    confirmation=tk.Tk()
    confirmation.title('Booking Confirmation')
    confirmation.geometry('500x500')
    bnumber=random.randint(10000,40000)
    
    def quit():
        confirmation.destroy()
        database()
    Label(confirmation,text='Confirmation',font='Helvetica 12 bold').grid(row=1,column=2)
    Label(confirmation,text='Booking Is Confirmed').grid(row=2,column=2)
    Label(confirmation,text='Your Booking Reference Number:'+str(bnumber),font='Helvetica 12 bold').grid(row=3,column=2)
    Label(confirmation,text='Contact Us:').grid(row=4,column=1)
    Label(confirmation,text='Phone Number:91310065').grid(row=5,column=2)
    Label(confirmation,text='Email:admin@triplife.com').grid(row=6,column=2)
    Button(confirmation,text='Quit',command=quit).grid(row=7,column=3)
    bnumber=int(bnumber)
cnum=''
cvvnum=''
expmonth=''
expyear=''
def payments():#payment window
    payments=tk.Tk()
    payments.geometry('700x350')
    payments.title('Payment')
    img1=Image.open('card.jpg')
    img1=img1.resize((110,50),Image.ANTIALIAS)
    render1=ImageTk.PhotoImage(img1)
    Label(payments,image=render1).place(x=100,y=220)
    v=tk.IntVar()
    cnumber=StringVar()
    cvv=StringVar()
    month=StringVar()
    year=StringVar()
    def check():
        global cnum
        global cvvnum
        global expmonth
        global expyear
        ctype=v.get()
        cnum=cnumber.get()
        cvvnum=cvv.get()
        expmonth=month.get()
        expyear=year.get()
        
        if ctype==0:
            return messagebox.showerror('Error','Select Card Type')
        elif cnum=='':
            return messagebox.showerror('Error','Enter Card Number')
        elif cvvnum=='':
            return messagebox.showerror('Error','Enter CVV number')
        elif expmonth=='':
            return messagebox.showerror('Error','Enter Month of Expiry')
        elif expyear=='':
            return messagebox.showerror('Error','Enter Year of Expiry')
        elif len(cvvnum)<3:
            return messagebox.showerror('Error','Enter valid CVV number')
        elif len(cvvnum)>3:
            return messagebox.showerror('Error','Enter valid CVV number')
        else:
            payments.destroy()
            confirmation()
    Label(payments,text='Payments',font='Helvetica 12 bold').grid(row=1,column=2)
    Label(payments,text='>>Total amount to pay: OMR'+totalprice).grid(row=2,column=1)
    Label(payments,text='>>Select Card Type').grid(row=3,column=1)
    Radiobutton(payments,text='Credit Card',variable=v,value=1).grid(row=4,column=1) 
    Radiobutton(payments,text='Debit Card',variable=v,value=2).grid(row=4,column=2)
    Label(payments,text='Enter Card Number').grid(row=5,column=1)
    Entry(payments,width=30,textvariable=cnumber).grid(row=5,column=2)
    Label(payments,text='CVV').grid(row=6,column=1)
    Entry(payments,width=3,textvariable=cvv).grid(row=7,column=1)
    Label(payments,text='Enter Card expiry date').grid(row=8,column=2)
    Label(payments,text='Month').grid(row=9,column=2)
    Entry(payments,width=4,textvariable=month).grid(row=10,column=2)
    Label(payments,text='(Enter in MM format)').grid(row=11,column=2)
    Label(payments,text='Year').grid(row=9,column=3)
    Entry(payments,width=6,textvariable=year).grid(row=10,column=3)
    Label(payments,text='(Enter in YYYY format)').grid(row=11,column=3)
    Button(payments,text='Confirm booking',command=check).grid(row=12,column=3)
    
    payments.mainloop()



def details(): #details GUI-GLOBAL 
        def command1():
            global adultlist
            global childlist
            global adpslist
            global chpslist
            a=adstr.get()
            b=chstr.get()
            c=psadstr.get()
            d=pschstr.get()
            adultlist=list(a.split(','))
            childlist=list(b.split(','))
            adpslist=list(c.split(','))
            chpslist=list(d.split(','))
            if adultnumber!=0:
                if adultlist[0]=='':
                    return messagebox.showerror('Error','Enter adult details')
                elif len(adultlist)>adultnumber:
                    return messagebox.showerror('Error','More adults than specified')
                elif len(adultlist)<adultnumber:
                    return messagebox.showerror('Error','Less adults than specified')
                elif adpslist[0]=='':
                    return messagebox.showerror('Error','Enter adults passport details')
                elif len(adpslist)>adultnumber:
                    return messagebox.showerror('Error','Details more than expected')
                elif len(adpslist)<adultnumber:
                    return messagebox.showerror('Error','Less details entered')
            elif childnumber!=0:
               if childlist[0]=='':
                   return messagebox.showerror('Error','Enter child details')
               elif len(childlist)>childnumber:
                   return messagebox.showerror('Error','More children than specified')
               elif len(childlist)<childnumber:
                   return messagebox.showerror('Error','Less children than specified')
               elif chpslist[0]=='':
                   return messagebox.showerror('Error','Enter children passport details')
               elif len(chpslist)>childnumber:
                   return messagebox.showerror('Error','More details than expected')
               elif len(chpslist)<childnumber:
                   return messagebox.showerror('Error','Less details entered') 
            details.destroy()
            payments()
            
        details=tk.Tk()
        details.geometry('500x500')
        Label(details,text='Enter Your Details').grid(row=1,column=4)
        Label(details,text='Adults').grid(row=2,column=4)
        adstr=StringVar()
        chstr=StringVar()
        psadstr=StringVar()
        pschstr=StringVar()
        Entry(details,textvariable=adstr,width=40).grid(row=3,column=4)
        Label(details,text='Children').grid(row=4,column=4)
        Entry(details,textvariable=chstr,width=40).grid(row=5,column=4)
        Label(details,text='Passport Details(adults)').grid(row=6,column=4)
        Entry(details,textvariable=psadstr,width=40).grid(row=7,column=4)
        Label(details,text='Passport Details(children)').grid(row=8,column=4)
        Entry(details,textvariable=pschstr,width=40).grid(row=9,column=4)
        Button(details,text='proceed',command=command1).grid(row=10,column=5) 
       

        

def itenary(): #itenary and details window
    global flightname
    global totalprice
    global origin
    global destination
    global departure
    global arrival
    itenary=tk.Tk()
    itenary.geometry('600x500')
    Label(itenary,text='ITENARY',font='Helvetica 12 bold').grid(row=1,column=3)
    Label(itenary,text='Flight:'+flightname).grid(row=2,column=2)
    Label(itenary,text='Origin:'+origin+'      '+'Destination:'+destination).grid(row=3,column=3)
    Label(itenary,text='DepartureTime:'+departure+'          '+'ArrivalTime:'+arrival).grid(row=4,column=3)
    Label(itenary,text='Trip Duration:'+totaltime).grid(row=5,column=3)
    Label(itenary,text='TRAVELLERS',font='Helvetica 12 bold').grid(row=6,column=3)
    Label(itenary,text='Number of Adults:'+str(adultnumber)).grid(row=7,column=3)
    Label(itenary,text='Number of Children:'+str(childnumber)).grid(row=8,column=3)
    def insure():
            global totalprice
            totalprice=int(totalprice)
            totalprice=totalprice+15
            totalprice=str(totalprice)
    var3=IntVar()
    Checkbutton(itenary, text="Add Travel Insurance(OMR 15)",variable=var3,command=insure).grid(row=9,column=3)
    def func():
        itenary.destroy()
        details()
    Button(itenary,text='Proceed for booking',command=func).grid(row=10,column=4)
    itenary.mainloop()
flightname=''
totalprice=''
origin=''
destination=''
departure=''
arrival=''
def end1():#domestic forward
    global flightname
    global totalprice
    global origin
    global destination
    global departure
    global arrival
    fselection.destroy()
    flightname=flname1
    origin=f1
    destination=f2
    totalprice=tprice1
    departure=deptime2
    arrival=arrtime2
    itenary()
   
def end2():#international forward
    global flightname
    global totalprice
    global origin
    global destination
    global departure
    global arrival
    fselection.destroy()
    flightname=flname
    origin=f1
    destination=f2
    totalprice=tprice
    departure=deptime1
    arrival=arrtime1
    itenary()

def details1():#airindia
    round.destroy()
    global flightname
    global origin
    global destination
    global departure
    global arrival
    global totalprice
    global f1
    global f2
    itenary=tk.Tk()
    itenary.title('Itenary')
    itenary.geometry('500x500')
    flightname=flname1
    totalprice=str(tprice1*2)
    #onward
    airindia1()
    departure=deptime2
    arrival=arrtime2
    origin=f1
    destination=f2
    #return
    f1,f2=f2,f1
    airindia1()
    departure1=deptime2
    arrival1=arrtime2
    origin1=f1
    destination1=f2
    Label(itenary,text='Onward Flight--',font='Helvetica 12 bold').grid(row=1,column=1)
    Label(itenary,text='Flight Name:'+flightname).grid(row=2,column=2)
    Label(itenary,text=origin+'    To    '+destination).grid(row=3,column=2)
    Label(itenary,text='Departure Time:'+departure+'     '+'Arrival Time:'+arrival).grid(row=4,column=2)
    Label(itenary,text='Return Flight--',font='Helvetica 12 bold').grid(row=5,column=1)
    Label(itenary,text='Flight Name:'+flightname).grid(row=6,column=2)
    Label(itenary,text=origin1+'    To    '+destination1).grid(row=7,column=2)
    Label(itenary,text='Departure Time:'+departure1+'     '+'Arrival Time:'+arrival1).grid(row=8,column=2)#timings
    Label(itenary,text='************************').grid(row=9,column=1)
    def insure():
            global totalprice
            totalprice=int(totalprice)
            totalprice=totalprice+15
            totalprice=str(totalprice)
    def outward():
        itenary.destroy()
        details()
    var8=IntVar()
    Checkbutton(itenary, text="Add Travel Insurance(OMR 15)",variable=var8,command=insure).grid(row=10,column=2) 
    Button(itenary,text='Proceed',command=outward).grid(row=11,column=3)
def details2():#omanair
    round.destroy()
    global flightname
    global origin
    global destination
    global departure
    global arrival
    global totalprice
    global f1
    global f2
    itenary=tk.Tk()
    itenary.title('Itenary')
    itenary.geometry('500x500')
    flightname=flname
    totalprice=str(tprice*2)
     #onward
    omanair1()
    departure=deptime1
    arrival=arrtime1
    origin=f1
    destination=f2
    #return
    f1,f2=f2,f1
    omanair1()
    departure1=deptime2
    arrival1=arrtime2
    origin1=f1
    destination1=f2
    Label(itenary,text='Onward Flight--',font='Helvetica 12 bold').grid(row=1,column=1)
    Label(itenary,text='Flight Name:'+flightname).grid(row=2,column=2)
    Label(itenary,text=origin+'    To    '+destination).grid(row=3,column=2)
    Label(itenary,text='Departure Time:'+departure+'     '+'Arrival Time:'+arrival).grid(row=4,column=2)
    Label(itenary,text='Return Flight--',font='Helvetica 12 bold').grid(row=5,column=1)
    Label(itenary,text='Flight Name:'+flightname).grid(row=6,column=2)
    Label(itenary,text=origin1+'    To    '+destination1).grid(row=7,column=2)
    Label(itenary,text='Departure Time:'+departure1+'     '+'Arrival Time:'+arrival1).grid(row=8,column=2)#timings
    Label(itenary,text='************************').grid(row=9,column=1)
    def insure():
            global totalprice
            totalprice=int(totalprice)
            totalprice=totalprice+15
            totalprice=str(totalprice)
    def outward():
        itenary.destroy()
        details()
    var8=IntVar()
    Checkbutton(itenary, text="Add Travel Insurance(OMR 15)",variable=var8,command=insure).grid(row=10,column=2) 
    Button(itenary,text='Proceed',command=outward).grid(row=11,column=3)

def oneway(): #oneway-gui
    global tprice
    global tprice1
    global flname
    global flname1
    tprice=str(tprice)
    tprice1=str(tprice1)
    img=Image.open('airindia.png')
    img1=Image.open('omanair.jpg')
    img1=img1.resize((110,50),Image.ANTIALIAS)
    img=img.resize((110,50),Image.ANTIALIAS)
    render=ImageTk.PhotoImage(img)
    render1=ImageTk.PhotoImage(img1)
    Label(fselection,image=render1).place(x=100,y=210)
    Label(fselection,image=render).place(x=220,y=210)
    if flag==1:#domestic
        Label(fselection,text=f1+'  To  '+f2,font='Helvetica 12 bold').grid(row=5,column=3)
        Label(fselection,text = ">>flight2>>",font='Helvetica 12 bold').grid(row=6, column=2)
        Label(fselection,text='flight name      departure-arrival     price:').grid(row=7,column=3)
        Label(fselection,text=flname1+'      '+deptime2+'      '+arrtime2+'  '+'OMR'+tprice1).grid(row=8,column=3)
        book2=ttk.Button(fselection,text='Book',command=end1)
        book2.grid(row=8,column=5)
    else:   #international
        Label(fselection,text=f1+'  To  '+f2,font='Helvetica 12 bold').grid(row=1,column=3)
        Label(fselection,text =">>flight1>>",font='Helvetica 12 bold').grid(row=2, column=2)
        Label(fselection,text='flight name      departure-arrival     price:').grid(row=3,column=3) 
        Label(fselection,text=flname+'      '+deptime1+'    '+arrtime1+'   '+'OMR'+tprice).grid(row=4,column=3)
        book=ttk.Button(fselection,text='Book',command=end2)
        book.grid(row=4,column=5)
        Label(fselection,text=f1+'  To  '+f2,font='Helvetica 12 bold').grid(row=5,column=3)
        Label(fselection,text = ">>flight2>>",font='Helvetica 12 bold').grid(row=6, column=2)
        Label(fselection,text='flight name      departure-arrival     price:').grid(row=7,column=3)
        Label(fselection,text=flname1+'      '+deptime2+'      '+arrtime2+'  '+'OMR'+tprice1).grid(row=8,column=3)
        book2=ttk.Button(fselection,text='Book',command=end1) 
        book2.grid(row=8,column=5)
    fselection.mainloop()

def roundtrip():#roundtrip-GUI
    global f1
    global f2
    global tprice
    global tprice1
    global flname
    global flname1
    tprice=str(tprice)
    tprice1=str(tprice1)
    if flag==1:#domestic
        Label(round,text=f1+'  To  '+f2).grid(row=2,column=2)
        Label(round,text='flight name      departure--arrival     ').grid(row=3,column=2)
        Label(round,text=flname1+'      '+deptime2+'      '+arrtime2).grid(row=4,column=2)
        f1,f2=f2,f1
        airindia1()
        Label(round,text='****************',font='Helvetica 12 bold').grid(row=5,column=1)
        Label(round,text=f1+'  To  '+f2).grid(row=6,column=2)
        Label(round,text='flight name      departure--arrival     ').grid(row=7,column=2)
        Label(round,text=flname1+'      '+deptime2+'      '+arrtime2).grid(row=8,column=2)
        Label(round,text='TotalPrice OMR:'+str(tprice1*2)).grid(row=9,column=2)
        f2,f1=f1,f2
        Button(round,text='book',command=details1).grid(row=10,column=3)
    else:#international
        Label(round,text=f1+'  To  '+f2).grid(row=2,column=2)
        Label(round,text='Flight1>>>>',font='Helvetica 12 bold').grid(row=2,column=1)
        Label(round,text='flight name      departure--arrival     ').grid(row=3,column=2)
        Label(round,text=flname+'      '+deptime1+'    '+arrtime1).grid(row=4,column=2)
        f1,f2=f2,f1
        omanair1()
        Label(round,text='******************').grid(row=5,column=1)
        Label(round,text=f1+'  To  '+f2).grid(row=6,column=2)
        Label(round,text='flight name      departure-arrival     price:').grid(row=7,column=2) 
        Label(round,text=flname+'      '+deptime1+'    '+arrtime1).grid(row=8,column=2)
        Label(round,text='TotalPrice: OMR'+str(tprice*2)).grid(row=9,column=2)
        Button(round,text='Book',command=details2).grid(row=10,column=3)
        Label(round,text='-------------------------').grid(row=11,column=1)
        f2,f1=f1,f2
        #####
        airindia1()
        Label(round,text='Flight2>>>>',font='Helvetica 12 bold').grid(row=12,column=1)
        Label(round,text=f1+'  To  '+f2).grid(row=12,column=2)
        Label(round,text='flight name      departure--arrival     ').grid(row=13,column=2)
        Label(round,text=flname1+'      '+deptime2+'      '+arrtime2).grid(row=14,column=2)
        f1,f2=f2,f1
        airindia1()
        Label(round,text='******************').grid(row=15,column=1)
        Label(round,text=f1+'  To  '+f2).grid(row=16,column=2)
        Label(round,text='flight name      departure--arrival     ').grid(row=17,column=2)
        Label(round,text=flname1+'      '+deptime2+'      '+arrtime2).grid(row=18,column=2)
        Label(round,text='TotalPrice: OMR'+str(tprice1*2)).grid(row=19,column=2)
        Button(round,text='Book',command=details1).grid(row=20,column=3)
        f2,f1=f1,f2
    round.mainloop()
if selection=='1':
    fselection=tk.Tk()
    fselection.title('TripLife-Flightdetails-oneway') 
    fselection.geometry('700x400')
    oneway()
if selection=='2':
    round=tk.Tk()
    round.title('RoundTrip')
    round.geometry('600x500')
    roundtrip()
