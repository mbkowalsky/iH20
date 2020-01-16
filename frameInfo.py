#!/usr/bin/python
from tkinter           import *
from settings          import *
from frameTools        import FrameSeparator
from frameTools        import MsgNotImplemented
from frameTools        import MsgInformation
from processXML        import readXML
from frameSaveRun      import FrameSaveRun
from PIL               import Image
from PIL.ImageTk       import PhotoImage
import os

class InfoSummary(Frame):
    """Display summary entries in Information."""

    def __init__(self, parent=None, datInfoSummary=[]):

        Frame.__init__(self, parent)
        self.config(bd=1, relief=SUNKEN, width=10, height=30, bg=colorCanv, padx=0, pady=5)
        self.pack(side=RIGHT, fill=BOTH)

        self.rows=[]
        self.colNames=[]
        self.colValues=[]
        self.frames=[]
        for items in datInfoSummary:
            frame = Frame(self)
            frame.config(bd=2, relief=FLAT, bg=color['tab'])
            frame.pack(expand=YES, fill=BOTH, side=TOP)
            self.frames.append(frame)

            row = Frame(frame)
            row.config(bd=2, relief=FLAT, bg=color['tab'])
            row.pack(expand=YES, fill=BOTH, side=TOP)
            self.rows.append(row)

            colName = Label(
                row,
                text=items[0],
                justify=RIGHT,
                padx=5,
                pady=0,
                bg=color['tab'],
                fg=colorInfo,
                wraplength=100,
                font=('Helvetica', sizeInfoType))
            colName.pack(expand=YES, fill=NONE, side=LEFT)
            colName.config(relief=FLAT, width=12, height=2, anchor=NE)
            self.colNames.append(colName)

            colValue = Label(
                row,
                textvariable=items[1],
                justify=LEFT,
                anchor=NW,
                padx=5,
                pady=0,
                bg=color['tab'],
                fg=colorInfoEntry,
                wraplength=wrapLengthInfo,
                font=('Helvetica', sizeInfoEntry))
            colValue.pack(expand=YES, fill=X, side=LEFT)
            colValue.config(relief=FLAT, width=100, height=2, anchor=NW)
            self.colValues.append(colValue)

class InfoSubFrame(Frame):
    """Create sub-frame for InfoSummary and InfoCanvas."""

    def __init__(self, parent=None, **options):
         Frame.__init__(self, parent, **options)
         self.config(
             bd=0, 
             relief=FLAT, 
             width=10, 
             height=30, 
             bg=color['tab'], 
             padx=10)
         self.pack(side=TOP, fill=BOTH)

class InfoTitleMenu(Frame):
    """Create title and menu at top of Information."""

    def __init__(self, parent=None, titleInfo=[], datInfoMenu=[]):
        Frame.__init__(self, parent)
        self.config(bd=2, relief=FLAT, width=10, height=30)
        self.pack(side=TOP, fill=BOTH)

        self.infoMenu = Menubutton(self, text='View', underline=0, bg=color['tab'])
        self.infoMenu.pack(side=RIGHT, fill=X, padx=10)
        self.file = Menu(self.infoMenu)
        for (name, key) in datInfoMenu:
            self.file.add_command(label=name, command=key)
        self.infoMenu.config(menu=self.file)

        self.title = Label(
            self,
            text=titleInfo,
            bg=color['tab'],
            fg=tabTitleColor,
            font=('Helvetica', 18, 'bold'),
            anchor=W)
        self.title.pack(side=LEFT, fill=X)
        self.title.config(width=80, height=1, padx=10, pady=5)

class InfoCanvas(Frame):
    """Create main canvas in Information for displaying images."""

    def __init__(self, parent=None, **options):
        Frame.__init__(self, parent, **options)
        self.config(bd=1, relief=SUNKEN, width=10, height=30, bg=colorCanv, padx=0, pady=5)
        self.pack(side=RIGHT, fill=BOTH)

        self.canv = Canvas(self, relief=FLAT)
        self.canv.config(
            width=canvWidth,
            height=canvHeight,
            scrollregion=canvasScrollRegion,
            highlightthickness=0,
            bg=colorCanv)

        self.sbar = Scrollbar(self)
        self.sbar.config(command=self.canv.yview, width=16)
        self.canv.config(yscrollcommand=self.sbar.set)
        self.sbar.pack(side=RIGHT, fill=Y)
        self.canv.pack(side=LEFT, expand=YES, fill=BOTH)

        self.thumbs = []
#       imgfile = 'iH2O_Logo.png'
        imgfile = 'Logo_FinsterleGeoConsulting_NoNG.png'
        path = os.path.join(dirThumbs, imgfile)
        self.obj = Image.open(path)
        self.obj.thumbnail(sizeCanvImage, Image.ANTIALIAS)
        self.img = PhotoImage(self.obj)
        self.canvImage = self.canv.create_image(
            x0_CanvImage,
            y0_CanvImage, 
            anchor = NW, 
            image = self.img)

        self.buttonChoose = Button(self, text="Choose image", command=self.onChoose)
        self.buttonChoose.pack()
        self.buttonDir = Button(self, text="Choose directory", command=self.onList)
        self.buttonDir.pack()
        self.buttonNext = Button(
            self, 
            text="Next image", 
            state=DISABLED,
            command=self.onNext)
        self.buttonNext.pack()

    def onList(self):
        """Ask to select directory, load images from directory for viewing.

        Enable the buttonNext to call onNext and display next image.
        """

        self.directory = filedialog.askdirectory()
        if self.directory:
            self.thumbs = []
            for imgfile in os.listdir(self.directory):
                path = os.path.join(self.directory, imgfile)
               #if not imgfile.startswith('.'): #skip .DS_Store file
                if (imgfile.endswith('.png') or imgfile.endswith('.jpg')):
                    obj = Image.open(path)
                    obj.thumbnail(sizeCanvImage, Image.ANTIALIAS)
               #    self.thumbs.append((imgfile,obj))
                    self.thumbs.append(PhotoImage(obj))
            self.thumbNumber = 0
            if len(self.thumbs)>0:
                self.canv.itemconfig(self.canvImage, image=self.thumbs[self.thumbNumber])
                self.buttonNext['state']=ACTIVE
            else:
                self.buttonNext['state']=DISABLED
        else:
            MsgInformation([], ['Message', 'Cancelled'])

    def onNext(self):
        """If images were loaded from directory, load next one in list."""

        if not self.thumbs==[]:
            self.thumbNumber += 1
            if self.thumbNumber == len(self.thumbs):
                self.thumbNumber = 0
            self.canv.itemconfig(self.canvImage, image = self.thumbs[self.thumbNumber])

    def onChoose(self):
        """Ask to select file and display image."""

        self.initialOpenDirectory = initialOpenDirectory
        self.file = filedialog.askopenfilename(
            initialdir = self.initialOpenDirectory, 
            title = "Select image",
            filetypes = (("xml files","*.xml"),("jpeg files","*.jpg")))
        if self.file:
            obj = Image.open(self.file)
            obj.thumbnail(sizeCanvImage, Image.ANTIALIAS)
            self.img = PhotoImage(obj)
            self.canv.itemconfig(self.canvImage, image = self.img)
        else:
            MsgInformation([], ['Message', 'Cancelled'])

    def showAllEvents(self, event):
        print(event)
        for attr in dir(event):
            if not attr.startswith('__'):
                print(attr, '=', getattr(event,attr))

    def onDoubleClick(self, event):
        print(event.x, event.y)   #view area coords
        print(self.canvas.canvasx(event.x), self.canvas.canvasy(event.y))  #canvas coords




if __name__ == "__main__": 

    from PIL               import Image

#   frm = InfoSummary()
    frm = []
    datInfoMenu = [
       #('View image', lambda:viewImage()),
        ('View image', lambda:openImage(frmGlobalX)),
        ('View file', lambda:msgUnavailable())
        ]
    InfoTitleMenu(frm, 'Project details', datInfoMenu)
   #InfoTitleMenu(frm)
    frmSub = InfoSubFrame(frm)
    InfoCanvas(frmSub)
    mainloop()


