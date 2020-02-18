#!/usr/bin/python
from tkinter            import *
from tkinter.messagebox import *
from settings           import *
from frameTools         import msgNotImplemented
from PIL                import Image
from PIL.ImageTk        import PhotoImage
from frameInput         import openProject
from processXML         import readXML
import os, sys, math


b = lambda x: 3 + 2*x
a = lambda y: y * b(y)
a = lambda y: b(y)
print(a(1))
print(a(2))
print(b(1))
