from time import sleep
import datetime
import urllib
import re
import os
import wx

API_KEY =    "e09f752b88d2e0d7d71b8f178d931970" 
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
    LIST_OF_Metroes=retriveListOfMetroes()
    ListofDate=listoftime()
    Timer=0
    for CDate in range(len(ListofDate)):
        if os.path.exists('.\\raw_data\\'+str(ListofDate[CDate][1])+'.csv')==False:
            f = open('.\\raw_data\\'+str(ListofDate[CDate][1])+'.csv', 'w')
            for CurrentMetro in LIST_OF_Metroes:
                urlm = str("http://ws.audioscrobbler.com/2.0/?method=geo.getmetrotrackchart&country="+str(CurrentMetro[1])+"&metro="+str(CurrentMetro[0])+"&start="+str(ListofDate[CDate][0])+"&end="+str(int(ListofDate[CDate][0])+604800)+"&limit=20&api_key="+str(API_KEY))
                ufile = urllib.urlopen(urlm)
                sleep(1.1)
                html_page = ufile.read()
                tmpList = re.findall(u'<track rank="[\w]*">[.\s]*<name>(.+)</name>[.\s]*<duration>([0-9]+)</duration>[.\s]*<listeners>([0-9]*)</listeners>[^"]*.*[\s]*<artist>[\s]*<name>(.*)</name>',html_page)
                Timer+=1
                if tmpList:
                    for i in range(len(tmpList)):
                        f.write(str(ListofDate[CDate][1])+' , '+'"'+tmpList[i][0]+'"'+' , '+'"'+tmpList[i][3]+'"'+' , '+duration2min(tmpList[i][1])+' , '+str(i+1)+' , '+str(tmpList[i][2])+' , '+'"'+CurrentMetro[0]+'"'+' , '+'"'+CurrentMetro[1]+'"'+'\n')
            f.close()
        else:
            Timer+=214
            print ListofDate[CDate][1]     
#Download()
#GUI part
class MainWindow(wx.Frame):
    def __init__(self, *args, **kw):
        super(MainWindow, self).__init__(*args, **kw) 
        self.InitUI()
    def InitUI(self):
        pnl = wx.Panel(self)
        #creating sizers
        verticalBox = wx.BoxSizer(wx.VERTICAL)
        horizontalBox1 = wx.BoxSizer(wx.HORIZONTAL)
        horizontalBox2 = wx.BoxSizer(wx.HORIZONTAL)
        horizontalBox3 = wx.BoxSizer(wx.HORIZONTAL)
        horizontalBox4 = wx.BoxSizer(wx.HORIZONTAL)
        horizontalBox5 = wx.BoxSizer(wx.HORIZONTAL)
        #creating widgets
        #static text
        self.text1 = wx.StaticText(pnl,label="\nPlease select weeks range in format <yyyyww>")
        self.text2 = wx.StaticText(pnl,label="Beginning from:\t")
        self.text3 = wx.StaticText(pnl,label="\tEnding on:")

        #Text Controls
        self.fromTextBox = wx.TextCtrl(pnl,style = wx.TE_CENTRE)
        self.endTextBox = wx.TextCtrl(pnl, style = wx.TE_CENTRE)
        #applying to box sizers
        horizontalBox1.Add(self.text1,proportion=1)
        horizontalBox2.Add(self.text2,proportion=1,flag = wx.ALIGN_CENTRE)
        horizontalBox2.Add(self.fromTextBox,proportion=1)
        horizontalBox2.Add(self.text3,proportion=1,flag = wx.ALIGN_CENTRE)
        horizontalBox2.Add(self.endTextBox, proportion=1)
        verticalBox.Add(horizontalBox1,flag = wx.ALIGN_CENTRE)
        verticalBox.Add((0,20))
        verticalBox.Add(horizontalBox2,flag = wx.ALIGN_CENTRE)
        #setting main panel sizer
        pnl.SetSizer(verticalBox)
        #window properties
        self.SetSize((500,300))
        self.SetTitle("Last.fm downloader")
        self.Centre()
        self.Show(True)






















        

app = wx.App()
MainWindow(None)
app.MainLoop()
