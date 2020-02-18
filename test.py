#!/usr/bin/python
from tkinter           import *
from settings          import *
from frameTools        import MsgInformation
import os

testDat =  dict([('@name', 'My Model (1)'), ('simulator', 'TOUGH2')])
#print(len(list(filter(None, testDat))))
#print(len([i for i in testDat if i]))
#for x in testDat:
if not isinstance(testDat, list):
    numMod = 1
    print('1:', numMod)

testDat = [dict([('@name', 'My Model (1)'), ('simulator', 'TOUGH2')]), 
           dict([('@name', 'My Model (2)'), ('simulator', 'TOUGHREACT')])]
#print(len(list(filter(None, testDat))))
#print(len([i for i in testDat if i]))
if isinstance(testDat, list):
    numMod = len(list(filter(None, testDat)))
    print('2:', numMod)
