
# Import Required Library 
from tkinter import *
from tkcalendar import Calendar 
from datetime import date
import os 
import xml.etree.ElementTree as ET

# Create Object 
page = Tk() 

#get current date
today = date.today()


## csv file read to import limit data
import csv
#dictionary to store all limit
dailyLimit = {}
mobileLimit = {}

with open('LimitFile/dailyLimit.csv', 'r') as file:
    reader = csv.reader(file)
    next(reader)
    for row in reader:
        dailyLimit[row[0]] = row[1]
        
# print(dailyLimit)


with open('LimitFile/mobileLimit.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        if(int(row[1])<0):
            row[1] = '0'
        mobileLimit[row[0]] = row[1]
       
# print(mobileLimit)

## end of csv file read to import limit data


y = int(today.strftime("%Y"))
m = int(today.strftime("%m"))
d = int(today.strftime("%d"))
# Set geometry 
page.geometry("400x400") 
  
# Add Calender 
cal = Calendar(page, selectmode = 'day', 
               year = y, month = m, day = d, 
               firstweekday = 'sunday', weekenddays = [6,7], 
               date_pattern = "dd.mm.yy", showweeknumbers = False, 
               weekendbackground = 'Light Green') 
  
cal.pack(pady = 5) 
  
def grad_date(): 
    date.config(text = "Selected Date is: " + cal.get_date()) 
    date_c = cal.get_date()
    date_list = date_c.split(".")
    month = ['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC']

    file_start = str(y) + date_list[1] + date_list[0]
    file_end = "*.xml"


    ch_dir = '\\\\150.1.62.26\\'+str(y)+'\\'+ month[int(date_list[1])-1] + '-' + date_list[2]

    #creating month folder in required destination using date format
    if not os.path.exists(ch_dir):
        os.mkdir(ch_dir) 
    
    os.chdir(ch_dir)
    

    #creating date folder in required destination using date format
    if not os.path.exists(date_c):
        os.mkdir(date_c) 


    src = "\\\\150.1.62.2\MottaiXML\\"
    
    #src = "E:\Projects\LimitPY\FinalProjectBefore_run\src\\"
    #dst = "E:\Projects\LimitPY\FinalProjectBefore_run\dst"

    dst = ch_dir + "\\" + date_c
    #dst = "\\\\150.1.62.26\\2021\MAR-21\\" + "test"

    cmd = "copy " + src + file_start + file_end +' '+ dst
    os.system(cmd)

    os.chdir(dst)

    cli_files = os.listdir('.')

    for cl_file in cli_files:
        if cl_file.endswith("-clients-RBS.xml"):
            xml_to_read = cl_file
            break

    tree = ET.parse(xml_to_read)
    root = tree.getroot()
    print('Client Code', '\t\t[Old]', '\t\t[New]')
    for limit in root.findall('Limits'):            # using root.findall() to avoid removal during traversal
        client = str(limit.find('ClientCode').text)
        cash = limit.find('Cash').text

        new_cash = dailyLimit.get(client,'noNeed')  #collecting cash limit if required to change
        #print(client,': ',new_cash)

        mobile_limit = mobileLimit.get(client,'noNeed') #collecting mobile limit 
        
        if new_cash !='noNeed' and int(new_cash) > int(cash):
            limit.find('Cash').text = new_cash
            print(client, '\t\t',cash, '\t\t',new_cash)

        if mobile_limit != 'noNeed':
            limit.find('Cash').text = mobile_limit
            print(client, '\t\t',cash, '\t\t',mobile_limit, '\tMobile code')

        
    tree.write('new.xml')

    toFormatXML = open("new.xml", "r")
    content = toFormatXML.read()
    toFormatXML.close()
    os.remove("new.xml")
    os.remove(xml_to_read)
    firstLine = "<?xml version=\"1.0\" encoding=\"utf-8\"?>\n\n"

    formatXML = open(xml_to_read, "w")
    formatXML.write(firstLine)
    formatXML.write(content)
    formatXML.close()
    print("Done")



# Add Button and Label 
Button(page, text = "Generate", command = grad_date).pack(pady = 20) 


date = Label(page, text = "") 
date.pack(pady = 5) 


Button(page, text = "Exit", command = exit).pack(pady = 10)    
# Excecute Tkinter 
page.mainloop()
