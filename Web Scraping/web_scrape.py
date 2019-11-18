import re
import csv
import urllib.request as ur
from bs4 import BeautifulSoup
import requests


url = 'https://www.timeanddate.com/weather/india/chennai/historic'
d = ur.urlopen(url)
soup =BeautifulSoup(d,'html.parser')

tab = soup.find('table', {'class': 'zebra tb-wt fw va-m tb-hover'})

print("STEP1")



col = tab.findAll(text='Temp')
col.append(tab.findAll(text='Weather')[0])
col.append(tab.findAll(text='Wind')[0])
col.append(tab.findAll(text='Humidity')[0])
col.append(tab.findAll(text='Barometer')[0])
col.append(tab.findAll(text='Visibility')[0])


print("STEP2")



c0 = tab.find('tbody')
un_clean=[]
for i in c0:
    rows=i.find_all('td')
    rows=[x.text.strip() for x in rows]
    rows.pop(0)
    rows.pop(3)
    un_clean.append(rows)
print(len(un_clean))
print(un_clean[0])

print("STEP3")


direc = tab.findAll('span', {'class': 'comp'})
#print(direc)
title =[]
for i in direc:
    title.append(i['title'])
print(len(title))
print(title[0])


print("STEP4")

import pandas as pd
df = pd.DataFrame(un_clean,columns=col)
df.insert(3,'Direction',title)
print(df.head(5))

print("STEP5")

def modify(col_name,unit,conv_unit):
    templist = list(df[col_name])
    l=[]
    for i in templist:
        l.append(i.strip(unit))
    my_new_list=[]
    for x in l:
        if x=='No wind':
            x= x.replace(" ","")
            my_new_list.append(x)
        else:
            string=conv_unit
            x = x + string
            my_new_list.append(x)

    print(my_new_list)
    df[col_name] = my_new_list
    print(df[col_name].head(5))

w= list(df['Weather'])
wl=[]
for i in w:
    i= i.replace(" ", "")
    wl.append(i)

b= list(df['Barometer'])
bl=[]
for i in b:
    i= i.replace(" ", "")
    bl.append(i)

modify('Temp','\xa0°F','°F')
modify('Wind',' mph','mph')
#modify('Barometer',' "Hg','"Hg')
modify('Visibility','\xa0mi','mi')
df['Weather'] = wl
df['Barometer'] = bl
print(df.head(5))

print("STEP6")


data = [df.columns.values.tolist()] + df.values.tolist()

with open('data.csv','w',newline='') as f:
    w = csv.writer(f) 
    w.writerows(data) 

