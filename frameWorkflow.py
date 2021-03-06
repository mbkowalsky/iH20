#!/usr/bin/python
from tkinter           import *
from settings          import *
from frameTools        import FrameSeparator
from PIL               import Image
from PIL.ImageTk       import PhotoImage
import os

class WorkflowTab(Frame):
    def __init__(self, parent=None, name=[], key=[], items=[], 
                 editState='disabled', status=[]):
        FrameSeparator([], TOP)
        self.frmBox = Frame()
        self.frmBox.pack_propagate(0)
        self.frmBox.pack(expand=YES, fill=BOTH, side=TOP)
        self.frmBox.config(bd=2, relief=FLAT, bg=colorWorkBG)

        self.frmBoxInner = Frame(self.frmBox)
        self.frmBoxInner.pack(side=TOP, fill=X, expand=YES)
        self.frmBoxInner.config(bg=colorWorkflow)
           
        self.title = Label(self.frmBoxInner,
            text=name,
            anchor=W,
            bg=colorTitleTab,
            fg=tabTitleColor,
            padx=5,
            font=('Helvetica', 18, 'bold'))
        self.title.pack(side=LEFT)
        self.title.config(width=20)
           
        self.editButton = Button(self.frmBoxInner,
            text='Edit',
            command=key,
            underline=0,
            state=editState.get(),
            fg=colorWorkLabel,
            bg=colorWorkflow)
        self.editButton.pack(side=RIGHT)

# MBK!!! Tried to do checks with different colors, including
# using images, image= plus selectimage= plus indicatoron=False
# but not working
#       path = os.path.join(dirThumbs, 'checkbox.png')
#       obj = Image.open(path)
#       obj.thumbnail(sizeCheckBox, Image.ANTIALIAS)
#      #checkBoxOn = PhotoImage(obj)
#       checkBoxOn = PhotoImage(file=path)
#       path = os.path.join(dirThumbs, 'checkbox.red.png')
#       obj = Image.open(path)
#       obj.thumbnail(sizeCheckBox, Image.ANTIALIAS)
#       checkBoxOff = PhotoImage(file=path)

#       self.checkBox = Checkbutton(self.frmBoxInner,
#           variable=status,
#           underline=0,
#           fg=colorWorkLabel,
#           bg=colorWorkflow,
#           width=2,
#           indicatoron=False,
#           image=checkBoxOff,
#           selectimage=checkBoxOn,
#           state=DISABLED, #Not using for input, only to display state
#           offvalue=0,
#           onvalue=1)
#       self.checkBox.pack(side=RIGHT)

        self.checkBox = Checkbutton(self.frmBoxInner,
            variable=status,
            underline=0,
            fg=colorWorkLabel,
            bg=colorWorkflow,
            width=2,
            state=DISABLED, #Not using for input, only to display state
            offvalue=0,
            onvalue=1)
        self.checkBox.pack(side=RIGHT)

        self.rows=[]
        self.colNames=[]
        self.colValues=[]
        for i in range(len(items)):
            subitems = items[i]
            row = Frame()
            row.pack(expand=YES, fill=BOTH, side=TOP)
            row.pack_propagate(0)
            row.config(bd=2, relief=FLAT, bg=colorTabDefault)
            self.rows.append(row)

            colName = Label(self.rows[i],
                text=subitems[0],
                justify=RIGHT,
                anchor=NE,
                padx=5,
                pady=0,
                fg=colorWorkLabel,
                font=('Helvetica', sizeWorkLabel))
            colName.pack(expand=YES, fill=NONE, side=LEFT)
            colName.config(
                relief=FLAT, 
                width=12, 
                height=0, 
                bg=colorWorkBG, 
                anchor=NE)
            self.colNames.append(colName)

            colValue = Label(self.rows[i],
                textvariable=subitems[1],
                justify=LEFT,
                anchor=NW,
                padx=5,
                pady=0,
                wraplength=wrapLengthWF,
                fg=colorWorkEntry,
                font=('Helvetica', sizeWorkEntry))
            colValue.pack(expand=YES, fill=X, side=LEFT)
            colValue.config(
                relief=FLAT, 
                width=30, 
                height=0, 
                bg=colorWorkBG, 
                anchor=NW)
            self.colValues.append(colValue)


if __name__ == "__main__": FrameWorkflowTabs().mainloop()
