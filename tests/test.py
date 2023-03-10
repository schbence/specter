from tkinter import *
from tkinter import filedialog as fd
import numpy as np
import pandas as pd
from helpers import helpme
from dialogs import ChannelNamesDialog

root = Tk()
root.minsize(500,500)
root.maxsize(500,500)

def buttonCallback():
    print("Bye bye!")
    root.destroy()

def printCallback():
    print(ch_names)

def calcCallback(name):
    mean = a.mean()
    print(name)
    outVar.set("Opened: %s" % name)
    df = pd.DataFrame(a)
    df.to_csv('random-numbers.csv')
    ch_names = ChannelNamesDialog(5).getValues()
    print("- + -".join(ch_names))

def openCallback():
    global fname
    helpme('open ')
    fname = fd.askopenfilename()



a = np.random.uniform(0,1,[100,100])
fname = ""
ch_names = None

outVar = StringVar()
outLabel = Label(root, textvariable=outVar)
outLabel.pack()

openButton = Button(root, text="Open", command = openCallback)
openButton.pack()
calcButton = Button(root, text="Calculate", command = lambda : calcCallback(fname))
calcButton.pack()
printButton = Button(root, text="Print", command = printCallback)
printButton.pack()
exitButton = Button(root, text="Exit", command = buttonCallback)
exitButton.pack()


root.mainloop()
