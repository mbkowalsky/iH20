#!/usr/bin/python

# Reading xml file
rootElement = 'project'

#MBK!!! should change these settings to a class or dict
# Settings for colors
color = {
    'tab': 'white',
    'tabTitle': '#8E8E8E',
    'workflow': '#f6f6f6',
    'keyButton': '#8E8E8E',
    'infoBG':'white',
    'inputBG': 'white',
    'inputBox': '#8E8E8E',
    'container': 'white',
    'msgFont': 'black',
    'info': 'black',
    'infoEntry': 'gray',
    'inputEntry': 'gray',
    'separator': '#f6f6f6',
    'workBG': '#f6f6f6',
    'workLabel': 'black',
    'workEntry': 'grey',
    'tabDefault': '#f6f6f6',
    'tabActive': 'gray90',
    'titleTab': '#f6f6f6',
    'toolbar': '#f6f6f6',
    'canv': 'white',
    'addModel': 'white'
}

# Settings for colors
#color['tab']         = 'white'
tabTitleColor    = '#8E8E8E'
colorWorkflow    = '#f6f6f6'
keyButtonColor   = '#8E8E8E'
colorInfoBG      = 'white'
colorInputBG     = 'white'   #
colorInputBox    = '#8E8E8E'
colorContainer   = '#f6f6f6'  
colorContainer   = 'white'    
colorMsgFont     = 'black'
colorInfo        = 'black'
colorInfoEntry   = 'gray'
colorInputEntry  = 'gray'    #
#colorSeparator  = '#f6f6f6'
colorSeparator   = 'white'
colorSeparator   = '#f6f6f6'
#colorSeparator   = '#8E8E8E'
colorWorkBG      = '#f6f6f6'
colorWorkLabel   = 'black'
colorWorkEntry   = 'grey'
colorTabDefault  = '#f6f6f6'
colorTabActive   = 'gray90'
colorTitleTab    = '#f6f6f6'
colorToolbar     = '#f6f6f6'
colorCanv        = 'white'
colorAddModel    = 'white'

# Settings for text size
sizeTextWorkflow = 12
sizeWorkLabel = 14
sizeWorkEntry = 12
sizeInfoEntry    = 12
sizeInfoType     = 12
sizeInputEntry    = 12

# Canvas
canvasScrollRegion = (0, 0, 300, 800)
canvWidth = 550
canvHeight = 300
sizeCanvImage = (canvWidth-25, canvWidth-25)
(x0_CanvImage, y0_CanvImage) = (10, 20)

# Workflow
wrapLengthWF = 225

# Info
wrapLengthInfo = 200

# Results
dirResults = '/Users/mbkowalsky/mikek/work/software/python/py2app_v1/thumbs' 
initialOpenDirectory = '/Users/mbkowalsky/mikek/photos/2019_12_19_Private_Free_Luca/'

# Thumbnail images
dirThumbs = '/Users/mbkowalsky/mikek/work/software/python/py2app_v1/thumbs' 
sizeThumbs = (30,30)

# Variables for output entries in Information

# Info for loading recent project (???hardwired for now)
dirRecent = '/Users/mbkowalsky/mikek/work/software/python/py2app_v1'
fileRecent = 'projectInfo.xml'
fileRecent = 'projectOne.xml'
initialDirAddFile = '.'
#defaultProjName = 'My Project'
#defaultProjFilename = 'untitled.xml'






