import pygame
import tkinter as tk
from tkinter import *
import os

#https://stackoverflow.com/questions/50487957/print-all-pygame-events-in-a-tkinter-mainloop
#TODO: save up to 10 colours (and also ability to export to txt file). use 10 smaller-than-the-main buttons to show these colours. these smaller buttons should also be able to copy their colour to the clipboard when clicked.

mainWindow = tk.Tk()
mainWindow.title("Colour Picker")

embed = tk.Frame(mainWindow, width = 500, height = 500) #creates embed frame    for pygame window
embed.grid(column=0,row=0,rowspan=3)

redSlider = Scale(mainWindow,from_=0,to=1,resolution=0.01,label="Red")
redSlider.grid(column=1,row=2)

greenSlider = Scale(mainWindow,from_=0,to=1,resolution=0.01,label="Green")
greenSlider.grid(column=2,row=2)

blueSlider = Scale(mainWindow,from_=0,to=1,resolution=0.01,label="Blue")
blueSlider.grid(column=3,row=2)

colourLabel = Label(mainWindow,text="Colour:")
colourLabel.grid(column=1,columnspan=3,row=0,sticky=S)

colourOutput = Entry(mainWindow,width=25,state="readonly")
colourOutput.grid(column=1,columnspan=3,row=1,sticky=N)

hexOutput = Entry(mainWindow,width=25,state="readonly")
hexOutput.grid(column=1,columnspan=3,row=1)

def writeToOutput(colourData):
    colourOutput.config(state=NORMAL)
    colourOutput.delete(0,END)
    colourOutput.insert(0,colourData)
    colourOutput.config(state="readonly")

def writeToHex(colourData):
    hexOutput.config(state=NORMAL)
    hexOutput.delete(0,END)
    hexOutput.insert(0,colourData)
    hexOutput.config(state="readonly")

def convertToHexCol(RGB):
    colour = "#"
    for i, colours in enumerate(RGB):
        if colours != 0:
            if len(hex(RGB[i]).lstrip("0x")) < 2:
                colour += "0" + hex(RGB[i]).lstrip("0x")
            else:
                colour += hex(RGB[i]).lstrip("0x")
        else:
            colour += "00"
    return colour

def copyColourToCB():
    mainWindow.clipboard_clear()
    mainWindow.clipboard_append(hexOutput.get())

colourButton = Button(mainWindow,width=10, command=copyColourToCB)#,state=DISABLED)
colourButton.grid(column=1,columnspan=3,row=0)

os.environ['SDL_WINDOWID'] = str(embed.winfo_id())
os.environ['SDL_VIDEODRIVER'] = 'windib'

screen = pygame.display.set_mode((500,500))
screen.fill(pygame.Color(255,255,255))
pygame.display.init()
pygame.display.update()

clock = pygame.time.Clock()

isFrozen = False

while True:
    redVal = redSlider.get()
    blueVal = blueSlider.get()
    greenVal = greenSlider.get()
    for event in pygame.event.get():
        if event.type == pygame.MOUSEMOTION:
            if not isFrozen:
                colour = [ round(redVal*(255-(255/5000)*((event.pos[0]/10)**2+(event.pos[1]/10)**2))) , round(greenVal*((255/50)*(event.pos[0]/10))) , round(blueVal*((255/50)*(event.pos[1]/10))) ]
                hexColour = convertToHexCol([ round(redVal*(255-(255/5000)*((event.pos[0]/10)**2+(event.pos[1]/10)**2))) , round(greenVal*((255/50)*(event.pos[0]/10))) , round(blueVal*((255/50)*(event.pos[1]/10))) ])
                writeToOutput(colour)
                writeToHex(hexColour)
                colourButton.config(background=hexColour)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if isFrozen:
                isFrozen = False
            else:
                isFrozen = True


    for x in range(0,50):
        for y in range(0,50):
            pygame.draw.rect(screen, [redVal*(255-(255/100)*(x+y)),greenVal*((255/50)*x),blueVal*((255/50)*y)],[x*10,y*10,10,10],0)

    pygame.display.update()
    clock.tick(60)
    mainWindow.update()
