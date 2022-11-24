import pandas as pd
from bs4 import BeautifulSoup
import numpy as np
from datetime import datetime
#from .WriteToFile import Helper
import os
import re
from googletrans import Translator


local_timezone = datetime.utcnow().astimezone().utcoffset()
            #Read which time one gets home
print("Please enter the time you get home (24h format)")
print(end=">") 
TimeGetHome = input()
TimeGetHome = datetime.strptime(TimeGetHome,"%H:%M")


page = ''
            #Sky Sports Web Page cached into WebPage1
cur_dir = os.path.dirname(os.path.abspath(__file__))
with open(cur_dir + '/WebPage1.txt') as f:
   for i in f:
    page+=i
PageXML = BeautifulSoup(page, 'html.parser')
body_of_tableXML = PageXML.find('div', {'data-sport':'football'})
            #Scrape the names and dates
Names = body_of_tableXML.findAll('span', {'class':'swap-text__target'})
dates = body_of_tableXML.findAll('span', {'class':'matches__date'})



            #goal.com Web Page cached into WebPage2   
with open(cur_dir + '/WebPage2.txt') as f:
   for i in f:
    page+=i
PageXML = BeautifulSoup(page, 'html.parser')
body_of_tableXML = PageXML.find('div', {'class':'table-container-scroll'})
FreeNames = body_of_tableXML.find_all('td')
            #Clean the Names into a string array
FreeNamesClean = ''
for j in range(len(FreeNames)):
    if(j%3 == 0):   
        FreeNamesClean += (re.sub('</*td>',"",str(FreeNames[j]))).replace(" ","")
FreeNamesClean = FreeNamesClean.split('-')


#Translate from Arabic DS
translator = Translator()
# for i in FreeNamesClean:
#     (translator.translate('hi'))

            #Output the matches and analytics we need
numberOfFreeGames = 0
numberOfFreeRO16Games = 0
numberOfFreeQfGames = 0
numberofgames = int(len(Names))
FreeGameIndex = 0
print ("{:<15} {:<25} {:<25} {:<25}".format('Game no.','Team 1', 'Times', 'Team 2'))
numberofgamesWatched = 0
for i,j in zip(range(0,numberofgames,2),range(numberofgames)): # j is for regular count while i counts 2 steps in order to treat the DSs as pairs
    TimeOfMatch = datetime.strptime((dates[j].contents[0].strip()),"%H:%M") + local_timezone
    if(TimeOfMatch >= TimeGetHome):
        print("{:<15} {:<25} {:<25} {:<25}".format(j+1, Names[i].contents[0],TimeOfMatch.strftime("%H:%M"),Names[i+1].contents[0]))
        numberofgamesWatched+=1
        if(j >= 60 and j!=63): #Finals are all free except losers final
             numberOfFreeGames += 1
        if((Names[i].contents[0] == FreeNamesClean[FreeGameIndex] and Names[i+1].contents[0] == FreeNamesClean[FreeGameIndex+1])): #Free matches collected from goal.com DS
             numberOfFreeGames += 1
             FreeGameIndex += 2
        if(j >= 48 and j<=55 and numberOfFreeRO16Games < 5): # 5 free matches from round of 16
            numberOfFreeRO16Games+=1
        if(j >= 56 and j<=59 and numberOfFreeQfGames < 3): 
            numberOfFreeQfGames+=1
numberOfFreeGames = numberOfFreeGames + numberOfFreeRO16Games + numberOfFreeQfGames
print("You will watch {:<2} matches and {:<2} free".format(numberofgamesWatched,numberOfFreeGames))