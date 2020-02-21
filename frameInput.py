#!/usr/bin/python
from tkinter           import *
from tkinter           import filedialog
from settings          import *
from frameTools        import MsgNotImplemented
from frameTools        import MsgInformation
from frameTools        import FrameSeparator
from frameTools        import FrameLabel
from processXML        import readXML
from frameInfo         import InfoCanvas
import os

class FrameSubInput(Frame):
    """Create sub-frame for Information."""

    def __init__(self, parent=None, **options):
        Frame.__init__(self, parent, **options)
        self.config(bd=2, relief=FLAT, height=30, bg=color['tab'])
        self.pack(side=TOP, fill=BOTH)

class FrameInput(Frame):
    """Create the User Input frame
    
    Contents will depend on which Workflow tab is selected.
    """

    def __init__(self, parent=None, **options):
        Frame.__init__(self, parent, **options)
        self.config(bd=2, relief=FLAT, height=30, bg=color['tab'])
        self.pack(side=TOP, fill=BOTH)

####################
# Project
####################
class ProjectContainer(Frame):
    def __init__(self, parent=None, nameInput=[], VarProj=[]):
        Frame.__init__(self, parent)
        self.pack(expand=YES, fill=BOTH)

        self.title = FrameLabel(self, nameInput)
        self.frmLabelMenu = Frame(self)
        self.frmLabelMenu.config(
            bd=1, 
            relief=FLAT, 
            height=30, 
            bg=color['tab']
        )
        self.menuOpenProject = Menubutton(
            self.frmLabelMenu, 
            text='Select', 
            underline=0, 
            bg=colorInputBox, 
            width=0)
        self.optionsOpenProject = Menu(self.menuOpenProject)

        self.nameLabel = Label(
            self.frmLabelMenu,
            text='Project option:',
            justify=RIGHT,
            width=40,
            bg='white',
            fg=color['inputEntry'],
            font=('Helvetica', sizeInputEntry, 'bold'))
        self.nameLabel.config(anchor=E)

        self.frmLabelMenu.pack(side=TOP, fill=X, expand=YES)
        self.nameLabel.pack(side=LEFT, expand=NO, fill=X, padx=10)
        self.menuOpenProject.pack(
            side=RIGHT, 
            expand=YES, 
            fill=X, 
            padx=11, 
            pady=5
        )
        self.frmProjectInfo = Frame(self)
        self.frmProjectInfo.pack(side=LEFT, fill=X, expand=YES)
        self.frmProjectInfo.config(
            bd=1, 
            relief=FLAT, 
            height=30, 
            bg=color['tab']
        )
        self.optionsOpenProject.add_command(
            label='New', 
            command=lambda: onClickProjectMenu(
                VarProj, 
                'New', 
                self.frmProjectInfo))
        self.optionsOpenProject.add_command(
            label='Open from file', 
            command=lambda: onClickProjectMenu(
                VarProj, 
                'Open',
                self.frmProjectInfo))
        self.optionsOpenProject.add_command(
            label='Open demo',
            command=lambda: onClickProjectMenu(
                VarProj, 
                'Open demo', 
                self.frmProjectInfo))
        self.menuOpenProject.config(menu=self.optionsOpenProject)

        # Project files already specified, special case in openProject:
        if VarProj.typeProj.get()=='Open demo':
            openProject(VarProj, 'Open demo', self.frmProjectInfo)
     
        # Parameters loaded previously, just populate entries:
        if VarProj.inputLabelsCreated.get() == True:
            makeProjectLabels(VarProj, self.frmProjectInfo)

def onClickProjectMenu(VarProj, typeIn, frmIn):
    VarProj.typeProj.set(typeIn)
    openProject(VarProj, typeIn, frmIn)

def makeProjectLabels(VarProj, frmIn):
# MBK !!! Here
   #print('What key', VarProj.projVar.items())
   #for (tst, (label, value)) in VarProj.projVar.items():
    for (label, value) in VarProj.projVar.items():
       #print('MBK', tst)
        row = Frame(frmIn)
        lab = Label(row,
            text=value['label'],
            justify=RIGHT,
            anchor=E,
            width=40,
            bg='white',
            fg=color['inputEntry'],
            font=('Helvetica', sizeInputEntry, 'bold'))
        row.pack(side=TOP, fill=X)
#       if VarProj.projVar.keys() == 'directory':
        ent = Entry(row, textvariable=value['current'])
#       else:
#           ent = Label(row, textvariable=value['current'])
        ent.pack(side=RIGHT, expand=YES, fill=X, padx=10)
        lab.pack(side=LEFT, expand=NO, fill=X, padx=10)
    VarProj.inputLabelsCreated.set(True)

def openProject(VarProj, fileNameIn, frmIn):

    # Set directory and filename depending on typeProj
    if VarProj.typeProj.get() == 'New':
        dirName = filedialog.askdirectory()
        if dirName:
            VarProj.projVar['directory']['current'][0].set(dirName)
        else:
            VarProj.projVar['directory']['current'][0].set('')
            
    elif VarProj.typeProj.get() == 'Open demo':
        path = os.path.join(dirRecent, fileRecent)
        dirName = os.path.dirname(path)
        fileName = os.path.basename(path)

    elif VarProj.typeProj.get() == 'Open':
        path = filedialog.askopenfilename(
            initialdir = ".",
            title = "Select file",
            filetypes = (("xml files","*.xml"),("jpeg files","*.jpg"))
        ) 
        dirName = os.path.dirname(path)
        fileName = os.path.basename(path)        

    else: 
# MBK!!! will these get used when calling from toolbar
        path = os.path.join(dirRecent, fileRecent)
        dirName = os.path.dirname(path)
        fileName = os.path.basename(path)
        makeProjectLabels(VarProj, frmIn)

    # Read xml file to open project but not if new or editing project
    if (dirName and (VarProj.typeProj.get() in ['Open', 'Open demo'])):
        VarProj.projVar['file-name']['current'][0].set(fileName)
        VarProj.projVar['directory']['current'][0].set(dirName)
        readXML(VarProj)
        # Initial file was read, so change typeProj
        VarProj.typeProj.set('Editing')

    elif dirName and VarProj.typeProj.get() == 'New':
        # Start with default values since new project
        # MBK!!! Add other workflow defaults eventually
        for name in ['file-name', 'project-name']:
            VarProj.projVar[name]['current'][0].set(
            VarProj.projVar[name]['default'])
        for name in VarProj.compVar:
            VarProj.compVar[name]['current'][0].set(
            VarProj.compVar[name]['default'])

    # Populate input entry boxes if not done earlier:
    if (VarProj.inputLabelsCreated.get() == False and dirName):
        makeProjectLabels(VarProj, frmIn)

def addFile(frm, VarProj, i, loadExisting, frmCanvas, frmTop):
    def addRows(fileName):
        row = Frame(frm)
        row.pack(side=TOP, fill=X)
        fileNameLabel = Label(
            row,
            text=fileName,
            justify=LEFT,
            anchor=SW,
            width=20,
            bg='white',
           #fg=color['inputEntry'],
            fg='black',
            font=('Helvetica', sizeInputEntry)
        )
        fileNameLabel.pack(side=LEFT, expand=NO, fill=X, padx=10, pady=0)

        deleteButton = Button(
            row,
            text='Delete',
            command=lambda: onDeleteFile(
                row, 
                fileName,
                VarProj.modelFilesList['input-file'][i]
            ),
            underline=0,
            fg=colorWorkLabel,
            bg=colorWorkflow)
        deleteButton.pack(side=RIGHT, expand=NO, fill=X, padx=10)

        viewButton = Button(
            row,
            text='View',
            command=lambda: onViewFile(
                row,
                VarProj,
                fileName,
                VarProj.modelFilesList['input-file'][i],
                frmCanvas,
                frmTop
            ),
            underline=0,
            fg=colorWorkLabel,
            bg=colorWorkflow)
        viewButton.pack(side=RIGHT, expand=NO, fill=X, padx=10)

    if loadExisting == FALSE:
        newFile = filedialog.askopenfilename(
            initialdir = initialDirAddFile,
            title = "Select",
           # MBK!!! filetypes option not working, all types accepted now
           #     not working properly otherwise 
           #filetypes = (("xml files","*.xml"),("All files","*.*"))
           #filetypes = [("All files", "*.*"), ("xml files", "*.xml")]
        )

        if newFile:
            dirNameX = os.path.dirname(newFile)
            fileNameX = os.path.basename(newFile)

            print('old files:', (VarProj.modelFilesList))
            VarProj.modelFilesList['input-file'][i].append(fileNameX)
            print('new files:', (VarProj.modelFilesList))
            print('new files[i]:', (VarProj.modelFilesList['input-file'][i]))

            # Adding new model entries (not existing ones)
            addRows(VarProj.modelFilesList['input-file'][i][-1])

        else:
            MsgNotImplemented([], ['Message', 'Cancelled'])

    else:
        # Add all model entries
        for fileName in VarProj.modelFilesList['input-file'][i]:
            addRows(fileName)

def onDeleteFile(obj, fileName, name):
    name.remove(fileName)
    obj.destroy()

def onViewFile(obj, VarProj, fileName, name, frmCanvas, frmTop):
    print('MBK', frmCanvas, fileName, name)
    frmCanvas.onChooseFile(VarProj, frmTop, fileName)

####################
# Model Setup
####################

class ModelInputContainer(Frame):
    """Create main container for Model Setup input.

    A sub frame for the title and "Add model" button is inserted
    here too. For now, when "Add model" is clicked, an additional subframe
    appears in this container (via AddModel class)
    """

    def __init__(self, parent=None, nameInput=[], VarProj=[], 
        isNewModel = FALSE, frmCanvas=[], frmTop=[]):
        Frame.__init__(self, parent)
        # Label at top of frame:
        self.title = FrameLabel(self, nameInput)
        self.title.obj.config(pady=0)

        self.config(
            bd=2, 
            relief=FLAT, 
            height=5, 
            bg=color['tab'])
        self.pack(side=TOP, fill=BOTH, padx=0)
 
        frmAddModelList = []
        frmInputList = []

        # Add new model in to scrollable frame
        addModelButton = Button(
            self,
            text='Add model',
            command=lambda:callAddModel(
                VarProj.numMod.get(), 
                TRUE,
                frmAddModelList
            ),
            underline=0,
            bg=color['tab'])
        addModelButton.pack(side=TOP, padx=35, pady=3, anchor=NE)
        
        self.canv = Canvas(self, relief=FLAT)

        self.canv.config(
            width=modelCanvWidth,
            height=modelCanvHeight,
            scrollregion=canvasScrollRegion,
            highlightthickness=0,
            bg=colorCanv)
        self.scrollbar = Scrollbar(self)
        self.frmScroll = Frame(self.canv)

        self.scrollbar.config(command=self.canv.yview, width=16)
        self.canv.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.canv.pack(side=TOP, expand=YES, fill=BOTH)

        self.frmScroll.config(
            bd=2, 
            relief=FLAT, 
            height=30, 
            bg=color['tab'])
        self.frmScroll.pack(fill=X)

        self.canv.create_window(
            0,
            0,
            width=inputCanvWidth,
            height=inputCanvHeight,
            anchor=NW,
            window=self.frmScroll)

# MBK !!! need to sort out binding for multiple scrollbars
#       # Will be platform dependent:
#       self.canv.bind_all("<MouseWheel>", self._on_mousewheel)

        def callAddModel(numExistingModels, isNewModel, frmAddModelList):
            if isNewModel == FALSE:
                # Existing models  
                if numExistingModels > 0:
                    for modelNum in VarProj.modelVar['number']['current']:
                        self.AddModel(
                            self.frmScroll, 
                            VarProj, 
                            modelNum.get(), 
                            isNewModel, 
                            frmCanvas, 
                            frmTop,
                            frmAddModelList,
                            frmInputList
                        )
            else:
                # New model  
                self.AddModel(
                    self.frmScroll,
                    VarProj,
                    numExistingModels,
                    TRUE,
                    frmCanvas,
                    frmTop,
                    frmAddModelList,
                    frmInputList
                )

        callAddModel(VarProj.numMod.get(), FALSE, frmAddModelList)

# MBK !!! need to sort out binding for multiple scrollbars
#   def _on_mousewheel(self, event):
#      # MBK!!! This command will depend on platform
#      # https://stackoverflow.com/questions/17355902/
       #         python-tkinter-binding-mousewheel-to-scrollbar
#      #self.canv.yview_scroll(-1*(event.delta/120), "units") #for Windows
#       self.canv.yview_scroll(-1*(event.delta), "units") #for OSX

    def AddModel(self, frmScroll, VarProj, i, isNewModel, frmCanvas, frmTop, 
                 frmAddModelList, frmInputList):
        """Create subframe in ModelInputContainer for adding a new model.
        """

        self.frmAddModel = Frame(frmScroll)
        self.frmAddModel.config(bd=1, relief=SUNKEN, height=30, bg=color['tab'])
        self.frmAddModel.pack(side=TOP, fill=X, pady=5, padx=10)
        frmAddModelList.append(self.frmAddModel)         
        print('MBK length of frmAddModelList', len(frmAddModelList))
        print('MBK isNewModel?', isNewModel)

        # Append variable list if new model 
        if isNewModel == TRUE:
            for item in VarProj.modelVar:
                if VarProj.modelVar[item]['type']=='StringVar()':
                    newVar = StringVar(value=VarProj.modelVar[item]['default'])
                elif VarProj.modelVar[item]['type']=='IntVar()':
                    newVar = IntVar(value=VarProj.modelVar[item]['default'])
                else:
                    print('MBK !!! appending new variable that is not ready yet')
                VarProj.modelList[item].append(newVar)
            for item in VarProj.modelFiles:
                VarProj.modelFilesList[item].append([])
      
        # Button to delete model:
        self.frmButton = Frame(self.frmAddModel)
        self.frmButton.pack(side=RIGHT, fill=NONE, expand=YES, anchor=NE)
        self.frmButton.config(
            bd=1, 
            relief=FLAT, 
            height=30, 
            bg=color['inputBG'])
        self.deleteButton = Button(
            self.frmButton,
            text='Delete model',
            command=lambda:deleteModel(self),
            underline=0,
            bg=color['tab'])
        self.deleteButton.config(anchor=E)
        self.deleteButton.pack(side=TOP, fill=X, padx=5, pady=5)

        # Frame for model entries:
        frmInput = Frame(self.frmAddModel)
        frmInput.pack(side=LEFT, fill=NONE, expand=YES, anchor=W)
        frmInput.config(bd=1, relief=FLAT, height=30, bg=color['tab'])
        try:
            frmInputList.append(frmInput)
            print('frmInputList.append(frmInput)', i, frmInputList)
        except:
            print('NOPE frmInputList.append(frmInput)', i)
            frmInputList = []

        # Menu for simulator selection:
        row = Frame(frmInputList[i])
        row.config(bg=colorModel)
        label = Label(
            row,
            text=VarProj.modelVar['simulator']['label'],
            justify=RIGHT,
            anchor=E,
            width=20,
            bg=colorModel,
            fg=color['inputEntry'],
            font=('Helvetica', sizeInputEntry, 'bold')
        )
        simOptions = VarProj.modelVar['simulator']['optionList']
        self.simulatorMenu = OptionMenu(
            row, 
            VarProj.modelVar['simulator']['current'][i], 
            *simOptions
        )
        self.simulatorMenu.config(
            justify=LEFT,
            underline=0,
            width=60
        )
        row.pack(side=TOP, fill=X)
        self.simulatorMenu.pack(side=RIGHT, fill=X, padx=10, pady=5)
        label.pack(side=LEFT, expand=NO, fill=X, padx=10)

        # Labels and entries for a model:
        for (key) in VarProj.modelVar:
            if not key == 'simulator':
                row = Frame(frmInputList[i])
                label = Label(
                    row,
                    text=VarProj.modelVar[key]['label'],
                    justify=RIGHT,
                    anchor=E,
                    width=20,
                    bg='white',
                    fg=color['inputEntry'],
                    font=('Helvetica', sizeInputEntry, 'bold'))

                name = VarProj.modelVar[key]['current'][i]
                entry = Entry(
                    row, 
                    textvariable=name,
                    width=60)
                row.pack(side=TOP, fill=X)
                entry.pack(side=RIGHT, expand=YES, fill=X, padx=10)
                label.pack(side=LEFT, expand=NO, fill=X, padx=10)

        # Button for adding new input files:
        self.menuSelectFile = Menubutton(
            self.frmButton, 
            text='Add file',
            underline=0,
            bg=colorInputBox,
            width=0
        )
        self.optionsSelectFile = Menu(self.menuSelectFile)
        print('MBK addFile frmInput', frmInputList[i])
        self.optionsSelectFile.add_command(
            label='Select file', 
            command=lambda:addFile(
               #self.frmInput, 
                frmInputList[i], 
                VarProj, 
                i, 
                FALSE,
                frmCanvas,
                frmTop
            )
        )
        self.optionsSelectFile.add_command(
            label='Select [...]', 
            command=MsgNotImplemented)
        self.menuSelectFile.config(menu=self.optionsSelectFile)
        self.menuSelectFile.pack(
            side=TOP, 
            expand=YES, 
            fill=X, 
            padx=10, 
            pady=5
        )
        self.nameLabel = Label(
            frmInputList[i],
            text=VarProj.modelFiles['input-file']['label'],
            justify=RIGHT,
            anchor=NE,
            width=20,
            bg='white',
            fg=color['inputEntry'],
            font=('Helvetica', sizeInputEntry, 'bold')
        )
        self.nameLabel.config(anchor=NE)
        self.nameLabel.pack(side=LEFT, expand=NO, fill=Y, pady=5, padx=10)

        # Display existing input file names
        loadExisting = TRUE
        addFile(frmInputList[i], VarProj, i, loadExisting, frmCanvas, frmTop)

        if isNewModel == TRUE:
            VarProj.modelVar['number']['current'][i].set(
                VarProj.numMod.get()
            )
            VarProj.numMod.set(VarProj.numMod.get()+1)

        def deleteModel(self):

            # Remove model from variables
            MBKprint = FALSE
            tst=i
            if MBKprint:
                for hey in VarProj.modelList['number']:
                     print('Hey', hey.get())
                for hey in VarProj.modelList['@name']:
                     print('Hey name', hey.get())
                MBKprint = FALSE
            for (key, items) in VarProj.modelList.items():
                print('Printing key in VarProj.modelList.items', key)
                for item in items:
                    print('Printing item', item.get())
                del VarProj.modelList[key][tst]

            VarProj.numMod.set(VarProj.numMod.get()-1)
            test = VarProj.numMod.get()

            count = 0
            for num in VarProj.modelVar['number']['current']:
                if num.get() >= tst:
                    num.set(num.get()-1)
                count += 1

            # Remove model input files from variables
            for (key, items) in VarProj.modelFilesList.items():
                del VarProj.modelFilesList[key][tst]

            # Remove models from canvas before re-generating existing ones
            for num in frmAddModelList:
                num.destroy()

            # Existing models
            isNewModel=FALSE 
           #if VarProj.numMod.get() >= 0:
            if VarProj.numMod.get() > 0:
                for modelNum in VarProj.modelVar['number']['current']:
                    self.AddModel(
                        self.frmScroll,
                        VarProj,
                        modelNum.get(),
                        isNewModel,
                        frmCanvas,
                        frmTop,
                        frmAddModelList
                        )


####################
# Computations
####################
class CompInputContainer(Frame):
    """Create main container for Computations input.

    A sub frame...
    """

    def __init__(self, parent=None, nameInput=[], VarProj=[], 
                 isNewModel = FALSE):
        Frame.__init__(self, parent)
        self.config(bd=2, relief=FLAT, height=30, bg=color['tab'])
        self.pack(side=TOP, fill=BOTH)

        self.title = FrameLabel(self, nameInput)

        self.frmTop = Frame(self)
        self.frmTop.pack(
            side=TOP, 
            fill=NONE, 
            expand=YES, 
            anchor=W, 
            padx=10
        )
        self.frmTop.config(bd=2, relief=FLAT, height=30, bg=color['tab'])

        row = Frame(self.frmTop)
        row.config(bg=colorModel)
        label = Label(
            row,
            text=VarProj.compVar['application-mode']['label'],
            justify=RIGHT,
            anchor=E,
            width=20,
            bg=colorModel,
            fg=color['inputEntry'],
            font=('Helvetica', sizeInputEntry, 'bold')
        )

        compModeOptions = VarProj.compVar['application-mode']['optionList']
        if VarProj.compVar['application-mode']['current'][0].get()=='':
            for name in VarProj.compVar:
                VarProj.compVar[name]['current'][0].set(
                VarProj.compVar[name]['default'])
        self.simulatorMenu = OptionMenu(row, 
            VarProj.compVar['application-mode']['current'][0], 
            *compModeOptions,
            command=self.makeCompInput(
                VarProj.compVar['application-mode']['current'][0], 
                VarProj
            )
        )
        self.simulatorMenu.config(
            justify=LEFT,
            underline=0,
            width=80)

        row.pack(side=TOP, fill=X)
        self.simulatorMenu.pack(side=RIGHT, fill=X, padx=10, pady=5)
        label.pack(side=LEFT, expand=NO, fill=X, padx=10)

    def makeCompInput(self, selectedMode, VarProj):
        modeInput(self, VarProj)

class modeInput(Frame):
    """Create subframe in CompInputContainer for selected application mode.
    """

    def __init__(self, parent=None, VarProj=[]):
        # Create frame into which model frames will be placed:
        Frame.__init__(self, parent)
        self.config(bd=1, relief=SUNKEN, height=30, bg=color['tab'])
        self.pack(side=TOP, fill=X, pady=5, padx=10)
      
        # Create frame to enter specs for selected application mode 
        self.frmInput = Frame(self)
        self.frmInput.pack(side=LEFT, fill=NONE, expand=YES, anchor=W)
        self.frmInput.config(bd=1, relief=FLAT, height=30, bg=color['tab'])

        self.frmButton = Frame(self)
        self.frmButton.pack(side=RIGHT, fill=NONE, expand=YES, anchor=NE)
        self.frmButton.config(
            bd=1, 
            relief=FLAT, 
            height=30, 
            bg=color['inputBG']
        )
        self.deleteButton = Button(
            self.frmButton,
            text='Reset',
            command=lambda:MsgInformation(
                [], 
                ['Message', 'Not available']
            ),
            underline=0,
            bg=color['tab']
        )
        self.deleteButton.config(anchor=E)
        self.deleteButton.pack(side=TOP, fill=X, padx=5, pady=5)

        # Add labels and entries for a model:
        for (label, value) in VarProj.compVar.items():
            if not label == 'application-mode' and value['current'][1].get():
                row = Frame(self.frmInput)
                lab = Label(
                    row,
                    text=value['label'],
                    justify=RIGHT,
                    anchor=E,
                    width=20,
                    bg='white',
                    fg=color['inputEntry'],
                    font=('Helvetica', sizeInputEntry, 'bold')
                )
                entry = Entry(
                    row, 
                    textvariable=value['current'][0], width=60
                )
                row.pack(side=TOP, fill=X)
                entry.pack(side=RIGHT, expand=YES, fill=X, padx=10)
                lab.pack(side=LEFT, expand=NO, fill=X, padx=10)



