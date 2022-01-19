from ast import Starred
from operator import index
import tkinter as tk
import time
import threading
from PIL import Image
from PIL import ImageEnhance
from io import BytesIO
import requests
from urllib.request import Request, urlopen
import keyboard
import os
import random
from tkinter import filedialog
from math import sqrt
from pynput.mouse import Button, Controller, Listener
import pyautogui
from Colors import *
 

mouse = Controller()

drawingArea = (0, 0)
corner1 = (0, 0)
corner2 = (0, 0)
fileName = str()
stopDrawing = False
textbox = (0, 0)
stage = ""

def on_click(x, y, button, pressed):
    global drawingArea
    global corner1, corner2, textbox, stage
    if pressed:
        if stage == "Get Top Left":
            corner1 = mouse.position
        if stage == "Get Bottom Right":
            corner2 = mouse.position
            x = abs(corner1[0]-corner2[0])
            y = abs(corner1[0]-corner2[1])
            drawingArea = (x, y)
        if stage == "Get Textbox":
            textbox = mouse.position
    stage = ""

# ...or, in a non-blocking fashion:
listener = Listener(
    on_click=on_click)
listener.start()

def DotPlace():
    global stopDrawing
    stopDrawing = False
    img = 0
    pixelCount = 50
    drawingArea = (abs(corner1[0]-corner2[0]), abs(corner1[1]-corner2[1]))
    xAddAmount = drawingArea[0]/pixelCount
    yAddAmount = drawingArea[1]/pixelCount
    # response = requests.get("https://upload.wikimedia.org/wikipedia/commons/6/61/Black_Circle.jpg")
    # img = ImageEnhance.Sharpness(Image.open(
    #     BytesIO(response.content)).convert('RGBA')).image
    img = ImageEnhance.Sharpness(Image.open(fileName).convert('RGBA')).image
    img = img.resize((int(pixelCount),
                     int(pixelCount)))
    pix = img.load()
    xSize, ySize = img.size
    lastColor = ""
    time.sleep(1)
    for x in range(int(xSize)):
        for y in range(int(ySize)):
            if (pix[x ,y][3] == 0 ):
                continue
            closestRGBIndex = FindClosestRGB((pix[x, y][0], pix[x, y][1], pix[x, y][2]))
            closestRGB = allColors[closestRGBIndex]
            newColor = GetHexColorFromRGB(closestRGB.R, closestRGB.G, closestRGB.B)
            
            if(newColor == lastColor):
              time.sleep(0.1)
              mouse.position = (corner1[0] + xAddAmount * x, corner1[1] + yAddAmount * y)
            #   mouse.position = (corner1[0] + xAddAmount * x , corner1[1] + yAddAmount * y + 1)
            #   mouse.click(Button.left, 1)
            else:
              mouse.release(Button.left)
              time.sleep(0.6)
              SetText(newColor)
              lastColor = newColor
              mouse.position = (corner1[0] + xAddAmount * x, corner1[1] + yAddAmount * y)
              mouse.press(Button.left)
              

def GetHexColorFromRGB(r, g, b):
    hex = "{:02x}{:02x}{:02x}".format(r,g,b)
    return hex

def GetTextbox():
    global stage
    stage="Get Textbox"
def GetTopLeft():
    global stage
    stage="Get Top Left"
def GetBottomRight():
    global stage
    stage="Get Bottom Right"

def SetText(newColor):
    global textbox
    mouse.position = textbox
    time.sleep(0.5)
    mouse.click(Button.left, 2)
    time.sleep(0.5)
    pyautogui.typewrite(["delete"])
    time.sleep(0.5)
    pyautogui.typewrite(newColor)
    time.sleep(0.5)
    pyautogui.typewrite(["enter"])
def Start():
    global started
    started = True

def DrawImage():
    DotPlace()
    print("1", corner1)
    print("2", corner2)
    print("t", textbox)

def FindClosestRGB(rgb: tuple):
    values = list()
    for color in allColors:
        number = 0
        number += abs(rgb[0]-color.RGB[0])
        number += abs(rgb[1]-color.RGB[1])
        number += abs(rgb[2]-color.RGB[2])
        
        red = pow(rgb[0] - color.RGB[0],2)
        green = pow(rgb[1] - color.RGB[1],2)
        blue = pow(rgb[2] - color.RGB[2],2)
        number = sqrt(red+green+blue)
        values.append(number)

    index_min = min(range(len(values)), key=values.__getitem__)
    #print(allColors[index_min].name)
    return index_min

def Exit():
    global stopDrawing
    stopDrawing = True
    print("Exiting")
    os._exit(0)

def OpenFile():
    global fileName
    fileName = filedialog.askopenfilename(initialdir="", filetypes=[(
        "PNG", "*.png"), ("JPG", "*.jpg"), ("JPEG", "*.jpeg")])
    print(fileName)
    statusLabel.config(text=f"Loaded image")

root = tk.Tk()
root.configure(background="#FFF")
slowMode = tk.BooleanVar()
imageMode = tk.IntVar()
drawMode = tk.IntVar()
root.geometry("800x600")
root.title("Gartic Drawbot")
tk.Button(root, text="Open file", command=OpenFile).pack()
statusLabel = tk.Label(text="Hello!")
tk.Button(root, text="Set textbox position", command=GetTextbox).pack()
tk.Button(root, text="Set top left position", command=GetTopLeft).pack()
tk.Button(root, text="Set bottom right position", command=GetBottomRight).pack()
tk.Button(root, text="Draw Image", command=DrawImage).pack()

statusLabel.pack()
keyboard.add_hotkey("escape", Exit)
root.mainloop()
