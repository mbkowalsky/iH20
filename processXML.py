#!/usr/bin/python
from tkinter           import *
from tkinter           import *
from settings          import *
from frameTools        import MsgInformation
import xmltodict
import os

def readXML(VarProj, VarMod):

    path = os.path.join(VarProj.dir.get(), VarProj.filename.get())
    with open(path) as fd:
        dat = xmltodict.parse(fd.read())
    modelNames = []
    modelNumbers= []
    modelComments = []
    simulatorNames = []
    modelInputFiles = []

# Project
    rootAttribute = '@name'
    try:
        VarProj.name.set(dat[rootElement][rootAttribute])

   #MBK!!! Experimenting with handling xml reading errors...
   #       Note xmltodict error not caught if "=" and quotes missing
    except (KeyError, TypeError) as info:
        print('XML msg:', info)
        MsgInformation(
            [],
            ['Message',
             'Missing root attribute "'+rootAttribute+'" in xml file'
            ])

    VarProj.comment.set(dat[rootElement]['comments'])

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

    multiElement = [
        'project-info', 
        'computations-info'
    ]
    multiVar = [
        VarProj.projVar, 
        VarProj.compVar
    ]

    for tabNum in range(len(multiVar)):

        mainElement = multiElement[tabNum]   
        genVar = multiVar[tabNum]
        print('>Reading', mainElement)

        # Cycle through each key and look for it in xml file 
        for var in genVar:
            print(' >>>Reading keyword:', var)
            try:
                selectOptions = genVar[var].get('optionList')
            except:
                selectOptions = []

            entry = dat[rootElement][mainElement].get(var)
            if entry: #keyword was found in xml file
                if selectOptions == None:  
                    print("    'optionList' was not found")
                    genVar[var]['current'].set(entry)

                elif selectOptions == []:
                    print("    'optionList' has no entries")
                    print('     entry found:', entry)
                    genVar[var]['current'].set(entry)
                else:
                    print("    'optionList' entries:")
                    value = []
                    for key, tkval in selectOptions.items():
                        if tkval == entry:
                            value = key
                    if value:
                        print('    Option found in list:', value)
                        genVar[var]['current'].set(value)
                    else:
                        print('   No option found for this entry:', entry)
                        MsgInformation(
                            [],
                            ['Message',
                             ('No option found for this entry:'+entry)
                            ])
            else:
                print('    Keyword not found in xml file:', var)

        # Print entire dictionary to screen:  
       #printDict(VarProj.compVar)

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


