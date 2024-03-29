from time import sleep
import datetime
import urllib
import re
import os
import wx
import thread
import webbrowser

API_KEY =    ("e09f752b88d2e0d7d71b8f178d931970","e09f752b88d2e0d7d71b8f178d931970")
API_SECRET = "8562cb7ab597776e0f92cabf6fc19dda"
Metro_URL = "http://ws.audioscrobbler.com/2.0/?method=geo.getmetros&api_key="+API_KEY[1]
Dates_URL = "http://ws.audioscrobbler.com/2.0/?method=geo.getmetroweeklychartlist&api_key="+API_KEY[0]
RAW_DATA_PATH = ".\\raw_data\\"
TABLE_FILE_NAME = "lfm_table.csv"


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
    sleep(1)
    html_page = ufile.read()
    tmpList = re.findall(ur"<name>(.+)</name>[\s]*<country>(.+)</country>",html_page)
    return tmpList
def retriveDates():
    ufile = urllib.urlopen(Dates_URL)
    sleep(1)
    html_page = ufile.read()
    tmpList = re.findall(r'<chart from="([0-9]+)" to="[0-9]+"/>',html_page)
    return tmpList

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


#GUI part
class MainWindow(wx.Frame):
    def __init__(self, *args, **kw):
        super(MainWindow, self).__init__(*args, **kw) 
        self.InitUI()
    def InitUI(self):
        icon = wx.Icon('lastfm.ico', wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)
        self.stopBtnPressed = False
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
        self.gauge = wx.Gauge(pnl, range = 0,size = (480,30))
        self.actionTxt = wx.StaticText(pnl, label ="Current action:\t")
        self.actionDetailsTxt = wx.StaticText(pnl, label = "waiting for action...")
        self.downloadBtn = wx.Button(pnl,id=wx.ID_DOWN, label = "Download")
        self.stopBtn = wx.Button(pnl,id=wx.ID_CANCEL, label = "Stop")
        self.mergeBtn = wx.Button(pnl,id=wx.ID_REFRESH,label = "Merge to '"+TABLE_FILE_NAME+"'")
        self.uploadBtn = wx.Button(pnl,id=wx.ID_UP, label = "Run visualization")
        #Text Controls
        self.fromTextBox = wx.TextCtrl(pnl,style = wx.TE_CENTRE)
        self.endTextBox = wx.TextCtrl(pnl, style = wx.TE_CENTRE)
        #applying to box sizers
        horizontalBox1.Add(self.text1,proportion=1)
        horizontalBox2.Add(self.text2,proportion=1,flag = wx.ALIGN_CENTRE)
        horizontalBox2.Add(self.fromTextBox,proportion=1)
        horizontalBox2.Add(self.text3,proportion=1,flag = wx.ALIGN_CENTRE)
        horizontalBox2.Add(self.endTextBox, proportion=1)
        horizontalBox3.Add(self.gauge, proportion=1, flag = wx.ALIGN_CENTRE)
        horizontalBox4.Add(self.actionTxt,proportion=1, flag = wx.ALIGN_CENTRE)
        horizontalBox4.Add(self.actionDetailsTxt,proportion=1, flag = wx.ALIGN_CENTRE)
        horizontalBox4.Add((130,0))#empty box
        horizontalBox5.Add(self.downloadBtn,proportion=0.25, flag = wx.ALIGN_CENTRE)
        horizontalBox5.Add(self.stopBtn,proportion=0.25, flag = wx.ALIGN_CENTRE)
        horizontalBox5.Add(self.mergeBtn,proportion=0.25, flag = wx.ALIGN_CENTRE)
        horizontalBox5.Add(self.uploadBtn,proportion=0.25, flag = wx.ALIGN_CENTRE)
        verticalBox.Add(horizontalBox1,flag = wx.ALIGN_CENTRE)
        verticalBox.Add((0,20))#blank line
        verticalBox.Add(horizontalBox2,flag = wx.ALIGN_CENTRE)
        verticalBox.Add((0,10))#blank line
        verticalBox.Add(horizontalBox3,flag = wx.ALIGN_CENTRE)
        verticalBox.Add((0,10))#blank line
        verticalBox.Add(horizontalBox4,flag = wx.ALIGN_CENTRE)
        verticalBox.Add((0,20))#blank line
        verticalBox.Add(horizontalBox5,flag = wx.ALIGN_CENTRE)
        #setting main panel sizer
        pnl.SetSizer(verticalBox)
        #Binding button events
        self.Bind(wx.EVT_BUTTON, self.onDownloadPressed, self.downloadBtn)
        self.Bind(wx.EVT_BUTTON, self.onStopPressed, self.stopBtn)
        self.Bind(wx.EVT_BUTTON, self.onMergePressed,self.mergeBtn)
        self.Bind(wx.EVT_BUTTON, self.onVisualizationPressed,self.uploadBtn)
        #window properties
        self.SetSize((500,230))
        self.SetTitle("Last.fm data downloader")
        self.Centre()
        self.Show(True)
    def onDownloadPressed(self,btnEvent):
        try:
            start = int( self.fromTextBox.GetValue() )
            end = int( self.endTextBox.GetValue() )
            thread.start_new_thread(self.Download,(start,end))
        except:
            wx.MessageBox("Empty start week or and of week","Error",wx.OK | wx.ICON_ERROR)
    def onStopPressed(self, btnEvent):
        self.stopBtnPressed = True
    def onMergePressed(self, btnEvent):
        #merging all files from .\raw_data to .\table.csv
        self.actionDetailsTxt.SetLabel("Merging to "+TABLE_FILE_NAME)
        self.actionDetailsTxt.Update()
        sleep(1)
        fileList = os.listdir(RAW_DATA_PATH)
        mergedFile = open(".\\"+TABLE_FILE_NAME,"a")
        mergedFile.write("Date|Song name|Artist name|Song running time|Song position|Unique listeners|Metro name|Country name\n")
        for currentFileName in fileList: 
            currentFile = open(RAW_DATA_PATH +currentFileName,"r")
            for line in currentFile:
                mergedFile.write(line)
            currentFile.close()
        mergedFile.close()    
        self.actionDetailsTxt.SetLabel("Waiting for action")
        #some logic here
    def onVisualizationPressed(self, btnEvent):
        #Upload .\table.csv to google fusion tables
        self.actionDetailsTxt.SetLabel('Starting visualization...')
        self.actionDetailsTxt.Update()
        sleep(1)
        webbrowser.open_new(".\\Visualization\\start.html")
        self.actionDetailsTxt.SetLabel("Waiting for action")
        #some logic here        
    def Download(self,Start,End):
        self.stopBtnPressed = False #when user clicks download, it is not possible that stop button pressed concurrently
        numberOfFilesToDownload = End - Start
        wx.CallAfter(self.gauge.SetRange,(numberOfFilesToDownload+1)*214+3)
        wx.CallAfter(self.actionDetailsTxt.SetLabel,"Retrieving list of available weeks")
        wx.CallAfter(self.gauge.SetValue,1)
        ListofDates=listoftime()
        start,end=-1,-1
        for CDate in range(len(ListofDates)):
            if ListofDates[CDate][1]==int(Start):
                start=CDate
            if ListofDates[CDate][1]==int(End):
                end=CDate+1
        if start==-1:
            wx.MessageBox("The start date is incorrect or non existant","Error",wx.OK | wx.ICON_INFORMATION)
        elif end==-1:
            wx.MessageBox("The end date is incorrect or non existant","Error",wx.OK | wx.ICON_INFORMATION)
        else:
            wx.CallAfter(self.actionDetailsTxt.SetLabel,"Retrieving list of metros")
            wx.CallAfter(self.gauge.SetValue,2)
            LIST_OF_Metroes=retriveListOfMetroes()
            Timer=3            
            ListofDate=ListofDates[start:end]
            if not os.path.exists('raw_data'):
                wx.CallAfter(self.actionDetailsTxt.SetLabel,"Creating raw_data directory")
                os.makedirs('raw_data')
                sleep(2)
            for CDate in range(len(ListofDate)):
                CurrentName=RAW_DATA_PATH+str(ListofDate[CDate][1])+'.csv'
                
                if os.path.exists(CurrentName)==False:
                    f = open(CurrentName, 'w')
                    for CurrentMetro in LIST_OF_Metroes:
                        Timer+=1
                        wx.CallAfter(self.gauge.SetValue,Timer)
                        wx.CallAfter(self.actionDetailsTxt.SetLabel,"downloading "+CurrentName+" metro: "+CurrentMetro[0])
                        if self.stopBtnPressed:
                            break
                        urlm = str("http://ws.audioscrobbler.com/2.0/?method=geo.getmetrotrackchart&country="+str(CurrentMetro[1])+"&metro="+str(CurrentMetro[0])+"&start="+str(ListofDate[CDate][0])+"&end="+str(int(ListofDate[CDate][0])+604800)+"&limit=20&api_key="+str(API_KEY[Timer%2]))
                        ufile = urllib.urlopen(urlm)
                        sleep(0.5)
                        html_page = ufile.read()
                        tmpList = re.findall(u'<track rank="[\w]*">[.\s]*<name>(.+)</name>[.\s]*<duration>([0-9]+)</duration>[.\s]*<listeners>([0-9]*)</listeners>[^"]*.*[\s]*<artist>[\s]*<name>(.*)</name>',html_page)
                        if tmpList:
                            for i in range(len(tmpList)):
                                f.write(str(ListofDate[CDate][1])+'|'+tmpList[i][0]+'|'+tmpList[i][3]+'|'+duration2min(tmpList[i][1])+'|'+str(i+1)+'|'+str(tmpList[i][2])+'|'+CurrentMetro[0]+'|'+CurrentMetro[1]+'\n')
                    f.close()
                    if self.stopBtnPressed:
                        wx.CallAfter(self.actionDetailsTxt.SetLabel,"Downloading stopped by user!!!")
                        sleep(1.5)
                        wx.CallAfter(self.actionDetailsTxt.SetLabel,"Deleting unfinished file: "+CurrentName)
                        sleep(1)
                        os.remove(CurrentName)
                        wx.CallAfter(self.actionDetailsTxt.SetLabel,"Unfinished file: "+CurrentName+" deleted!!!")
                        sleep(1.5)
                        break
                    else:
                        wx.CallAfter(self.actionDetailsTxt.SetLabel,"Finished downloading: "+CurrentName)
                        sleep(1.5)
                else:
                    Timer+=214
                    wx.CallAfter(self.gauge.SetValue,Timer)
                    wx.CallAfter(self.actionDetailsTxt.SetLabel,"File: "+CurrentName+" already exists! Skipping...")
                    sleep(1)
        wx.CallAfter(self.actionDetailsTxt.SetLabel,"Waiting for action")      
        wx.CallAfter(self.gauge.SetValue,0)
        self.stopBtnPressed = False
if __name__=='__main__':
    app = wx.App(redirect=False)
    MainWindow(None)
    app.MainLoop()
