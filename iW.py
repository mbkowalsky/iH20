#!/usr/bin/python
from tkinter            import *
from tkinter.messagebox import *
from tkinter            import filedialog
from frameMenu          import MainMenu
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
from PIL               import Image
from PIL.ImageTk       import PhotoImage

if __name__ == '__main__':

    root = Tk()

    class ProjectVariables(Frame):
        def __init__(self, parent=None, frm=[]):
            Frame.__init__(self, parent)
            self.frm = []

            self.dir = StringVar()
            self.file = StringVar()
            self.filename = StringVar()
            self.name = StringVar()
            self.comment = StringVar()
            self.status = StringVar()
            self.numMod = IntVar()
            self.mNum = IntVar()
            self.numPar = StringVar(value=0)
            self.numActivePar = StringVar(value=0)
            self.numInactivePar = StringVar(value=0)
            self.numObs = StringVar(value=0)
            self.results = StringVar()
            self.models = StringVar()
            self.modelComment = StringVar()
            self.inputFiles = StringVar()
            self.editMode = StringVar()
            self.editMode.set('Debug mode')

            # Workflow control
            self.editButtonStatus = {
                'project': StringVar(value='active'),
                'models': StringVar(value='active'),
                'parameters': StringVar(value='disabled'),
                'observations': StringVar(value='disabled'),
                'computations': StringVar(value='active'),
                'results': StringVar(value='disabled')}

            # Status for workflow tabs
            self.status = {
                'project': BooleanVar(value='False'),
                'models': BooleanVar(value='False'),
                'parameters': BooleanVar(value='False'),
                'observations': BooleanVar(value='False'),
                'computations': BooleanVar(value='False'),
                'results': BooleanVar(value='False')}

           # Computational parameters
            self.compVar = {
                'application-mode': {
                    'label': 'Application mode:',
                    'optionList': {
                        'Forward simulation': 'forward',
                        'Sensitivity analysis': 'sensitivity',
                        'Data-worth analysis': 'data-worth',
                        'Model calibration': 'calibration'},
                    'default': 'Forward simulation',
                    'previous': [],
                    'current': StringVar()},
                'iterations': {
                    'label': 'Number of iterations:',
                    'optionList': [],
                    'default': 1,
                    'previous': [],
                    'current': StringVar()},
                'incomplete': {
                    'label': 'Incomplete runs allowed:',
                    'optionList': [],
                    'default': 1,
                    'previous': [],
                    'current': StringVar()},
                'levenberg': {
                    'label': 'Levenberg parameter:',
                    'optionList': [],
                    'default': 1,
                    'previous': [],
                    'current': StringVar()},
                'marquardt': {
                    'label': 'Marquardt parameter:',
                    'optionList': [],
                    'default': 10.0,
                    'previous': [],
                    'current': StringVar()},
                'comment': {
                    'label': 'Comments:',
                    'optionList': [],
                    'default': [],
                    'previous': [],
                    'current': StringVar()},
                'generic': {
                    'label': 'Generic parameter:',
                    'default': 10.0,
                    'previous': [],
                    'current': StringVar()},
                'test': {
                    'label': 'Test parameter:',
                    'default': 10.0,
                    'previous': [],
                    'current': StringVar()},
            }

           #Keeping this as may be a useful approach
           #}
           #defaults = {
           #    'interface' : '-en1',
           #    'verbose' : '-v',
           #    'fontname' : 'Courier',
           #    'point' : 12
           #self.compVar = dict((d,StringVar(value=v)) for (d,v) in compVarInfo.items())

    class ModelVariables(Frame):
        def __init__(self, parent=None, frm=[]):
            Frame.__init__(self, parent)
            self.frm = []
            self.file = StringVar()
            self.name = StringVar()
            self.comment = StringVar()
            self.status = StringVar()
            self.num = IntVar()
            self.numPar = IntVar()
            self.numActivePar = IntVar()
            self.numInactivePar = IntVar()
            self.numObs = IntVar()
            self.simulator = StringVar()
            self.simulator.set('None')
            self.inputFiles = StringVar()
            self.numInputFiles = IntVar()

    selectedTab = StringVar()
    commandOK = StringVar()
    msgText = StringVar()

    selectedTab.set('None')
    commandOK.set('True')
    msgText.set('None')

    VarProj = ProjectVariables()
#MBK!!! This approach needs to be redone differently 
    VarMod = [ModelVariables(), 
              ModelVariables(), 
              ModelVariables(), 
              ModelVariables(), 
              ModelVariables()]

# Messages and key controls

    def frameMsgOKCancel(FrameIn, msgText, commandOK, VarProj):
        frm = Frame(FrameIn)
        frm.config(bd=1, relief=SUNKEN, bg=tabColor)
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
            bg=tabColor,
            fg=colorMsgFont,
            font=('Helvetica') )
        label.config(width=10, padx=3, pady=3)
        label.pack(side=LEFT)

        message = Label(frm,
            textvariable = msgText,
            anchor=W,
            bg=tabColor,
            fg=colorMsgFont,
            font=('Helvetica') )
        message.config(width=70, padx=3, pady=3)
        message.pack(side=LEFT)

        def onClickOK():

            name = str(selectedTab.get())
            # Currently OK enabled only when editing workflow tab
            if not name=='None':  

                if askyesno('Verify OK', 'Are you finished editing '+name+'?'):
                    # MBK!!! Need to implement new approach for checking/setting status
                    
                    #setEdit(VarProj, VarMod)
                    #setStatus(VarProj, VarMod)

                    if selectedTab.get() == 'Project':
                        if not VarProj.filename.get()=="":
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
                            VarProj.status['project'].set(False)
                            VarProj.status['models'].set(False)
                            VarProj.status['parameters'].set(False)
                            VarProj.status['observations'].set(False)
                            VarProj.status['computations'].set(False)
                            VarProj.status['results'].set(False)
                        changeTabColor(tabProjectInfo, colorTabDefault) 

                    elif selectedTab.get() == 'Model Setup':
                       #if temporaryYesMan() == TRUE:
                        # MBK!!! For now just checking simulator 
                        if (not VarMod[0].simulator.get() == 'None' and
                            not VarMod[0].inputFiles.get() == ''):
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
                # MBK!!! Must add guidance for when OK is clicked but nothing is open
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
                # MBK!!! Must add guidance for when Cancel is clicked but nothing is open
                MsgInformation(
                    [],
                    ['Message', 
                     'Available options include the following: [...]'
                    ])

        def temporaryYesMan(): #Just using this while developing code
            return TRUE
        # MBK!!! Need to create routines to check status and enable/disable edit buttons
        def setEdit(VarProj, VarMod):
            return TRUE
        def setStatus(VarProj, VarMod):
            return TRUE

# Menu and toolbar

    menuOptions = [
        ('File', 0,
         [('Open',        0, lambda:frmMainMenu.onClickOpen(VarProj, VarMod)),
          ('Open Recent', 0, lambda:MsgInformation([], ['Message', 'Not available'])),
          ('Quit',        0, sys.exit)]),
        ('Edit',          0,
         [('Project',     0, lambda:editProject()),
          ('Model Setup', 0, lambda:editModelSetup()),
          ('Parameters',  0, lambda:MsgInformation([], ['Message', 'Not available'])),
          ('Observations',0, lambda:MsgInformation([], ['Message', 'Not available'])),
          ('Computations',0, lambda:editComputations())]),
        ('Run', 0,
         [('Option 1',    0, lambda:MsgInformation([], ['Message', 'Not available'])),
          ('Option 2',    0, lambda:MsgInformation([], ['Message', 'Not available']))]),
        ('View', 0,
         [('Choose image',     0, lambda:frmCanvas.onChoose()),
          ('Choose directory', 0, lambda:frmCanvas.onList())]),
        ('Help', 0,
         [('iH2O Help',   0, lambda:help()),
          ('Support',     0, lambda:support())]) ]

    frmMainMenu = MainMenu(root, menuOptions, VarProj, VarMod)
    frmInfoGlobal = FrameContainer()         

#MBK!!! Need to implement tool for opening and displaying text file???
    # Menu that appears at top of Information
    datInfoMenu = [
        ('Choose image', lambda:frmCanvas.onChoose()),
        ('Choose file', lambda:msgUnavailable())
        ]
   
# Information, Input, Controls

    datInfoSummary = [
        ('Project Name:', VarProj.name),
        ('Models:',       VarProj.numMod),
        ('Parameters:',   VarProj.numPar),
        ('Observations:', VarProj.numObs),
        ('Application:',  VarProj.compVar['application-mode']['current']),
        ('Results:',      VarProj.results),
        ('Comments:',     VarProj.comment)
        ]

    # Frames for Information
    frmTop = InfoTitleMenu(frmInfoGlobal, 'Project details', datInfoMenu)
    frmSubInfo = InfoSubFrame(frmInfoGlobal)

    # Frames for canvas and summary info
    frmCanvas = InfoCanvas(frmSubInfo)
    frmSummary = InfoSummary(frmSubInfo, datInfoSummary)
    frmSep = FrameSeparator(frmInfoGlobal, TOP, colorSeparator, 10)

    # Frames for Key Controls and Messages 
    FrameSeparator(frmInfoGlobal,)
    FrameSaveRun(frmInfoGlobal,)

    # Main frames for Input
    frmSubInput = FrameSubInput(frmInfoGlobal)
    frmInputGlobal = FrameInput(frmSubInput)
    frmMsg = frameMsgOKCancel(frmInfoGlobal,msgText,commandOK, VarProj)
  
# Workflow

    frm = []
    tabProjectInfo = WorkflowTab(
        frm,
        'Project', lambda:editProject(),
        [('Name:', VarProj.name),
         ('File:', VarProj.filename),
         ('Comments:', VarProj.comment)],
        VarProj.editButtonStatus['project'],
        VarProj.status['project'])

    # MBK!!! Still sorting out multi-dimensional model variable
    i = 0 #Just printing of a few variables from first model (i=0) below 
    
    tabModelInfo = WorkflowTab(
        frm,
        'Model Setup', lambda:editModelSetup(),
        [('Models:', VarProj.numMod),
         ('Model name:', VarMod[i].name),
        #('Input files:', VarMod[i].inputFilesProjectContainer)],
         ('Input files:', VarMod[i].inputFiles)],
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
        [('Number:', VarProj.numObs)],
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
        frmCanvas.canv.itemconfig(frmCanvas.canvImage, image = frmCanvas.thumbs[3])

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
        changeTabColor(tabProjectInfo,  colorTabActive)            
        clearFrame(frmInputGlobal)                        
        frmInputGlobal = FrameInput(frmSubInput)
        datProj = [
            # MBK!!! Need to add control on user changing directory in entry widget
            ('Project directory:', VarProj.dir),
            # MBK!!! May need to add control in entry widget on characters or 
            #        have popup dialog together with directory selection
            ('Project filename:', VarProj.filename),
            ('Project name:', VarProj.name),
            ('Comments:', VarProj.comment)
            ]
        ProjectContainer(frmInputGlobal, 'Project details', datProj, VarProj, VarMod) 
        printMsg('"Edit Project" clicked.')                 

    def editModelSetup():
        global frmInputGlobal
        selectedTab.set('Model Setup')
        changeTabsToDefaultColor()
        changeTabColor(tabModelInfo, colorTabActive)
        clearFrame(frmInputGlobal)
        frmInputGlobal = FrameInput(frmSubInput)
        NewModel = False
        VarProj.mNum.set(0)
        ModelInputContainer(frmInputGlobal, 'Model Setup', VarProj, VarMod, NewModel)
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
        NewModel = False
        CompInputContainer(frmInputGlobal, 'Computations', VarProj, VarMod, NewModel)
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

    # MBK!!! Temporary way to change color to default during code development:
    def changeTabsToDefaultColor():
            changeTabColor(tabProjectInfo, colorTabDefault)
            changeTabColor(tabModelInfo, colorTabDefault)
            changeTabColor(tabParameterInfo, colorTabDefault)
            changeTabColor(tabObservationInfo, colorTabDefault)
            changeTabColor(tabComputationsInfo, colorTabDefault)

    def printMsg(msg):
        msgText.set(msg)

    def clearTop():
        global frmInputGlobal
        clearFrame(frmInputGlobal)

    root.mainloop()


