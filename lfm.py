from time import sleep
import datetime
import urllib
import re
import os

# You have to have your own unique two values for API_KEY and API_SECRET
# Obtain yours from http://www.last.fm/api/account for Last.fm
API_KEY =    "e09f752b88d2e0d7d71b8f178d931970" # this is a sample key
API_SECRET = "8562cb7ab597776e0f92cabf6fc19dda"
Metro_URL = "http://ws.audioscrobbler.com/2.0/?method=geo.getmetros&api_key="+API_KEY
Dates_URL = "http://ws.audioscrobbler.com/2.0/?method=geo.getmetroweeklychartlist&api_key="+API_KEY

def duration2min(time):
    totalTime = int(time)/60
    seconds = int(time)%60
    if seconds < 10:
        ans = str(totalTime)+':'+"0"+str(seconds)
    else:
        ans = str(totalTime)+':'+str(seconds)
    return ans
def retriveListOfMetroes():
    ufile = urllib.urlopen(Metro_URL)
    sleep(2)
    html_page = ufile.read()
    tmpList = re.findall(ur"<name>(.+)</name>[\s]*<country>(.+)</country>",html_page)
    return tmpList
def retriveDates():
    ufile = urllib.urlopen(Dates_URL)
    sleep(2)
    html_page = ufile.read()
    tmpList = re.findall(r'<chart from="([0-9]+)" to="[0-9]+"/>',html_page)
    return tmpList

def listoftime():
    List_of_Dates=retriveDates()
    LIST_OF_Metroes=retriveListOfMetroes()
    try:
        ListofDate
    except NameError:
        ListofDate = None
    for CurrentDate in range(len(List_of_Dates)):
        TIME = (int(datetime.datetime.fromtimestamp(int(List_of_Dates[CurrentDate])+86400).strftime('%Y')),int(datetime.datetime.fromtimestamp(int(List_of_Dates[CurrentDate])+86400).strftime('%m')),int(datetime.datetime.fromtimestamp(int(List_of_Dates[CurrentDate])+86400).strftime('%d')))
        if ListofDate==None:
            ListofDate=datetime.datetime.fromtimestamp(int(List_of_Dates[CurrentDate])+86400).strftime('%Y')+'0'+str(datetime.date(TIME[0],TIME[1],TIME[2]).isocalendar()[1])+','
        else:
            if (datetime.date(TIME[0],TIME[1],TIME[2]).isocalendar()[1])>9:
                ListofDate+=datetime.datetime.fromtimestamp(int(List_of_Dates[CurrentDate])+86400).strftime('%Y')+str(datetime.date(TIME[0],TIME[1],TIME[2]).isocalendar()[1])+','
            else:
                ListofDate+=datetime.datetime.fromtimestamp(int(List_of_Dates[CurrentDate])+86400).strftime('%Y')+'0'+str(datetime.date(TIME[0],TIME[1],TIME[2]).isocalendar()[1])+','
    NameDate=eval(ListofDate)
    ListofDate=zip(List_of_Dates,NameDate)
    return ListofDate

def Download(Start,End):
    ListofDates=listoftime()
    Timer=0
    start,end=0,0
    for CDate in range(len(ListofDates)):
        if ListofDates[CDate][1]==int(Start):
            start=CDate
        if ListofDates[CDate][1]==int(End):
            end=CDate+1
    if start==0:
        print "The start date is incorrect or non existant"
    if end==0:
        print "The end date is incorrect or non existant"
    ListofDate=ListofDates[start:end]
    if not os.path.exists('raw_data'):
        os.makedirs('raw_data')  
    for CDate in range(len(ListofDate)):
        CurrentName='.\\raw_data\\'+str(ListofDate[CDate][1])+'.csv'
        Timer+=1
        if os.path.exists(CurrentName)==False:
            f = open(CurrentName, 'w')
            for CurrentMetro in LIST_OF_Metroes:
                urlm = str("http://ws.audioscrobbler.com/2.0/?method=geo.getmetrotrackchart&country="+str(CurrentMetro[1])+"&metro="+str(CurrentMetro[0])+"&start="+str(ListofDate[CDate][0])+"&end="+str(int(ListofDate[CDate][0])+604800)+"&limit=20&api_key="+str(API_KEY))
                ufile = urllib.urlopen(urlm)
                sleep(1.1)
                html_page = ufile.read()
                tmpList = re.findall(u'<track rank="[\w]*">[.\s]*<name>(.+)</name>[.\s]*<duration>([0-9]+)</duration>[.\s]*<listeners>([0-9]*)</listeners>[^"]*.*[\s]*<artist>[\s]*<name>(.*)</name>',html_page)
                if tmpList:
                    for i in range(len(tmpList)):
                        f.write(str(ListofDate[CDate][1])+' , '+'"'+tmpList[i][0]+'"'+' , '+'"'+tmpList[i][3]+'"'+' , '+duration2min(tmpList[i][1])+' , '+str(i+1)+' , '+str(tmpList[i][2])+' , '+'"'+CurrentMetro[0]+'"'+' , '+'"'+CurrentMetro[1]+'"'+'\n')
            f.close()
        else:
            print ListofDate[CDate][1]
        
           
Download()
