#!/usr/bin/python
from tkinter           import *
from settings          import *
from frameTools        import MsgInformation
import os

#**************************************
# Save and Run buttons
#**************************************

class FrameSaveRun(Frame):
    def __init__(self, parent=None, VarProj=[]):
        Frame.__init__(self, parent=None)
        self.config(bd=2, relief=FLAT)
        self.pack(expand=NO, fill=X, side=BOTTOM)
        buttonSave = Button(
            self, 
            text='Save', 
            command=lambda:onClickSave(VarProj)
        )
        buttonSave.config(width=21, padx=0, pady=3)
        buttonSave.pack(side=LEFT, fill=X)
        buttonRun = Button(
            self, 
            text='Run', 
            command=lambda:onClickRun(VarProj)
        )
        buttonRun.config(width=21, padx=0, pady=3)
        buttonRun.pack(side=LEFT, fill=X)

def onClickSave(VarProj):
    """Save variables by copying from 'current' to 'previous'."""

#   print('Before saving:')
#   for item in VarProj.compVar:
#       print(item, 'Value of "previous":', VarProj.compVar[item]['previous'].get())
#       print(item, 'Value of "current":', VarProj.compVar[item]['current'].get())

#   for name in VarProj.compVar:
#       VarProj.compVar[name]['previous'].set(
#           VarProj.compVar[name]['current'].get())
#   for name in VarProj.modelVar:
#       for model in VarProj.modelVar[name]['previous']:
#          #VarProj.compVar[name]['previous'][model].set(
#          #VarProj.compVar[name]['current'][model].get())
#           print(model.get())
#           model.set(model.get())
#           print('After Saving:', model.get())
#
#   print('After saving:')
#   for item in VarProj.compVar:
#       print(item, 'Value of "previous":', VarProj.compVar[item]['previous'].get())
#       print(item, 'Value of "current":', VarProj.compVar[item]['current'].get())

def onClickRun(VarProj):
    """Run code."""

    # Create iTOUGH2 input file here?

#   os.system("itough2")    
#   print('Save:', VarProj)
    redirectedGuiShellCmd('itough2')

# Experimenting with technique from Lutz for redirecting output to GUI:
class GuiOutput:
   #font = ('courier', 9, 'normal')
    def __init__(self, parent=None):
        self.text = None
        if parent: self.popupnow(parent)

    def popupnow(self, parent=None):
        if self.text: return
        self.text = ScrollText(parent or Toplevel())
        self.text.pack()

    def write(self, text):
        self.popupnow()
        self.text.text.insert(END, str(text))
        self.text.text.see(END)
        self.text.text.update()

    def writelines(self, lines):
        for line in lines: self.write(line)

class ScrollText(Frame):
    def __init__(self, parent=None, text='', file=None):
        Frame.__init__(self, parent)
        self.pack(expand=YES, fill=BOTH)
        self.makeWidgets()
        self.setText(text, file)

    def makeWidgets(self):
        sbar = Scrollbar(self)
        text = Text(self, relief=SUNKEN)
        sbar.config(command=text.yview)
        text.config(yscrollcommand=sbar.set)
        sbar.pack(side=RIGHT, fill=Y)
        text.pack(side=LEFT, expand=YES, fill=BOTH)
        self.text = text

    def setText(self, text='', file=None):
        if file:
            text = open(file, 'r').read()
        self.text.delete('1.0', END)
        self.text.insert('1.0', text)
        self.text.mark_set(INSERT, '1.0')
        self.text.focus()

def redirectedGuiShellCmd(command):
    import os
    input = os.popen(command, 'r')
    output = GuiOutput()
    def reader(input, output):
        while True:
            line = input.readline()
            if not line: break
            output.write(line)
    reader(input, output)

if __name__ == "__main__": FrameSaveRun().mainloop()
