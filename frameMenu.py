#!/usr/bin/python
from tkinter            import *
from tkinter.messagebox import *
from settings           import *
from frameTools         import msgNotImplemented
from PIL                import Image
from PIL.ImageTk        import PhotoImage
from frameInput         import openProject
from processXML         import readXML
import os, sys, math

class MainMenu(Frame):
    """Creates main menu, and tool bar.
    """

    def __init__(self, parent=None, menuOptions=[], VarProj=[], VarMod=[]):
        Frame.__init__(self, parent)
        self.pack(expand=YES, fill=BOTH)
        self.master.title('iH2O')
        self.master.iconbitmap(bitmap='gray50') 
        self.menubar = Menu(self.master)
        self.master.config(menu=self.menubar)
    
        for (name, key, items) in menuOptions:
            pulldown = Menu(self.menubar)
            for (namesub, keysub, itemssub) in items:
                pulldown.add_command(label=namesub, command=itemssub)
            self.menubar.add_cascade(
                label=name, 
                underline=key, 
                menu=pulldown)

        self.toolbar = Frame(self, relief=GROOVE, bd=1)
        self.toolbar.pack(side=BOTTOM, fill=X, pady=0)
        self.toolbarOptions = [

            ('Open', 0, lambda:self.onClickOpen(VarProj, VarMod)),
            ('Open test', 0, lambda:self.onClickOpenTest(VarProj, VarMod)),
            ('Quit', 0, self.quit)
            ]
        
        self.toolbarButtons = []
        for (name, key, item) in self.toolbarOptions:
            toolbarButton = Button(
                self.toolbar,
                text=name,
                command=item)
            toolbarButton.pack(side=LEFT, expand=NO, fill=NONE)
            self.toolbarButtons.append(toolbarButton)

        editMode = [
            'Normal mode',
            'Debug mode'
            ]
 
        self.simulatorMenu = OptionMenu(self.toolbar, VarProj.editMode, *editMode,
            command=self.setEditMode(VarProj.editMode, VarProj, VarMod))
        self.simulatorMenu.config(
            justify=LEFT,
            underline=0)
        self.simulatorMenu.pack(side=LEFT, fill=X, padx=10, pady=5)

        # MBK!!!: Toolbar button/images need functions/commands and correct images
        tst=self.imageMenu() 
        for obj in self.photoObjs:
            bt = Button(self.toolbar, image=obj, command=msgNotImplemented)
            bt.pack(side=RIGHT, expand=NO, fill=NONE)

    def setEditMode(self, editMode, VarProj, VarMod):
        if editMode.get() == 'Debug mode':
            VarProj.editButtonStatus['project'].set('active')
            VarProj.editButtonStatus['models'].set('active')
            VarProj.editButtonStatus['computations'].set('active')

    def onClickOpen(self, VarProj, VarMod):
       #openProject(VarProj,[])
        openProject(VarProj, VarMod, [])

    def onClickOpenTest(self, VarProj, VarMod):
        path = os.path.join(dirRecent, fileRecent)
        openProject(VarProj, VarMod, 'Open test')

    # MBK!!!: Toolbar images not doing anything
    def imageMenu(self):
        self.size = sizeThumbs
        thumbs = []
        self.photoObjs = []
        if os.path.exists(dirThumbs):
            for imgfile in os.listdir(dirThumbs):
                path = os.path.join(dirThumbs, imgfile)
                if not imgfile.startswith('.'): #skip .DS_Store file 
                    obj = Image.open(path)
                    obj.thumbnail((self.size[0], self.size[1]), Image.ANTIALIAS)
                    thumbs.append((imgfile,obj))
            for (imgfile, obj) in thumbs:
                img = PhotoImage(obj)
                self.photoObjs.append(img)
        else:
            showerror('Error', 'Directory does not exist!\n'+dirThumbs)
       
def help():
    msgNotImplemented()

def support():
    msgNotImplemented()

if __name__ == '__main__': MainMenu().mainloop()

