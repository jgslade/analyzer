import pwd
import os
import sqlite3 as lite
import subprocess
import time

#variables
program="plasmashell"
previousProgram="none"
programList=[]
setMouse=""
mouseDefault="F3"
newMode=[]
newColor=[]
newBut1=[]
newBut2=[]
newG4=[]
newG5=[]
newG6=[]
newG7=[]
newG8=[]
newG9=[]
specialCharacters=["—","-"]
trunc="none"

def getUsername():
    return pwd.getpwuid( os.getuid() )[ 0 ]

#Get the data from database
getList = lite.connect('/home/%s/.config/ratslap/ratslap_config.db'%(getUsername()))
with getList:
    getList.row_factory = lite.Row
    listCursor = getList.cursor()
    listCursor.execute("select * from config")
    appList = listCursor.fetchall()
    for app in appList:
        programList.append(app['Application'])
        newMode.append(app['Mode'])
        newColor.append(app['Color'])
        newG4.append(app['G4'])
        newG5.append(app['G5'])
        newG6.append(app['G6'])
        newG7.append(app['G7'])
        newG8.append(app['G8'])
        newG9.append(app['G9'])
print(programList)
print(newMode)


#Returns the active window name
def activeWindow(process):
    window = subprocess.Popen(['xdotool', 'getactiveWindow', 'getwindowname'],stdout=subprocess.PIPE,universal_newlines=True)

    (windowName, err) = window.communicate()
    return windowName

def formatName(appName):
    for i in range(len(specialCharacters)):
        if specialCharacters[0] in activeWindow(program):
            reverse=activeWindow(program)[::-1]
            trunc=(reverse.split(specialCharacters[0])[0]).strip()[::-1]
        elif specialCharacters[1] in activeWindow(program):
            reverse=activeWindow(program)[::-1]
            trunc=(reverse.split(specialCharacters[1])[0]).strip()[::-1]
        else:
            trunc=activeWindow(program).strip()
            break
    return(trunc)


#Checks for changes to the active window
while True:
    time.sleep(.5)
    for i in range(len(programList)):
        if (formatName(program)==previousProgram):
            continue
        elif (programList[1] == formatName(program)):
            print("Setting mouse to %s."%(newMode[1]))
            print(formatName(program))
            subprocess.Popen(['ratslap', '--select', newMode[1]])
            previousProgram=formatName(program)
        elif (programList[2] == formatName(program)):
            print("Setting mouse to %s."%(newMode[2]))
            print(formatName(program))
            subprocess.Popen(['ratslap', '--select', newMode[2]])
            previousProgram=formatName(program)
        else:
            print("Setting mouse to %s."%(mouseDefault))
            print(formatName(program))
            subprocess.Popen(['ratslap', '--select', newMode[0]])
            previousProgram=formatName(program)