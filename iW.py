#!/usr/bin/python
from tkinter            import *
from tkinter.messagebox import *
from tkinter            import filedialog
#from frameMenu          import MainMenu
from frameToolbar       import FrameToolbar
from frameInfo          import InfoSubFrame  
from frameInfo          import InfoTitleMenu
from frameInfo          import InfoCanvas
from frameInput         import FrameSubInput
from frameInput         import FrameInput
from frameInput         import ModelInputContainer
from frameInput         import ProjectContainer
from frameInput         import CompInputContainer
from frameSaveRun       import FrameSaveRun
from frameSaveRun       import GuiOutput
from frameSaveRun       import redirectedGuiShellCmd
from frameWorkflow      import WorkflowTab
from frameInfo          import InfoSummary
from frameExtra         import FrameExtra
from frameExtra         import FrameExtraMenu
from frameExtra         import FrameExtraItems
from processXML         import readXML
from frameTools         import FrameContainer
from frameTools         import FrameSeparator
from frameTools         import MsgInformation
from frameTools         import msgNotImplemented
from frameTools         import msgUnavailable
from frameTools         import clearFrame
from settings           import *
import os
from PIL                import Image
from PIL.ImageTk        import PhotoImage
#from subprocess         import Popen, PIPE
import subprocess

if __name__ == '__main__':

    root = Tk()

    class ProjectVariables(Frame):
        def __init__(self, parent=None, frm=[]):
            Frame.__init__(self, parent)
            self.frm = []

            self.typeProj = StringVar(value='Unknown')
            self.viewType = StringVar(value='images')
            self.inputLabelsCreated = BooleanVar(value=False)
            self.models = StringVar()
            self.simulators= StringVar()
            self.numMod = IntVar()
#Deleting as these get pulled into dictionaries or used elsewhere
            self.numPar = IntVar(value=0)
            self.numActivePar = IntVar(value=0)
            self.numInactivePar = IntVar(value=0)
            self.numObs = IntVar(value=0)
            self.mNum = IntVar()
            self.modelComment = StringVar()
            self.inputFiles = StringVar()
            self.editMode = StringVar()
            self.editMode.set('Normal mode')
            self.results = StringVar()

            self.canvasButtons = {
                'image': {
                    'label': 'View image',
                    'command': lambda:frmCanvas.onChoose(VarProj, frmTop)
                },
                'directory': {
                    'label': 'Load images in directory',
                    'command': lambda:frmCanvas.onChooseDir(VarProj, frmTop)
                },
                'next image': {
                    'label': 'Next image in directory',
                    'command': lambda:frmCanvas.onNext()
                },
                'text': {
                    'label': 'View text file',
                    'command': lambda:frmCanvas.onChooseFile(VarProj, frmTop, [])
                },
                'clear': {
                    'label': 'Clear',
                    'command': lambda:frmCanvas.onClear(VarProj, frmTop)
                }
            }

            self.canvasButtonStatus = {
                'image': StringVar(value='active'),
                'directory': StringVar(value='active'),
                'next image': StringVar(value='disabled'),
                'text': StringVar(value='active'),
                'clear': StringVar(value='active')}

            # Workflow control
            self.editButtonStatus = {
                'project': StringVar(value='active'),
                'models': StringVar(value='disabled'),
                'parameters': StringVar(value='disabled'),
                'observations': StringVar(value='disabled'),
                'computations': StringVar(value='disabled'),
                'results': StringVar(value='disabled')}

            # Status for workflow tabs
            self.status = {
                'project': BooleanVar(value='False'),
                'models': BooleanVar(value='False'),
                'parameters': BooleanVar(value='False'),
                'observations': BooleanVar(value='False'),
                'computations': BooleanVar(value='False'),
                'results': BooleanVar(value='False')}

# Project parameters
            keyProj = {
                'directory': ['Project directory:', [], dirRecent, 'StringVar()'],
                'file-name': ['Project filename:', [], 'My File', 'StringVar()'],
                'project-name': ['Project name:', [], 'My Project', 'StringVar()'],
                'comment': ['Comments:', [], [], 'StringVar()']}
            self.projList = {}
            self.projListPrev = {}
            self.projVar = {}
            for (name, items) in keyProj.items():
                print('keyProj.items:', name, items)
                self.projList[name]=[]
                self.projListPrev[name]=[]
                # Need to open project (i.e., before adding Models):
                self.projListPrev[name].append(StringVar())
                self.projList[name].append(StringVar())
                self.projVar.update({
                    name: {
                        'label': items[0],
                        'optionList': items[1],
                        'default': items[2],
                        'previous': self.projListPrev[name],
                        'current': self.projList[name],
                        'type': items[3]}})
    
# Model-setup parameters
            keyModel = {
                'number': ['Model number:', [], 99, 'IntVar()'],
                '@name': ['Name of model:', [], 'My Model', 'StringVar()'],
                'simulator': [
                    'Simulator:', {
                        'None': 'none',
                        'TOUGH2': 'tough2',
                        'TOUGHREACT': 'toughreact',
                        'ECOSYS': 'ecosys',
                        'User supplied': 'user'},
                    'None',
                    'StringVar()'],
                'comment': ['Comments:', [], [], 'StringVar()']}

            self.modelList = {}
            self.modelListPrev = {}
            self.modelVar = {}
            self.modelFilesList = {}
            self.modelFilesListPrev = {}
            self.modelFiles = {}

            for (name, items) in keyModel.items():
                print('keyModel.items:', name, items)
                self.modelList[name]=[]
                self.modelListPrev[name]=[]
                self.modelVar.update({
                    name: {
                        'label': items[0],
                        'optionList': items[1],
                        'default': items[2],
                        'previous': self.modelListPrev[name],
                        'current': self.modelList[name],
                        'type': items[3]}})

            keyInputFiles = {'input-file': ['Files:', [], [], 'string']}
            for (name, items) in keyInputFiles.items():
                print('keyInputFiles.items:', name, items)
                self.modelFilesList[name]=[]
                self.modelFilesListPrev[name]=[]
                self.modelFiles.update({
                    name: {
                        'label': items[0],
                        'optionList': items[1],
                        'default': items[2],
                        'previous': self.modelFilesListPrev[name],
                        'current': self.modelFilesList[name],
                        'type': items[3]}})

# Computational parameters
            keyComp = {
                'application-mode': [
                    'Application mode:', {
                         'Forward simulation': 'forward',
                         'Sensitivity analysis': 'sensitivity',
                         'Data-worth analysis': 'data-worth',
                         'Model calibration': 'calibration'},
                    'Forward Simulation',
                    'StringVar()'],
                'iterations': ['Number of iterations:', [], 1, 'IntVar()'],
                'incomplete': ['Incomplete runs allowed:', [], 1, 'IntVar()'],
                'levenberg': ['Levenberg parameter:', [], 1, 'IntVar()'],
                'marquardt': ['Marquardt parameter:', [], 10, 'IntVar()'],
                'comment': ['Comments:', [], [], 'StringVar()']}

            self.compList = {}
            self.compListPrev = {}
            self.compVar = {}

            for (name, items) in keyComp.items():
                print('keyComp.items:', name, items)
                self.compList[name]=[]
                self.compListPrev[name]=[]
                # Need before adding Models:
                self.compListPrev[name].append(StringVar())
                self.compList[name].append(StringVar())
                self.compVar.update({
                    name: {
                        'label': items[0],
                        'optionList': items[1],
                        'default': items[2],
                        'previous': self.compListPrev[name],
                        'current': self.compList[name],
                        'type': items[3]}})

           #Keeping this as may be a useful approach
           #}
           #defaults = {
           #    'interface' : '-en1',
           #    'verbose' : '-v',
           #    'fontname' : 'Courier',
           #    'point' : 12
           #self.compVar = dict(
           #    (d,StringVar(value=v)) for (d,v) in compVarInfo.items())

    VarProj = ProjectVariables()

    selectedTab = StringVar()
    commandOK = StringVar()
    msgText = StringVar()

    selectedTab.set('None')
    commandOK.set('True')
    msgText.set('None')

# Messages and key controls

    def frameMsgOKCancel(FrameIn, msgText, commandOK, VarProj):
        frm = Frame(FrameIn)
        frm.config(bd=1, relief=SUNKEN, bg=color['tab'])
        frm.pack(expand=NO, fill=X, side=BOTTOM)

        cancelButton = Button(
            frm, 
            text='Cancel', 
            command=lambda:onClickCancel())
        cancelButton.config(width=21, padx=0, pady=3)
        cancelButton.pack(side=RIGHT, fill=X)
        OK_Button = Button(
            frm, 
            text='OK', 
            command=lambda:onClickOK())
        OK_Button.config(width=21, padx=0, pady=3)
        OK_Button.pack(side=RIGHT, fill=X)

        label = Label(frm,
            text='Message:',     
            anchor=W,
            bg=color['tab'],
            fg=colorMsgFont,
            font=('Helvetica') )
        label.config(width=10, padx=3, pady=3)
        label.pack(side=LEFT)

        message = Label(frm,
            textvariable = msgText,
            anchor=W,
            bg=color['tab'],
            fg=colorMsgFont,
            font=('Helvetica') )
        message.config(width=70, padx=3, pady=3)
        message.pack(side=LEFT)

        def onClickOK():

            name = str(selectedTab.get())
            # Currently OK enabled only when editing workflow tab
            if not name=='None':  

                if askyesno(
                    'Verify OK', 
                    'Are you finished editing '+name+'?'):
                    
                    # MBK!!! Need new approach for checking/setting status
                    
                    #setEdit(VarProj)
                    #setStatus(VarProj)

                    if selectedTab.get() == 'Project':
                        if not VarProj.projVar['file-name']['current'][0].get()=="":
                            tabProjectInfo.editButton['state'] = 'active'
                            tabModelInfo.editButton['state'] = 'active'
                           #VarProj.statProj.set(True)
                            VarProj.status['project'].set(True)
                        else:
                            tabModelInfo.editButton['state'] = 'disabled'
                            tabObservationInfo.editButton['state'] = 'disabled'
                            tabParameterInfo.editButton['state'] = 'disabled'
                            tabComputationsInfo.editButton['state'] = 'disabled'
                            tabResults.editButton['state'] = 'disabled'
                            for key in VarProj.status:
                                VarProj.status[key].set(False)
                        changeTabColor(tabProjectInfo, colorTabDefault) 

                    elif selectedTab.get() == 'Model Setup':
                        tst = []
                        for name in VarProj.modelVar['@name']['current']:
                            tst.append(name.get())
                        VarProj.models.set(tst)
                        tst = []
                        for name in VarProj.modelVar['simulator']['current']:
                            tst.append(name.get())
                        VarProj.simulators.set(tst)

                        if (not 
                            VarProj.modelVar['simulator']['current'][0].get() == 'None'
                           ):
                           #tabComputationsInfo.editButton['state'] = 'active'
                            VarProj.status['models'].set(True)
                        else:
                            VarProj.status['models'].set(False)
                        changeTabColor(tabModelInfo, colorTabDefault) 

                    elif selectedTab.get() == 'Parameters':
                        if temporaryYesMan() == TRUE:
                            pass
                        else:
                            pass
                        changeTabColor(tabParameterInfo, colorTabDefault)

                    elif selectedTab.get() == 'Observations':
                        if temporaryYesMan() == TRUE:
                            pass
                        else:
                            pass
                        changeTabColor(tabObservationInfo, colorTabDefault)

                    elif selectedTab.get() == 'Computations':
                        if temporaryYesMan() == TRUE:
                            VarProj.status['computations'].set(True)
                        else:
                            VarProj.status['computations'].set(False)
                        changeTabColor(tabComputationsInfo, colorTabDefault)

                    printMsg('Available options: [not yet implemented]')
                    frmInputGlobal.destroy()
                else:
                    printMsg('Continue editing '+name+'.')
            else:
                # MBK!!! Must fix for OK but nothing is open
                MsgInformation(
                    [],
                    ['Message', 
                     'Available options include the following: [...]'
                    ])
        def onClickCancel():
            name = str(selectedTab.get())
            if not name=='None': 
                if askyesno('Verify Cancel', 'Cancel edits in '+name+'?'):
                    frmInputGlobal.destroy()
                    printMsg('Edits in '+name+' cancelled.') 
                else:
                    printMsg('Continue editing '+name+'.')
            else:
                # MBK!!! Must fix for Cancel but nothing is open
                MsgInformation(
                    [],
                    ['Message', 
                     'Available options include the following: [...]'
                    ])

        def temporaryYesMan(): #Just using this while developing code
            return TRUE
        # MBK!!! Need check for status and enable/disable edit buttons
        def setEdit(VarProj):
            return TRUE
        def setStatus(VarProj):
            return TRUE

# Menu and toolbar

    def mainMenu(FrameIn, VarProj):
        """Creates main menu, and toolbar.
        """
        frm = Frame(FrameIn)
        frm.pack(expand=YES, fill=BOTH)
        frm.master.title('iH2O')
        frm.master.iconbitmap(bitmap='gray50')
        frm.menubar = Menu(frm.master)
        frm.master.config(menu=frm.menubar)

        menuOptions = [
            ('File', 0,
             [('Open', 0, 
               lambda:onClickOpen(VarProj)),
              ('Open demo', 0, 
               lambda:onClickOpenDemo(VarProj)),
              ('Open recent', 0, 
               lambda:MsgInformation(
                   [], ['Message', 'Not available'])),
              ('Quit', 0, sys.exit)]),

            ('Edit', 0,
             [('Project', 0, 
               lambda:editProject()),
              ('Model Setup', 0, 
               lambda:editModelSetup()),
              ('Parameters', 0, 
               lambda:MsgInformation(
                   [], ['Message', 'Not available'])),
              ('Observations',0, 
               lambda:MsgInformation(
                   [], ['Message', 'Not available'])),
              ('Computations',0, 
               lambda:editComputations())]),

            ('Run', 0,
             [('Option 1', 0, 
               lambda:MsgInformation(
                   [], ['Message', 'Not available'])),
              ('Option 2', 0, 
               lambda:MsgInformation(
                   [], ['Message', 'Not available']))]),

            ('View', 0,
             [('Input files', 0, 
               lambda:frmCanvas.onViewFiles(VarProj)),
              ('Choose image', 0, 
               lambda:frmCanvas.onChoose()),
              ('Choose directory', 0, 
               lambda:frmCanvas.onChooseDir(VarProj))]),

            ('Help', 0,
             [('iH2O Help', 0, 
               lambda:help()),
              ('Support', 0, 
               lambda:support())]) ]

        for (name, key, items) in menuOptions:
            pulldown = Menu(frm.menubar)
            for (namesub, keysub, itemssub) in items:
                pulldown.add_command(label=namesub, command=itemssub)
            frm.menubar.add_cascade(
                label=name,
                underline=key,
                menu=pulldown)

        toolbar = Frame(frm, relief=GROOVE, bd=1)
        toolbar.pack(side=BOTTOM, fill=X, pady=0)
        toolbarOptions = [
           #('Open', 0, lambda:onClickOpen(VarProj)),
            ('Open demo', 0, lambda:onClickOpenDemo(VarProj)),
            ('Quit', 0, frm.quit)
            ]

        for (name, key, item) in toolbarOptions:
            toolbarButton = Button(
                toolbar,
                text=name,
                command=item)
            toolbarButton.pack(side=LEFT, expand=NO, fill=NONE)

        def onClickOpen(VarProj):
            VarProj.typeProj.set('Open')
            editProject()

        def onClickOpenDemo(VarProj):
            path = os.path.join(dirRecent, fileRecent)
            VarProj.typeProj.set('Open demo') 
            VarProj.inputLabelsCreated.set(True)
            editProject()

        # Temporary option to enable all edit buttons (debug mode)
        frmRadio = Frame(toolbar)
        frmRadio.config(bd=1, relief=FLAT, bg=color['miniFrame'])
        frmRadio.pack(side=LEFT, expand=NO, fill=NONE, padx=10)
        modeOptions = [
            'Normal mode',
            'Edit-all mode'
        ]
        radios = []
        for mode in modeOptions:
            radio = Radiobutton(
                frmRadio,
                text=mode, 
                value=mode,
                variable=VarProj.editMode, 
                command=lambda:setEditButtons())
            radio.pack(side=LEFT, expand=NO, fill=NONE)
            radios.append(radio)

# checkBoxVal = IntVar()
# checkBox = Checkbutton(toolbar, variable=checkBoxVal, text='Debug mode')
# checkBox.pack(side=LEFT, expand=NO, fill=NONE)

        def setEditButtons():
            # MBK!!! For now can only switch "to" debug mode, then disabled
            if VarProj.editMode.get() == 'Debug mode':
                for tab in VarProj.editButtonStatus:
                    VarProj.editButtonStatus[tab].set('active')
                    tabProjectInfo.editButton['state'] = 'active'
                    tabModelInfo.editButton['state'] = 'active'
                    tabParameterInfo.editButton['state'] = 'active'
                    tabObservationInfo.editButton['state'] = 'active'
                    tabComputationsInfo.editButton['state'] = 'active'
                    tabResults.editButton['state'] = 'active',
                radios[0].config(state='disabled')
                radios[1].config(state='disabled')

        # MBK!!!: Toolbar images not doing anything
        def imageMenu():
            size = sizeThumbs
            thumbs = []
            photoObjs = []
            if os.path.exists(dirThumbs):
                for imgfile in os.listdir(dirThumbs):
                    path = os.path.join(dirThumbs, imgfile)
                    if not imgfile.startswith('.'): #skip .DS_Store file
                        obj = Image.open(path)
                        obj.thumbnail((size[0], size[1]), Image.ANTIALIAS)
                        thumbs.append((imgfile,obj))
                for (imgfile, obj) in thumbs:
                    img = PhotoImage(obj)
                    photoObjs.append(img)
            else:
                showerror('Error', 'Directory does not exist!\n'+dirThumbs)
            return photoObjs
  
#           for obj in photoObjs:
#               bt = Button(toolbar, image=obj, command=msgNotImplemented)
#               bt.pack(side=RIGHT, expand=NO, fill=NONE) 
#       tst=imageMenu()
#       for obj in photoObjs:
#           bt = Button(toolbar, image=obj, command=msgNotImplemented)
#           bt.pack(side=RIGHT, expand=NO, fill=NONE)

        photoObjs = imageMenu()
        for obj in photoObjs:
            bt = Button(toolbar, image=obj, command=msgNotImplemented)
            bt.pack(side=RIGHT, expand=NO, fill=NONE)

    frmMainMenu = mainMenu(root, VarProj)
    frmInfoGlobal = FrameContainer()         

# Information, Input, Controls

    # MBK!!! to be swapped out with new dictionary references, as developed
    datInfoSummary = [
        ('Project Name:', VarProj.projVar['project-name']['current']),
        ('Models:',       VarProj.numMod),
        ('Parameters:',   VarProj.numPar),
        ('Observations:', VarProj.numObs),
        ('Application:',  VarProj.compVar['application-mode']['current']),
        ('Results:',      VarProj.results),
        ('Comments:',     VarProj.projVar['comment']['current'])
        ]

    # Frames for Information
    frmTop = InfoTitleMenu(frmInfoGlobal, 'Project details', VarProj)
    frmSubInfo = InfoSubFrame(frmInfoGlobal)

    # Frames for canvas and summary info
    frmCanvas = InfoCanvas(frmSubInfo, VarProj, frmTop)
    InfoCanvas.makeCanvImage(frmCanvas, 'iHHO_logo_noBackground.png') 

    frmSummary = InfoSummary(frmSubInfo, datInfoSummary)
    frmSep = FrameSeparator(frmInfoGlobal, TOP, colorSeparator, 10)

    # Frames for Key Controls and Messages 
    FrameSeparator(frmInfoGlobal,)
    FrameSaveRun(frmInfoGlobal, VarProj)

    # Main frames for Input
    frmSubInput = FrameSubInput(frmInfoGlobal)
    frmInputGlobal = FrameInput(frmSubInput)
    frmMsg = frameMsgOKCancel(frmInfoGlobal,msgText,commandOK, VarProj)
 
    def onViewFiles():
#       try:
#           print('Before:', frmCanvas.buttons[0]['text'])
#          #frmCanvas.buttons[0]['text']='X'
#       except:
#           print('MBK no can do')
        frmCanvas.makeCanvText()

    def onViewImages():
        frmCanvas.makeCanvImage()

    def onChooseImage():
        frmCanvas.onChoose()
# MBK!!! here check/remove this
    def onChooseFile():
        frmCanvas.onChooseFile(VarProj)

# Workflow
    frm = []
    tabProjectInfo = WorkflowTab(
        frm,
        'Project', lambda:editProject(),
        [('Name:', VarProj.projVar['project-name']['current']),
         ('File:', VarProj.projVar['file-name']['current']),
         ('Comments:', VarProj.projVar['comment']['current'])],
        VarProj.editButtonStatus['project'],
        VarProj.status['project'])

    # MBK!!! Still sorting out multi-dimensional model variable
    i = 0 #Just printing of a few variables from first model (i=0) below 
    
    tabModelInfo = WorkflowTab(
        frm,
        'Model Setup', lambda:editModelSetup(),
        [('Simulators:', VarProj.simulators),
         ('Models:', VarProj.models)],
        VarProj.editButtonStatus['models'],
        VarProj.status['models'])
    tabParameterInfo = WorkflowTab(
        frm,
        'Parameters', lambda:editParameters(),
        [('Active:', VarProj.numActivePar),
         ('Inactive:', VarProj.numInactivePar)],
        VarProj.editButtonStatus['parameters'],
        VarProj.status['parameters'])
    tabObservationInfo = WorkflowTab(
        frm,
        'Observations', lambda:editObservations(),
       #[('Number:', VarProj.numObs)],
        [('Edit status:', VarProj.editButtonStatus['observations'])],
        VarProj.editButtonStatus['observations'],
        VarProj.status['observations'])
    tabComputationsInfo = WorkflowTab(
        frm,
        'Computations', lambda:editComputations(),
        [('Mode:', VarProj.compVar['application-mode']['current']),
         ('Comments:', VarProj.compVar['comment']['current'])],
        VarProj.editButtonStatus['computations'],
        VarProj.status['computations'])
    tabResults = WorkflowTab(
        frm,
        'Results', lambda:msgNotImplemented(),
        [('Output:', VarProj.results),
         ('Status:', VarProj.status)],
        VarProj.editButtonStatus['results'],
        VarProj.status['results'])

# Extra stuff to be used elsewhere or deleted

#   FrameExtraMenu()  #Keep for now in case useful later
#   FrameExtraItems() #Keep for now in case useful later

# Misc 

    def viewImage():
        frmCanvas.canv.itemconfig(
            frmCanvas.canvImage, 
            image = frmCanvas.thumbs[3])

    def openTest():
        file = filedialog.askopenfilename(
            initialdir = ".",
            title = "Select image",
            filetypes = (("xml files","*.xml"),("jpeg files","*.jpg")))

        obj = Image.open(file)
        obj.thumbnail(sizeCanvImage, Image.ANTIALIAS)
        tst = PhotoImage(obj)

        frmCanvas.thumbs[0] = tst
        frmCanvas.canv.itemconfig(frmCanvas.canvImage, image = tst)

    def editProject():
        global frmInputGlobal                                    
        selectedTab.set('Project')                          
        changeTabsToDefaultColor()
        changeTabColor(tabProjectInfo, colorTabActive)            
        clearFrame(frmInputGlobal)                        
        frmInputGlobal = FrameInput(frmSubInput)
        ProjectContainer(
            frmInputGlobal, 
            'Project details', 
            VarProj)
        printMsg('"Edit Project" clicked.')                 

    def editModelSetup():
        global frmInputGlobal
        selectedTab.set('Model Setup')
        changeTabsToDefaultColor()
        changeTabColor(tabModelInfo, colorTabActive)
        clearFrame(frmInputGlobal)
        frmInputGlobal = FrameInput(frmSubInput)
        isNewModel = False
        VarProj.mNum.set(0)
        ModelInputContainer(
            frmInputGlobal, 
            'Model Setup', 
            VarProj, 
            isNewModel,
            frmCanvas,
            frmTop)
        printMsg('"Edit Model Setup" clicked.')

    def editParameters():
        global frmInputGlobal
        selectedTab.set('Parameters')
        changeTabsToDefaultColor()
        changeTabColor(tabParameterInfo, colorTabActive)
        clearFrame(frmInputGlobal)
        printMsg('"Edit Parameters" clicked.')

    def editObservations():
        global frmInputGlobal
        selectedTab.set('Observations')
        changeTabsToDefaultColor()
        changeTabColor(tabObservationInfo, colorTabActive)
        clearFrame(frmInputGlobal)
        printMsg('"Edit Observations" clicked.')

    def editComputations():
        global frmInputGlobal
        selectedTab.set('Computations')
        changeTabsToDefaultColor()
        changeTabColor(tabComputationsInfo, colorTabActive)
        clearFrame(frmInputGlobal)
        frmInputGlobal = FrameInput(frmSubInput)
        isNewModel = False
        CompInputContainer(
            frmInputGlobal, 
            'Computations', 
            VarProj, 
            isNewModel)
        printMsg('"Edit Computations" clicked.')

    def changeTabColor(tabType, color):
        tabType.title['bg'] = color
        tabType.frmBox['bg'] = color
        tabType.frmBoxInner['bg'] = color
        tabType.editButton['bg'] = color
        tabType.checkBox['bg'] = color
        for i in range(len(tabType.rows)):
            tabType.rows[i]['bg'] = color
            tabType.colNames[i].config(bg = color)
            tabType.colValues[i].config(bg = color)

    # MBK!!! Temporary way to change color to default 
    def changeTabsToDefaultColor():
        for tab in [tabProjectInfo, 
                    tabModelInfo, 
                    tabParameterInfo, 
                    tabObservationInfo, 
                    tabComputationsInfo]:
            changeTabColor(tab, colorTabDefault)

    def printMsg(msg):
        msgText.set(msg)

    def clearTop():
        global frmInputGlobal
        clearFrame(frmInputGlobal)

    """Stuff to delete:
    textOut = Text()
    textOut.pack()

    def ls_proc():
        return Popen(['ls'], stdout=PIPE)

    with dir_proc() as p:
        if p.stdout:
            for line in p.stdout:
                textOut.insert(END, line)
        if p.stderr:
            for line in p.stderr:
                textOut.insert(END, line)

#   ls_proc = Popen('ls', stdout=open('2020_01_31_Test.txt', 'w'))
#   ls_proc = Popen('ls', stdout=PIPE, stderr=PIPE)
#   out, err = ls_proc.communicate()
    result = subprocess.run(['ls', '-l'], stdout=subprocess.PIPE)
    print('MBK output:', result.stdout.decode('utf-8'))

    Button(root, text='Test output',
          #command=lambda: redirectedGuiShellCmd('ls -lt')).pack(fill=X)
           command=lambda: redirectedGuiShellCmd('itough2')).pack(fill=X)
    """

    root.mainloop()


