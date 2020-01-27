#!/usr/bin/python
from tkinter           import *
from tkinter           import filedialog
from settings          import *
from frameTools        import MsgNotImplemented
from frameTools        import MsgInformation
from frameTools        import FrameSeparator
from frameTools        import FrameLabel
from processXML        import readXML
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
    def __init__(self, parent=None, nameInput=[], VarProj=[], VarMod=[]):
        Frame.__init__(self, parent)
        self.pack(expand=YES, fill=BOTH)

        self.title = FrameLabel(self, nameInput)
        self.frmLabelMenu = Frame(self)
        self.frmLabelMenu.config(bd=1, relief=FLAT, height=30, bg=color['tab'])

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
        self.menuOpenProject.pack(side=RIGHT, expand=YES, fill=X, padx=10, pady=5)

        self.frmProjectInfo = Frame(self)
        self.frmProjectInfo.pack(side=LEFT, fill=X, expand=YES)
        self.frmProjectInfo.config(bd=1, relief=FLAT, height=30, bg=color['tab'])

        self.optionsOpenProject.add_command(
            label='New', 
            command=lambda: onClickProjectMenu(
                VarProj, 
                VarMod, 
                'New', 
                self.frmProjectInfo))
        self.optionsOpenProject.add_command(
            label='Open from file', 
            command=lambda: onClickProjectMenu(
                VarProj, 
                VarMod, 
                'Open',
                self.frmProjectInfo))
        self.optionsOpenProject.add_command(
            label='Open demo',
            command=lambda: onClickProjectMenu(
                VarProj, 
                VarMod, 
                'Open demo', 
                self.frmProjectInfo))
        self.menuOpenProject.config(menu=self.optionsOpenProject)

        # Project files aleady specified, special case in openProject:
        if VarProj.typeProj.get()=='Open demo':
            openProject(VarProj, VarMod, 'Open demo', self.frmProjectInfo)
     
        # Parameters loaded previously, just populate entries:
# MBK!!! May rename inputLabelsCreated 
        if VarProj.inputLabelsCreated.get() == True:
            makeProjectLabels(VarProj, self.frmProjectInfo)

def onClickProjectMenu(VarProj, VarMod, typeIn, frmIn):
    VarProj.typeProj.set(typeIn)
    openProject(VarProj, VarMod, typeIn, frmIn)

def makeProjectLabels(VarProj, frmIn):
    for (label, value) in VarProj.projVar.items():
       #if value['current'].get():
            row = Frame(frmIn)
            lab = Label(row,
                text=value['label'],
                justify=RIGHT,
                anchor=E,
                width=40,
                bg='white',
                fg=color['inputEntry'],
                font=('Helvetica', sizeInputEntry, 'bold'))
            ent = Entry(row, textvariable=value['current'])
            row.pack(side=TOP, fill=X)
            ent.pack(side=RIGHT, expand=YES, fill=X, padx=10)
            lab.pack(side=LEFT, expand=NO, fill=X, padx=10)
    VarProj.inputLabelsCreated.set(True)

def openProject(VarProj, VarMod, fileNameIn, frmIn):

    # Set directory and filename depending on typeProj
    if VarProj.typeProj.get() == 'New':
        dirName = filedialog.askdirectory()
        if dirName:
            VarProj.projVar['directory']['current'].set(dirName)
        else:
            VarProj.projVar['directory']['current'].set('')
            
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
    if (dirName and 
           (VarProj.typeProj.get() in ['Open', 'Open demo'])):
        VarProj.projVar['file-name']['current'].set(fileName)
        VarProj.projVar['directory']['current'].set(dirName)
        readXML(VarProj, VarMod)
        # Initial file was read, so change typeProj
        VarProj.typeProj.set('Editing')

    elif dirName and VarProj.typeProj.get() == 'New':
        # Start with default values since new project
        # MBK!!! Add other workflow defaults eventually
        for name in ['file-name', 'project-name']:
            VarProj.projVar[name]['current'].set(
            VarProj.projVar[name]['default'])
        for name in VarProj.compVar:
            VarProj.compVar[name]['current'].set(
            VarProj.compVar[name]['default'])

    # Populate input entry boxes if not done earlier:
#   if VarProj.inputLabelsCreated.get() == False:
    if (VarProj.inputLabelsCreated.get() == False and
        dirName):
        makeProjectLabels(VarProj, frmIn)

def addFile(frm, VarProj, VarMod, i, loadExisting):
    if loadExisting == FALSE:
       #prevFile = VarMod[i].inputFiles.get()
        newFile = filedialog.askopenfilename(
            initialdir = initialDirAddFile,
            title = "Select",
            filetypes = (("xml files","*.xml"),("jpeg files","*.jpg"))
            )
        if newFile:
            fileName = []
            prevFile = VarMod[i].inputFiles.get()
            fileName.append(prevFile)
            fileName.append(newFile)
            VarMod[i].numInputFiles.set(VarMod[i].numInputFiles.get()+1)
            VarMod[i].inputFiles.set(fileName)
            print('digs1', fileName, VarMod[i].numInputFiles.get())
        else:
            MsgNotImplemented([], ['Message', 'Cancelled'])

   #if VarMod[i].numInputFiles.get()>0:
    if not VarMod[i].inputFiles.get() == '':
        fileNameLabel = Label(
            frm,
            textvariable=VarMod[i].inputFiles,
            justify=LEFT,
            anchor=NW,
            width=20,
            bg='white',
           #fg=color['inputEntry'],
            fg='black',
            font=('Helvetica', sizeInputEntry)
            )
        fileNameLabel.pack(side=TOP, expand=NO, fill=X, padx=10)

####################
# Model Setup
####################

class ModelInputContainer(Frame):
    """Create main container for Model Setup input.

    A sub frame for the title and "Add model" button is inserted
    here too. For now, when "Add model" is clicked, an additional subframe
    appears in this container (via AddModel class)
    """

    def __init__(self, parent=None, nameInput=[], VarProj=[], VarMod=[], NewModel = FALSE):
        Frame.__init__(self, parent)
        self.config(bd=2, relief=FLAT, height=30, bg=color['tab'])
        self.pack(side=TOP, fill=BOTH)
        self.title = FrameLabel(self, nameInput)
        self.frmTitle = Frame(self)
        self.frmTitle.pack(fill=X)
        self.frmTitle.config(bd=2, relief=FLAT, height=30, bg=color['tab'])

        # Existing models  
        if VarProj.numMod.get()>0:
            NewModel = FALSE
            for mNum in range(VarProj.numMod.get()):
                AddModel(self, VarProj, VarMod, mNum, NewModel)

        # New model
        addModelButton = Button(
            self.frmTitle,
            text='Add model',
            command=lambda:AddModel(self, VarProj, VarMod, VarProj.mNum.get(),TRUE),
            underline=0,
            bg=color['tab'])
        addModelButton.pack(side=RIGHT, fill=X, padx=0)

class AddModel(Frame):
    """Create subframe in ModelInputContainer for adding a new model.
    """

    def __init__(self, parent=None, VarProj=[], VarMod=[], i=0, NewModel=FALSE):
        # Create frame into which model frames will be placed:
        Frame.__init__(self, parent)
        self.config(bd=1, relief=SUNKEN, height=30, bg=color['tab'])
        self.pack(side=TOP, fill=X, pady=5, padx=10)
      
        # Create frame for button to delete model:
        self.frmButton = Frame(self)
        self.frmButton.pack(side=RIGHT, fill=NONE, expand=YES, anchor=NE)
        self.frmButton.config(bd=1, relief=FLAT, height=30, bg=color['inputBG'])
        self.deleteButton = Button(
            self.frmButton,
            text='Delete model',
            command=lambda:self.deleteModel(), 
            underline=0,
            bg=color['tab'])
        self.deleteButton.config(anchor=E)
        self.deleteButton.pack(side=TOP, fill=X, padx=5, pady=5)

        # Create frame for a model and its entries:
        self.frmInput = Frame(self)
        self.frmInput.pack(side=LEFT, fill=NONE, expand=YES, anchor=W)
        self.frmInput.config(bd=1, relief=FLAT, height=30, bg=color['tab'])

        # Create menu for simulator selection:
        row = Frame(self.frmInput)
        row.config(bg=colorAddModel)
        label = Label(
            row,
            text='Simulator:',
            justify=RIGHT,
            anchor=E,
            width=20,
            bg=colorAddModel,
            fg=color['inputEntry'],
            font=('Helvetica', sizeInputEntry, 'bold'))

        simOptions = [
            'None', 
            'TOUGH2', 
            'TOUGHREACT',
            'ECOSYS',
            'User supplied'
            ]

        self.simulatorMenu = OptionMenu(row, VarMod[i].simulator, *simOptions)
        self.simulatorMenu.config(
            justify=LEFT,
            underline=0,
            width=60)

        row.pack(side=TOP, fill=X)
        self.simulatorMenu.pack(side=RIGHT, fill=X, padx=10, pady=5)
        label.pack(side=LEFT, expand=NO, fill=X, padx=10)

        VarMod[i].num.set(VarProj.mNum.get())
        datModel = [
            ('Name of model:', VarMod[i].name),
            ('Model number:', VarMod[i].num),
            ('Comments:', VarMod[i].comment)
            ]

        # Add labels and entries for a model:
        for (label, value) in datModel:
            row = Frame(self.frmInput)
            lab = Label(row,
                text=label,
                justify=RIGHT,
                anchor=E,
                width=20,
                bg='white',
                fg=color['inputEntry'],
                font=('Helvetica', sizeInputEntry, 'bold'))
            entry = Entry(row, textvariable=value, width=60)
            row.pack(side=TOP, fill=X)
            entry.pack(side=RIGHT, expand=YES, fill=X, padx=10)
            lab.pack(side=LEFT, expand=NO, fill=X, padx=10)

        # Create button for adding new input files to a model:
        self.menuSelectFile = Menubutton(
           #self.frmInput,
            self.frmButton, 
            text='Add file',
            underline=0,
            bg=colorInputBox,
            width=0)
        self.optionsSelectFile = Menu(self.menuSelectFile)
        self.optionsSelectFile.add_command(
            label='Select File', 
            command=lambda:addFile(self.frmInput, VarProj, VarMod, i, FALSE))
        self.optionsSelectFile.add_command(
            label='Option 2', 
            command=MsgNotImplemented)
        self.menuSelectFile.config(menu=self.optionsSelectFile)
        self.menuSelectFile.pack(side=TOP, expand=YES, fill=X, padx=10, pady=5)

        self.nameLabel = Label(
            self.frmInput,
            text='Files:',
            justify=RIGHT,
            width=20,
            bg='white',
            fg=color['inputEntry'],
            font=('Helvetica', sizeInputEntry, 'bold'))
        self.nameLabel.config(anchor=E)
        self.nameLabel.pack(side=LEFT, expand=NO, fill=X, padx=10)

        # Disply existing input file names
        if not VarMod[i].inputFiles.get() == '':
            loadExisting = TRUE
            addFile(self.frmInput, VarProj, VarMod, i, loadExisting)

        VarProj.mNum.set(VarProj.mNum.get()+1)
        if NewModel == TRUE:
            VarProj.numMod.set(VarProj.numMod.get()+1)

    def deleteModel(self):
        # MBK!!! Need to actually remove model from variables.
        self.destroy()


####################
# Computations
####################
class CompInputContainer(Frame):
    """Create main container for Computations input.

    A sub frame...
    """

    def __init__(self, parent=None, nameInput=[], VarProj=[], VarMod=[], NewModel = FALSE):
        Frame.__init__(self, parent)
        self.config(bd=2, relief=FLAT, height=30, bg=color['tab'])
        self.pack(side=TOP, fill=BOTH)

        self.title = FrameLabel(self, nameInput)

        self.frmTop = Frame(self)
       #self.frmTop.pack(fill=X)
        self.frmTop.pack(side=TOP, fill=NONE, expand=YES, anchor=W, padx=10)
        self.frmTop.config(bd=2, relief=FLAT, height=30, bg=color['tab'])

        row = Frame(self.frmTop)
        row.config(bg=colorAddModel)
        label = Label(
            row,
            text=VarProj.compVar['application-mode']['label'],
            justify=RIGHT,
            anchor=E,
            width=20,
            bg=colorAddModel,
            fg=color['inputEntry'],
            font=('Helvetica', sizeInputEntry, 'bold'))

        compModeOptions = VarProj.compVar['application-mode']['optionList']
        if VarProj.compVar['application-mode']['current'].get()=='':
            for name in VarProj.compVar:
                VarProj.compVar[name]['current'].set(
                VarProj.compVar[name]['default'])
        self.simulatorMenu = OptionMenu(row, 
            VarProj.compVar['application-mode']['current'], 
            *compModeOptions,
            command=self.makeCompInput(
                VarProj.compVar['application-mode']['current'], 
                VarProj, 
                VarMod))
        self.simulatorMenu.config(
            justify=LEFT,
            underline=0,
            width=80)

        row.pack(side=TOP, fill=X)
        self.simulatorMenu.pack(side=RIGHT, fill=X, padx=10, pady=5)
        label.pack(side=LEFT, expand=NO, fill=X, padx=10)

    def makeCompInput(self, selectedMode, VarProj, VarMod):
        modeInput(self, VarProj, VarMod)

class modeInput(Frame):
    """Create subframe in CompInputContainer for selected application mode.
    """

    def __init__(self, parent=None, VarProj=[], VarMod=[]):
        # Create frame into which model frames will be placed:
        Frame.__init__(self, parent)
        self.config(bd=1, relief=SUNKEN, height=30, bg=color['tab'])
        self.pack(side=TOP, fill=X, pady=5, padx=10)
      
        # Create frame to enter for specs for selected application mode 
        self.frmInput = Frame(self)
        self.frmInput.pack(side=LEFT, fill=NONE, expand=YES, anchor=W)
        self.frmInput.config(bd=1, relief=FLAT, height=30, bg=color['tab'])

        self.frmButton = Frame(self)
        self.frmButton.pack(side=RIGHT, fill=NONE, expand=YES, anchor=NE)
        self.frmButton.config(bd=1, relief=FLAT, height=30, bg=color['inputBG'])
        self.deleteButton = Button(
            self.frmButton,
            text='Reset',
            command=lambda:MsgInformation([], ['Message', 'Not available']),
            underline=0,
            bg=color['tab'])
        self.deleteButton.config(anchor=E)
        self.deleteButton.pack(side=TOP, fill=X, padx=5, pady=5)

        # Add labels and entries for a model:
        for (label, value) in VarProj.compVar.items():
           #if not label == 'application-mode':
            if not label == 'application-mode' and value['current'].get():
                row = Frame(self.frmInput)
                lab = Label(row,
                    text=value['label'],
                    justify=RIGHT,
                    anchor=E,
                    width=20,
                    bg='white',
                    fg=color['inputEntry'],
                    font=('Helvetica', sizeInputEntry, 'bold'))
                entry = Entry(row, textvariable=value['current'], width=60)
                row.pack(side=TOP, fill=X)
                entry.pack(side=RIGHT, expand=YES, fill=X, padx=10)
                lab.pack(side=LEFT, expand=NO, fill=X, padx=10)



