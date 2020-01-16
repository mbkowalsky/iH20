#!/usr/bin/python
from tkinter            import *
from tkinter.messagebox import *
from settings           import *
import os

#**************************************
# Tools for frames
#**************************************

def askDirectory():
    file = filedialog.askdirectory()
    return file

def msgUnavailable():
    showwarning('Message', 'Option not available')

def msgNotImplemented():
    showwarning('Message', 'Option not implemented')

class MsgInformation(Frame):
    """Create message box with title and message as input."""

    def __init__(self, parent=None, msg=[]):
        Frame.__init__(self, parent)
        if not msg==[]:
            showinfo(msg[0], msg[1])

class MsgNotImplemented(Frame):
    def __init__(self, parent=None, msg=[]):
        Frame.__init__(self, parent)
        if not msg==[]:
            showwarning(msg[0], msg[1])
        else:
            showwarning('Message', 'Option not implemented')
   
def callScript():
    #from viewer_thumbs import viewer
    #main, save = viewer(kind=Toplevel)
    #main.mainloop()
    #showerror('Not implemented','Not yet available')
    msgNotImplemented()

class FrameSeparator(Frame):
   #def __init__(self, parent=None, sideSpec=BOTTOM):
    def __init__(self, parent=None, sideSpec=BOTTOM, colorSpec='white', padySpec=0):
        Frame.__init__(self, parent)
        self.config(bd=2, relief=FLAT, height=2, bg=colorSpec)
       #self.config(bd=2, relief=GROOVE, height=2, bg=colorSpec)
        self.pack(side=sideSpec, fill=BOTH, pady=padySpec)

class FrameContainer(Frame):
    """ Container for Information sub-frames """
    def __init__(self, parent=None, **options):
        Frame.__init__(self, parent, **options)
       #self.config(bd=2, relief=FLAT, bg=colorContainer)
        self.config(bd=2, relief=FLAT, bg=colorContainer, height=800, width=1000)
        self.pack(expand=YES, fill=BOTH, side=RIGHT)
        self.pack_propagate(0) #Turn off geometry propagation for frame to keep window from growing/shrinking

class FrameLabel(Frame):
    def __init__(self, frm=[], name=[]):
        self.msg = Label(
            frm,
            text=name,
            anchor=NW,
            bg=color['tab'],
            fg=tabTitleColor,
            font=('Helvetica', 18, 'bold'))
        self.msg.config(width=20, height=1, padx=10, pady=5)
        self.msg.pack(side=TOP, fill=X)

def clearFrame(frm):
    frm.destroy()

def selectImage():
    file = 'ESDLogo.gif'
    self.imgfile.set(file)

