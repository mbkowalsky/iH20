#!/usr/bin/python
from tkinter           import *
from settings          import *

#**************************************
# Top Toolbar frame
#**************************************
class FrameToolbar(Frame):
    def __init__(self, parent=None, **options):
        Frame.__init__(self, parent, **options)
        self.config(bd=2, relief=FLAT, bg=colorToolbar)
        self.pack(expand=YES, fill=X, side=TOP)
        obj = Label(self, text='TOOLBAR')
        obj.config(width=100, bg=colorToolbar)
        obj.pack()

if __name__ == "__main__": FrameToolbar().mainloop()
