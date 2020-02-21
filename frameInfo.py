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
        self.config(
            bd=1, 
            relief=SUNKEN, 
            width=10, 
            height=30, 
            bg=colorCanv, 
            padx=0, 
            pady=5)
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
             padx=5)
         self.pack(side=TOP, fill=BOTH)

class InfoTitleMenu(Frame):
    """Create title and menu at top of Information."""

    def __init__(self, parent=None, titleInfo=[], VarProj=[]):
        Frame.__init__(self, parent)
        self.config(bd=2, relief=FLAT, width=10, height=30)
        self.pack(side=TOP, fill=BOTH)

        self.infoMenu = Menubutton(self, text='View', underline=0, bg=color['tab'])
        self.infoMenu.pack(side=RIGHT, fill=X, padx=10)
        self.file = Menu(self.infoMenu)
        for (items) in VarProj.canvasButtons:
            self.file.add_command(
                label=VarProj.canvasButtons[items]['label'], 
                command=VarProj.canvasButtons[items]['command'],
                state=VarProj.canvasButtonStatus[items].get())
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

    def __init__(self, parent=None, VarProj=[], frmTop=[]):
        Frame.__init__(self, parent)
        self.config(
            bd=1, 
            relief=SUNKEN, 
            width=10, 
            height=30, 
            bg=colorCanv, 
            padx=0, 
            pady=5)
        self.pack(side=RIGHT, fill=BOTH)

        self.canv = Canvas(self, relief=FLAT)

# MBK !!! need to sort out binding of mousewheel and pointer for multiple scrollbars
#       # Will be platform dependent: 
#       self.canv.bind_all("<MouseWheel>", self._on_mousewheel)

        self.canv.config(
            width=infoCanvWidth,
            height=infoCanvHeight,
            scrollregion=canvasScrollRegion,
            highlightthickness=0,
            bg=colorCanv)
        self.makeButtons(VarProj)

        self.sbar = Scrollbar(self)
        self.sbar.config(command=self.canv.yview, width=16)
        self.canv.config(yscrollcommand=self.sbar.set)
        self.sbar.pack(side=RIGHT, fill=Y)
        self.canv.pack(side=LEFT, expand=YES, fill=BOTH)

# MBK !!! need to sort out binding of mousewheel and pointer for multiple scrollbars
#   def _on_mousewheel(self, event):
#      # MBK!!! This command will depend on platform
#      # https://stackoverflow.com/questions/17355902/python-tkinter-binding-mousewheel-to-scrollbar
#      #self.canv.yview_scroll(-1*(event.delta/120), "units") #for Windows
#       self.canv.yview_scroll(-1*(event.delta), "units") #for OSX

    def makeCanvImage(self, imgfile='iHHO_logo_noBackground.png'): 
        self.canv.delete("all")
       #self.thumbs = []
        self.path = os.path.join(dirThumbs, imgfile)
        self.obj = Image.open(self.path)
        self.obj.thumbnail(sizeCanvImage, Image.ANTIALIAS)
        self.img = PhotoImage(self.obj)
        self.canvImage = self.canv.create_image(
                x0_CanvImage,
                y0_CanvImage, 
                anchor = NW, 
                image = self.img)

    def makeCanvText(self):
        self.canv.delete('all')
        self.canvImage = Text(self, relief=FLAT)
        self.canvImage.config(
            relief=FLAT,
            highlightthickness=1,
            bd=1)
 
        self.canvImage.pack(side=LEFT, expand=YES, fill=BOTH)
        path = os.path.join(dirRecent, fileRecent)
        file = path
        self.setText('test', file)
 
        self.canvWindow = self.canv.create_window(
                x0_CanvImage,
                y0_CanvImage,
                width=500,
                height=250,
                anchor=NW,
                window=self.canvImage)

    def setText(self, text='', file=None):
        if file:
            try:
                text = open(file, 'r').read()
                self.canvImage.delete('1.0', END)
                self.canvImage.insert('1.0', text)
                self.canvImage.mark_set(INSERT, '1.0')
                self.canvImage.focus()
            except:
                MsgInformation([], ['Message',
                    'File not found: '+file])                

#   def getText(self):
#       return self.text.get('1.0', 'end-2c')

    # Buttons inside Input frame, at top of canvas
    def makeButtons(self, VarProj):

        frmButtons = Frame(self)
        frmButtons.pack(side=TOP, anchor=N)
        
        self.buttonList = {}
        for (items) in VarProj.canvasButtons:
            self.buttonList[items] = Button(
                frmButtons, 
                text=VarProj.canvasButtons[items]['label'], 
                command=VarProj.canvasButtons[items]['command'],
                state=VarProj.canvasButtonStatus[items].get())
            self.buttonList[items].pack(side=LEFT)

    def onChooseDir(self, VarProj, frmTop):
        """Ask to select directory, load images from directory for viewing.

        Enable the button to call onNext and display next image.
        """

       #self.makeCanvImage()
        self.directory = filedialog.askdirectory()
        if self.directory:
            self.thumbs = []
            for imgfile in os.listdir(self.directory):
                path = os.path.join(self.directory, imgfile)
               #if not imgfile.startswith('.'): #skip .DS_Store file
                if (imgfile.endswith('.png') or imgfile.endswith('.jpg')):
                    obj = Image.open(path)
                    obj.thumbnail(sizeCanvImage, Image.ANTIALIAS)
                    self.thumbs.append(PhotoImage(obj))
            self.thumbNumber = 0
            if len(self.thumbs)>0:
                self.makeCanvImage()
                self.canv.itemconfig(
                    self.canvImage, 
                    image=self.thumbs[self.thumbNumber])

                # Set button inside and menu entry on top of canvas
                self.buttonList['next image']['state']=ACTIVE
                frmTop.file.entryconfigure(
                    VarProj.canvasButtons['next image']['label'], 
                    state='active')

            else:
                # Set button inside and menu entry on top of canvas
                self.buttonList['next image']['state']='disabled'
                frmTop.file.entryconfigure(
                    VarProj.canvasButtons['next image']['label'],
                    state='disabled')

                MsgInformation([], ['Message', 
                    'No images found in the selected directory'])

    def onClear(self, VarProj, frmTop):
        """Clear canvas."""

        self.canv.delete("all")
        self.buttonList['next image']['state']=DISABLED

        # Set button inside and menu entry on top of canvas
        self.buttonList['next image']['state']='disabled'
        frmTop.file.entryconfigure(
            VarProj.canvasButtons['next image']['label'],
            state='disabled')

    def onNext(self):
        """If images were loaded from directory, load next one in list."""

        if not self.thumbs==[]:
            self.thumbNumber += 1
            if self.thumbNumber == len(self.thumbs):
                self.thumbNumber = 0
            self.canv.itemconfig(
                self.canvImage, 
                image = self.thumbs[self.thumbNumber])

    def onChoose(self, VarProj, frmTop):
        """Ask to select image file and display it."""

        self.initialOpenDirectory = initialOpenDirectory
        self.file = filedialog.askopenfilename(
            initialdir = self.initialOpenDirectory, 
            title = "Select image",
            filetypes = (("xml files","*.xml"),("jpeg files","*.jpg")))
        if self.file:
            self.makeCanvImage()
            obj = Image.open(self.file)
            obj.thumbnail(sizeCanvImage, Image.ANTIALIAS)
            self.img = PhotoImage(obj)
            self.canv.itemconfig(self.canvImage, image = self.img)

            # Set button inside and menu entry on top of canvas
            self.buttonList['next image']['state']='disabled'
            frmTop.file.entryconfigure(
                VarProj.canvasButtons['next image']['label'],
                state='disabled')
 
    def onChooseFile(self, VarProj, frmTop, fileName):
        """Ask to select text file and display it."""

        if fileName == []:
            self.initialOpenDirectory = initialOpenDirectory
            self.file = filedialog.askopenfilename(
                initialdir = VarProj.projVar['directory']['current'][0].get(),
                title = "Select image",
               #filetypes = (("xml files","*.xml"),("jpeg files","*.jpg")))
                filetypes = (("xml files","*.xml"),("all files","*.*")))
        else:
            self.file = fileName

        if self.file:
            self.makeCanvText()
            self.setText('test', self.file)

            # Set button inside and menu entry on top of canvas
            self.buttonList['next image']['state']='disabled'
            frmTop.file.entryconfigure(
                VarProj.canvasButtons['next image']['label'],
                state='disabled')

    def showAllEvents(self, event):
        print(event)
        for attr in dir(event):
            if not attr.startswith('__'):
                print(attr, '=', getattr(event,attr))

    def onDoubleClick(self, event):
        print(event.x, event.y)   #view area coords
        print(self.canvas.canvasx(event.x), self.canvas.canvasy(event.y))  #canvas coords



