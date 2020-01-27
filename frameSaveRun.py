#!/usr/bin/python
from tkinter           import *
from settings          import *
from frameTools        import MsgInformation
import os

#**************************************
# Save and Run buttons
#**************************************

class FrameSaveRun(Frame):
   #def __init__(self, parent=None, **options):
    def __init__(self, parent=None, VarProj=[], VarMod=[]):
        Frame.__init__(self, parent=None)
        self.config(bd=2, relief=FLAT)
        self.pack(expand=NO, fill=X, side=BOTTOM)
        buttonSave = Button(
            self, 
            text='Save', 
            command=lambda:onClickSave(VarProj, VarMod))
        buttonSave.config(width=21, padx=0, pady=3)
        buttonSave.pack(side=LEFT, fill=X)
        buttonRun = Button(
            self, 
            text='Run', 
            command=lambda:onClickRun(VarProj, VarMod))
        buttonRun.config(width=21, padx=0, pady=3)
        buttonRun.pack(side=LEFT, fill=X)

def onClickSave(VarProj, VarMod):
    """Save variables by copying from 'current' to 'previous'."""

    print('Before saving:')
    for item in VarProj.compVar:
        print(item, 'Value of "previous":', VarProj.compVar[item]['previous'].get())
        print(item, 'Value of "current":', VarProj.compVar[item]['current'].get())

    for name in VarProj.compVar:
        VarProj.compVar[name]['previous'].set(
            VarProj.compVar[name]['current'].get())

    print('After saving:')
    for item in VarProj.compVar:
        print(item, 'Value of "previous":', VarProj.compVar[item]['previous'].get())
        print(item, 'Value of "current":', VarProj.compVar[item]['current'].get())

def onClickRun(VarProj, VarMod):
    """Run code."""

    # Create iTOUGH2 input file here?

    os.system("itough2")    

if __name__ == "__main__": FrameSaveRun().mainloop()
