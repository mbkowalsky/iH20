#!/usr/bin/python
from tkinter import *
from settings import *
from frameTools import callScript

#**************************************
# Extra stuff to remember
#**************************************

class FrameExtra(Frame):
    def __init__(self, parent=None, **options):
        Frame.__init__(self, parent=None, **options)
        self.config(bd=2, relief=RAISED)
        self.pack(expand=YES, fill=BOTH, side=LEFT)

class FrameExtraMenu(Frame):
    def __init__(self, parent=None, **options):
#       Menubutton.__init__(self, parent=None, **options)
        Menubutton.__init__(self, text='Choose option:')

#       obj = Menubutton(self, text='Choose option:')
        options = Menu(self)
        options.add_command(label='Run viewer', command=callScript)
        options.add_command(label='Option 1', command=self.quit)
        options.add_command(label='Option 2', command=self.quit)
        options.add_command(label='Option 3', command=self.quit)
        self.config(bd=4, relief=RAISED, menu=options)
        self.pack(side=LEFT, anchor=NW)

class FrameExtraItems(Frame):
    def __init__(self, parent=None, **options):
        Frame.__init__(self, parent=None, **options)
        self.config(bd=2, relief=RAISED)
        self.pack(expand=YES, fill=BOTH)
        var1 = StringVar()
        var2 = StringVar()
        opt1 = OptionMenu(self, var1, 'Parameter 1', 'Parameter 2', 'Parameter 3')
        opt2 = OptionMenu(self, var2, 'Observation 1', 'Observation 2', 'Observation 3')
        opt1.pack(fill=X,side=TOP)
        opt2.pack(fill=X,side=TOP)
        var1.set('Parameter 1')
        var2.set('Observation 1')

        def state(): print(var1.get(), var2.get())
        Button(self, command=state, text='State').pack(side=LEFT)
        Button(self, command=state, text='Quit').pack(side=RIGHT)

if __name__ == "__main__": FrameExtra().mainloop()
