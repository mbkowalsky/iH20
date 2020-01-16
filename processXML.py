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

# Computations
    mainElement = 'computations-info'    

    # Cycle through each key in computations and look for it in xml file 
    for var in VarProj.compVar:
        print('>>>Reading keyword:', var)
        entry = dat[rootElement][mainElement].get(var)
        selectOptions = VarProj.compVar[var].get('optionList')

        # Check whether keyword was found in xml file
        if entry:

            if selectOptions == None: 
                print("   'optionList' was not found")
                VarProj.compVar[var]['current'].set(entry)

            elif selectOptions == []: 
                # Keyword 'optionList' found but has no entries
                print("   'optionList' has no entries")
                VarProj.compVar[var]['current'].set(entry)

            else:
                # Keyword 'optionList' found and has entries
                print("   'optionList' entries:")
                print(selectOptions)
                value = []
                for key, tkval in selectOptions.items():
                    if tkval == entry:
                        value = key

                # Check whether xml entry corresponds to key in optionList
                if value:
                    print('   Option found for this entry:', value)
                   #VarProj.compVar[var]['current'].set(entry)
                    VarProj.compVar[var]['current'].set(value)
                else:
                    print('   XML entry:', entry)
                    print('   No option found for this entry')
                    MsgInformation(
                        [],
                        ['Message',
                         ('The unrecognized entry "'+entry+
                          '" was read for element <'+entry+'> '+
                          'in input file "'+VarProj.filename.get()+'."')
                        ])
        else:
            print('   Keyword not found:', var)

        # Print entire dictionary to screen:  
#       printDict(VarProj.compVar)

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


