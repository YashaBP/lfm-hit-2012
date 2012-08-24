#import pylast
from time import sleep
import datetime
import urllib
import re
#import os

# You have to have your own unique two values for API_KEY and API_SECRET
# Obtain yours from http://www.last.fm/api/account for Last.fm
API_KEY =    "e09f752b88d2e0d7d71b8f178d931970" # this is a sample key
API_SECRET = "8562cb7ab597776e0f92cabf6fc19dda"
COUNTRY_URL = "http://www.last.fm/charts"
Metro_URL = "http://ws.audioscrobbler.com/2.0/?method=geo.getmetros&api_key=e09f752b88d2e0d7d71b8f178d931970"
Dates_URL = "http://ws.audioscrobbler.com/2.0/?method=geo.getmetroweeklychartlist&api_key=e09f752b88d2e0d7d71b8f178d931970"

#def retriveListOfCountries():
#    ufile = urllib.urlopen(COUNTRY_URL)
#    html_page = ufile.read()
#    tmpList = re.findall(u'<option value="([a-zA-Z,\s]+)"',html_page)
#    return tmpList
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
    #print tmpList
    return tmpList
def retriveDates():
    ufile = urllib.urlopen(Dates_URL)
    sleep(2)
    html_page = ufile.read()
    tmpList = re.findall(r'<chart from="([0-9]+)" to="[0-9]+"/>',html_page)
    return tmpList
#def reprunicode(u):
#    return repr(u).decode('raw_unicode_escape')

LIST_OF_Metroes=retriveListOfMetroes()
#LIST_OF_COUNTRIES=retriveListOfCountries()
Timer=0


def listoftime():
    List_of_Dates=retriveDates()
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

def Download():
    ListofDate=listoftime()
    Timer=0
#    os.chdir(".\\raw_data")
    for CDate in range(len(ListofDate)):
        if os.path.exists(str(ListofDate[CDate][1])+'.csv')==False:
            f = open(str(".\\raw_data\\"+ListofDate[CDate][1])+'.csv', 'w')
            for CurrentMetro in LIST_OF_Metroes:
                urlm = str("http://ws.audioscrobbler.com/2.0/?method=geo.getmetrotrackchart&country="+str(CurrentMetro[1])+"&metro="+str(CurrentMetro[0])+"&start="+str(ListofDate[CDate][0])+"&end="+str(ListofDate[CDate+1][0])+"&limit=20&api_key=e09f752b88d2e0d7d71b8f178d931970")
                ufile = urllib.urlopen(urlm)
                sleep(1.1)
                html_page = ufile.read()
                tmpList = re.findall(u'<track rank="[\w]*">[.\s]*<name>(.+)</name>[.\s]*<duration>([0-9]+)</duration>[.\s]*<listeners>([0-9]*)</listeners>[^"]*.*[\s]*<artist>[\s]*<name>(.*)</name>',html_page)
                Timer+=1
                if tmpList:
                    for i in range(len(tmpList)):
                        f.write(str(ListofDate[CDate][1])+' , '+'"'+tmpList[i][0]+'"'+' , '+'"'+tmpList[i][3]+'"'+' , '+duration2min(tmpList[i][1])+' , '+str(i+1)+' , '+str(tmpList[i][2])+' , '+'"'+CurrentMetro[0]+'"'+' , '+'"'+CurrentMetro[1]+'"'+'\n')
                        print(str(ListofDate[CDate][1])+' , '+'"'+tmpList[i][0]+'"'+' , '+'"'+tmpList[i][3]+'"'+' , '+duration2min(tmpList[i][1])+' , '+str(i+1)+' , '+str(tmpList[i][2])+' , '+'"'+CurrentMetro[0]+'"'+' , '+'"'+CurrentMetro[1]+'"'+'\n')
            f.close()
        else:
            print ListofDate[CDate][1]
        
            

Download()
        
'''network = pylast.LastFMNetwork(api_key = API_KEY, api_secret = API_SECRET)
sleep(2)



for currentCountry in LIST_OF_COUNTRIES:
    country = network.get_country(currentCountry)
    sleep(1)
    top = country.get_top_tracks()
    #network.ws_server
    sleep(1)
    #name of the top artist
    print top[0].item.title
    sleep(1)'''
'''#create connection to last fm network
network = pylast.LastFMNetwork(api_key = API_KEY, api_secret = API_SECRET)
#timestamp
timestamp= str(d.date())+"-"+str(d.hour)
# country
country = network.get_country("Spain")
top = country.get_top_tracks()
#name of the top artist
top[0].item.get_artist().get_name()
#name of the song
top[0].item.get_title()
#number of listeners (scrobblers - lastfm listeners)
top[0].item.get_playcount()
#duration 
duration2min(top[0].item.get_duration())
#album name
top[0].item.get_album().get_name()'''
