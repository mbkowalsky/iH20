#!/usr/bin/python
from tkinter           import *
from settings          import *
from frameTools        import MsgInformation

#**************************************
# Save and Run buttons
#**************************************

class FrameSaveRun(Frame):
    def __init__(self, parent=None, **options):
        Frame.__init__(self, parent=None, **options)
        self.config(bd=2, relief=FLAT)
        self.pack(expand=NO, fill=X, side=BOTTOM)
        buttonSave = Button(
            self, 
            text='Save', 
            command=lambda:MsgInformation([], ['Message', 'Not available']))
        buttonSave.config(width=21, padx=0, pady=3)
        buttonSave.pack(side=LEFT, fill=X)
        buttonRun = Button(
            self, 
            text='Run', 
            command=lambda:MsgInformation([], ['Message', 'Not available']))
        buttonRun.config(width=21, padx=0, pady=3)
        buttonRun.pack(side=LEFT, fill=X)

if __name__ == "__main__": FrameSaveRun().mainloop()
