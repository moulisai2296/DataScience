#Importing Libraries
import re
import csv
import urllib.request as ur
from bs4 import BeautifulSoup
import requests

#Opening URL of the website to scrape
url = 'https://www.timeanddate.com/weather/india/chennai/historic'
d = ur.urlopen(url)

#Extracting all HTML code of the URL
soup =BeautifulSoup(d,'html.parser')
tab = soup.find('table', {'class': 'zebra tb-wt fw va-m tb-hover'}) #Finding required table

#Scraping Column names of a table present in the URL
col = tab.findAll(text='Temp')
col.append(tab.findAll(text='Weather')[0])
col.append(tab.findAll(text='Wind')[0])
col.append(tab.findAll(text='Humidity')[0])
col.append(tab.findAll(text='Barometer')[0])
col.append(tab.findAll(text='Visibility')[0])

#Getting all table data and cleaning HTML tags from it
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


direc = tab.findAll('span', {'class': 'comp'})
#print(direc)
title =[]
for i in direc:
    title.append(i['title'])
print(len(title))
print(title[0])

#Creating a dataframe and storing the scraped table values in it.
import pandas as pd
df = pd.DataFrame(un_clean,columns=col)
df.insert(3,'Direction',title)
print(df.head(5))

def modify(col_name,unit,conv_unit):
    ''' Function used to do unit conversions of different metrics and 
        to perform some cleaning of additional spaces'''
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
    #print(my_new_list)
    df[col_name] = my_new_list

#Cleaning Weather and Barometer columns
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

#Appling function on DataFrame columns
modify('Temp','\xa0°F','°F')
modify('Wind',' mph','mph')
modify('Visibility','\xa0mi','mi')
df['Weather'] = wl
df['Barometer'] = bl
print(df.head(5))

#Storing the scrapped data from Data Frame to .CSV file
data = [df.columns.values.tolist()] + df.values.tolist()
with open('data.csv','w',newline='') as f:
    w = csv.writer(f) 
    w.writerows(data) 
