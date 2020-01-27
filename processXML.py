#!/usr/bin/python
from tkinter           import *
from tkinter           import *
from settings          import *
from frameTools        import MsgInformation
import xmltodict
import os

def readXML(VarProj, VarMod):

    path = os.path.join(
        VarProj.projVar['directory']['current'].get(), 
        VarProj.projVar['file-name']['current'].get())

    with open(path) as fd:
        # Main dict with info from XML file:
        dat = xmltodict.parse(fd.read())

    multiElement = [
        'project-info', 
        'computations-info'
    ]
    multiVar = [
        VarProj.projVar, 
        VarProj.compVar
    ]

    printXML = False
    for tabNum in range(len(multiVar)):

        mainElement = multiElement[tabNum]   
        genVar = multiVar[tabNum]
        if printXML: print('>Reading', mainElement)

        # Cycle through each key and look for it in xml file 
        for var in genVar:
            if printXML: print(' >>>Reading keyword:', var)
            try:
                selectOptions = genVar[var].get('optionList')
            except:
                selectOptions = []

            entry = dat[rootElement][mainElement].get(var)
            if entry: #keyword was found in xml file
                if selectOptions == None:  
                    if printXML: print("    'optionList' was not found")
                    genVar[var]['current'].set(entry)

                elif selectOptions == []:
                   #print("    'optionList' has no entries")
                    if printXML: print('     entry found:', entry)
                    genVar[var]['current'].set(entry)
                else:
                    if printXML: print("    'optionList' entries:")
                    value = []
                    for key, tkval in selectOptions.items():
                        if tkval == entry:
                            value = key
                    if value:
                        if printXML: print('    Option found in list:', value)
                        genVar[var]['current'].set(value)
                    else:
                        if printXML: print('   No option found for this entry:', entry)
                        MsgInformation(
                            [],
                            ['Message',
                             ('No option found for this entry:'+entry)
                            ])
            else:
                if printXML: print('    Keyword not found in xml file:', var)

        # Print entire dictionary to screen:  
        if printXML: printDict(VarProj.compVar)

#Everything below here is to be removed/redone differently:
    modelNames = []
    modelNumbers= []
    modelComments = []
    simulatorNames = []
    modelInputFiles = []

# Model Setup
    modelElement = 'modelInfo'
    try:
        datlist = []
        test = dat[rootElement][modelElement] 
        if not isinstance(test, list):
            # For case of multiple models in a list
            datlist.append(test)   # For case of multiple models in a list
        else:
            datlist = test         # For case of one  model (not in a list)

    except KeyError:
        MsgInformation(
            [],
            ['Message',
             'Missing <'+modelElement+'> in xml file'
            ])

    modNum = 0
    for item in datlist:
        datXML = [
            ('modelNames', '@name'),
            ('modelNumbers', 'modelNumber'),
            ('simulatorNames', 'simulator'),
            ('modelComments', 'comment')
            ]
        # MBK!!! Should do this differently, not using eval. Plan to redo.
        for (variableString, xmlString) in datXML:
            try:
               #eval(variableString+'.append("'+item[xmlString]+'")')
                   
                if isinstance(item[xmlString],list):
                    for j in item[xmlString]:
                        eval(variableString+'.append("'+j+'")')
                else:
                    eval(variableString+'.append("'+item[xmlString]+'")')
                   
            except:
                eval(variableString+".append('')")

        # Special treatment for handling list with multiple entries
        try:
            modelInputFiles.append([])
            xmlString = 'input-file'
            if isinstance(item[xmlString],list):
                for j in item[xmlString]:
                    modelInputFiles[modNum].append(j)
            else:
                modelInputFiles[modNum].append(item[xmlString])
            modNum =+ 1
        except:
            modelInputFiles.append([])
            modelInputFiles[modNum].append('')
 
    VarProj.models.set(modelNames)
    VarProj.inputFiles.set(modelInputFiles)
    numModels = len(modelNames)
    for i in range(numModels):
        VarMod[i].inputFiles.set(modelInputFiles[i])
        VarMod[i].numInputFiles.set(len(modelInputFiles[i]))
        VarMod[i].name.set(modelNames[i])
        VarMod[i].num.set(modelNumbers[i])
        VarMod[i].comment.set(modelComments[i])
        VarMod[i].simulator.set(simulatorNames[i])
    VarProj.numMod.set(numModels)

# Results
    try:
        VarProj.results.set(dat[rootElement]['results']['file'])
    except (KeyError, TypeError) as info:
        VarProj.results.set('')
        print('XML msg:', info)

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


