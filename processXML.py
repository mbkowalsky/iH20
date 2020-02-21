#!/usr/bin/python
from tkinter           import *
from tkinter           import *
from settings          import *
from frameTools        import MsgInformation
import xmltodict
import os
import copy

def readXML(VarProj):

    path = os.path.join(
        VarProj.projVar['directory']['current'][0].get(), 
        VarProj.projVar['file-name']['current'][0].get())

    try: 
        with open(path) as fd:
            # Main dict with info from XML file:
            try:
                dat = xmltodict.parse(fd.read())
            except Exception as exceptionInfo: 
                MsgInformation(
                    [],
                    ['Error!', 
                        ('Error parsing input file "' + path
                            + '" due to "' + str(exceptionInfo) + '"'
                        )
                    ]
                )
                print(exceptionInfo)
                return
    except:
        MsgInformation(
            [],         
            ['Error!',
                ('Could not open project: ' + path)
            ]
        )
        return
    
    multiElement = [
        'project-info', 
        'computations-info',
        'model-info',
        'model-info'
    ]
    multiVar = [
        VarProj.projVar, 
        VarProj.compVar,
        VarProj.modelVar,
        VarProj.modelFiles
    ]
    multiList = [
        VarProj.projList, 
        VarProj.compList,
        VarProj.modelList,
        VarProj.modelFilesList,
    ]

    # Lists for workflow display:
    modelNames = []
    simulatorNames = []
    modelInputFiles = []

    printXML = False
    printMBK = False
    for tabNum in range(len(multiVar)):

        mainElement = multiElement[tabNum]   
        genVar = multiVar[tabNum]
        genList = multiList[tabNum]

        if printXML: print('>Reading', mainElement)

        testDat = dat[rootElement][mainElement]
        if printMBK: print('MBK mainElement:', testDat)
        
        numModels = 1
        if not mainElement.lower() == 'project-info':

            if not isinstance(testDat, list):
                numModels = 1
            else:
               #numModels = len([i for i in testDat if i])
                numModels = len(list(filter(None, testDat)))

            # Add to model variable list with default entries 
            if not genList == VarProj.modelFilesList:
                addModelToList(numModels, genVar, genList)

            # Add to model file list 
            if mainElement.lower() == 'model-info' and genList == VarProj.modelFilesList:
                addInputFilesToList(numModels, VarProj.modelFiles, VarProj.modelFilesList)

            if printMBK: print('MBK numModels:', numModels)
 
        for setNum in range(0, numModels):

            # Cycle through each key and look for it in xml file 
            for var in genVar:
                if printXML: print(' >>>Reading keyword:', var)
                try:
                    selectOptions = genVar[var].get('optionList')
                except:
                    selectOptions = []

                try:
                    if numModels > 1:
                        entry = dat[rootElement][mainElement][setNum].get(var)
                        if printMBK: print('MBK multiple:', entry)
                    else:
                        entry = testDat[var]
                        if printMBK: print('MBK single:', entry)
                except:
                    if printMBK: print('No can do:', rootElement, mainElement, var)
                    entry = []

                # Check if keyword entry is found in xml file
                if entry: 

                    # More than one entry with same keyword (excluding input files)
                    if isinstance(entry, list) and not var == 'input-file': 
                        entry = entry[-1]
                        MsgInformation(
                            [],
                            ['Warning!',
                            ('Multiple entries found for "' + var 
                            + '." Keeping the last entry: ' + entry.lower()
                            )
                            ])

                    if selectOptions == None:  
                        if printXML: print("    'optionList' was not found")
                        genList[var][setNum].set(entry)

                    elif selectOptions == []:
                        if printXML: print('     entry found:', entry)
                        if var == 'input-file':
                            if isinstance(entry, list):
                                genList[var][setNum] = entry
                            else:
                                genList[var][setNum] = [entry]
                        else:
                            genList[var][setNum].set(entry)
                    else:
                        if printXML: print("    'optionList' entries:")
                        value = []
                        for key, tkval in selectOptions.items():
                            # Compare lower case entries to allow mixed case
                            if tkval.lower() == entry.lower():
                                value = key
                        if value:
                            if printXML: print('    Option found in list:', value)
                            # Using value (not entry) due to order in keyComp, to be 
                            # compatible with how list is created for menu:
                            genList[var][setNum].set(value)
                        else:
                            if printXML: print('   No option found for this entry:', entry)
                            MsgInformation(
                                [],
                                ['Warning!',
                                ('The entry "' + entry 
                                 + '" is not a valid option for XML element "'
                                 + var 
                                 + '" in input file "'
                                 + path + '"')
                                ])
                else:
                    if printXML: print('    Keyword not found in xml file:', var)

    # Set variable strings for workflow display (MBK!!! may redo)
    numModels = 0
    for name in VarProj.modelVar['@name']['current']:
       numModels += 1
       modelNames.append(name.get())
    VarProj.models.set(modelNames)
    VarProj.numMod.set(numModels)

    for name in VarProj.modelVar['simulator']['current']:
       simulatorNames.append(name.get())
    VarProj.simulators.set(simulatorNames)

def addModelToList(numModels, genVar, genList):
    for i in range(numModels):
        for item in genVar:
           #genList[item].append(StringVar()) 
            # MBK!!! Not sure whether eval is a good approach
            genList[item].append(eval(genVar[item]['type'])) 
           #genList[item].append(genVar[item]['type']) 

def addInputFilesToList(numModels, genVar, genList):
    for i in range(numModels):
        for item in genVar:
           #genList[item].append('')
            genList[item].append([])

# Misc
def printDict(dictVar):

    print('Enumerate command:')
    for i in enumerate(dictVar.items()):
        print(i)

    print('Iterating:')
    for key in dictVar:
        print('> key:', key)
        for key2 in dictVar[key]:
            print('  >> key:', key2, ', value:', dictVar[key][key2])


