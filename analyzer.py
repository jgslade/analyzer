#!/usr/bin/env python

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
currentMode="F3"
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
for i in range(len(programList)):
    print ("%s: %s; %s"%(programList[i], newMode[i], newColor[i]))


#Returns the active window name
def activeWindow(process):
    window = subprocess.Popen(['xdotool', 'getactiveWindow', 'getwindowname'],stdout=subprocess.PIPE,universal_newlines=True)

    (windowName, err) = window.communicate()
    return windowName

#formats the active window name for comparison
def formatName(appName):
    for i in range(len(specialCharacters)):
        reverse=activeWindow(program)[::-1]
        trunc=(reverse.split(specialCharacters[i])[0]).strip()[::-1]
    return(trunc)


#Checks for changes to the active window
while True:
    time.sleep(.5)
    for i in range(len(programList)):
        if (formatName(program)==previousProgram):
            continue
        elif (formatName(program) in programList):
            pos=programList.index(formatName(program))
            print("Setting mouse to %s."%(newMode[pos]))
            print(formatName(program))
            subprocess.Popen(['ratslap', '--modify', newMode[pos], '-c', newColor[pos], '-4', newG4[pos], '-5', newG5[pos], '-6', newG6[pos], '-7', newG7[pos], '-8', newG8[pos], '-9', newG9[pos],'--select', newMode[pos]])
            previousProgram=formatName(program)
            currentMode=newMode[pos]
            print(currentMode)
        else:
            if (currentMode == mouseDefault):
                previousProgram=formatName(program)
                continue
            else:
                print("Mouse currently set to: %s."%(currentMode))
                print("Setting mouse to %s."%(mouseDefault))
                print(formatName(program))
                subprocess.Popen(['ratslap', '--select', newMode[0]])
                previousProgram=formatName(program)
                currentMode=mouseDefault
