import time, random, math
import json

################
#MATRIX VARS
################
SIM = False

#DIM OF MATRIX
WIDTH = 32
HEIGHT = 32

#
REFRESH = 20

# FILES
FURNACE_FILE = "furnace.txt"
FIRE_FILE = "fire.txt"

#
fireshape = []

firePalette = []
fireShape = []
fire = {}

br = 255
fireDir = 1
FIRE_INC = 255 / 5
REST = 1000

furnacePalette = []
furnace = {}

#list of frame dictionaries mapping pixels to colors
ani = []

#list of smoke objects: [position, color]
smoke = []
SMOKE_COLOR = (50, 50, 50)

#line in the ani file where pixel map begins
pixelStart = 0

#current line in ani file
currLine = 0

if SIM:
    import pygame
    from matsim import MatrixSim
    matrix = MatrixSim(WIDTH, HEIGHT)
else:
    import hub75
    matrix = hub75.Hub75(WIDTH, HEIGHT)

def generateSmoke():
    global smoke
    #dict of gray smoke pixels that quickly float upward
    #randomly generate a couple particles every couple frames

    if random.randint(0, 10) == 5:
        smoke.append([random.randint(5, 31), 16], SMOKE_COLOR)

def drawSmoke():
    global smoke
    #move smoke upwards and variably to the left and right by 1 pixel
    #delete from smoke dict once out of sight

    for s in smoke:
        matrix.set_rgb(s[0][0], s[0][1], 0, 0, 0)

        s[0][1] -= 2

        if s[0][1] > HEIGHT - 1 or s[0][1] < 0:
            smoke.remove(s)
        else:
            matrix.set_rgb(s[0][0], s[0][1], s[1][0], s[1][1], s[1][2])
    
def loadFurnace(filename):
    global furnace, furnacePalette
    
    currLine = 0
    with open(filename, "r") as file:
        lines = file.readlines()
        line = lines[currLine].strip()
        while line != "P":
            data = [int(i) for i in line.split(" ")]
            color = (data[0], data[1], data[2])
            furnacePalette.append(color)

            currLine += 1
            line = lines[currLine].strip()

        currLine += 1
        line = lines[currLine].strip()
        while line != "F":
            x = int(line)
            y = -1
            
            currLine += 1
            line = lines[currLine].strip()
            while line != "X":
                line = line.split(' ')
                y = int(line[0])
                c = furnacePalette[int(line[1])]

                #DEPR: store pixel
                # fkey = str(x) + " " + str(y)
                # furnace[fkey] = c

                #draw pixel
                matrix.set_rgb(x, y, c[0], c[1], c[2])

                #increment line
                currLine += 1
                line = lines[currLine].strip()

            currLine += 1
            line = lines[currLine].strip()

def drawFurnace():
    global furnace, furnacePalette

    if len(furnace) <= 0:
        return

    for pixel in furnace.keys():
        cindex = furnace[pixel]
        c = furnacePalette[cindex]
        x, y = pixel.strip().split(" ")
        matrix.set_rgb(x, y, c[0], c[1], c[2])
    
def loadFire(filename):
    global fire, fireShape, firePalette
    
    currLine = 0
    with open(filename, "r") as file:
        lines = file.readlines()
        line = lines[currLine].strip()
        while line != "P":
            # print(line)
            data = [int(i) for i in line.split(" ")]
            color = (data[0], data[1], data[2])
            firePalette.append(color)

            currLine += 1
            line = lines[currLine].strip()

        currLine += 1
        line = lines[currLine].strip()
        while line != "F":
            x = int(line)
            y = -1
            
            currLine += 1
            line = lines[currLine].strip()
            while line != "X":
                line = line.split(' ')
                y = int(line[0])
                c = int(line[1])

                #DEPR: store pixel
                fkey = str(x) + " " + str(y)
                fire[fkey] = c
                fireShape.append((x,y))


                #increment line
                currLine += 1
                line = lines[currLine].strip()

            currLine += 1
            line = lines[currLine].strip()

def compressFireShape():
    global fireShape

    fireIndex = 0
    compFireShape = []
    while fireIndex < len(fireShape):
        compFireShape.append(fireShape[fireIndex])
        (x, y) = fireShape[fireIndex]
        fireShape.remove((x+1, y))
        fireShape.remove((x, y+1))
        fireShape.remove((x+1, y+1))

        fireIndex += 1

    fireShape = compFireShape

def drawFire():
    global fire, firePalette, br, fireDir

    if len(fire) <= 0:
        return

    for pixel in fire.keys():
        cindex = fire[pixel]
        c = firePalette[cindex]
        x, y = pixel.strip().split(" ")
        bfactor = br / 255.0
        matrix.set_rgb(int(x), int(y), int(bfactor*c[0]), int(bfactor*c[1]), int(bfactor*c[2]))
        #matrix.set_rgb(int(x), int(y), int(c[0]), int(c[1]), int(c[2]))

    br += FIRE_INC * fireDir
    if br >= 255:
        br = 255
        fireDir *= -1
    elif br <= 0:
        br = 0
        fireDir *= -1

def generateFire():
    global fire, firePalette, br, fireDir

    if len(fire) <= 0:
        return

    for pixel in fireShape:
        cindex = random.randint(1, len(firePalette) - 1)
        c = firePalette[cindex]
        (x, y) = pixel
        bfactor = br / 255.0
        matrix.set_rgb(x, y, int(bfactor*c[0]), int(bfactor*c[1]), int(bfactor*c[2]))
        matrix.set_rgb(x + 1, y, int(bfactor*c[0]), int(bfactor*c[1]), int(bfactor*c[2]))
        matrix.set_rgb(x, y + 1, int(bfactor*c[0]), int(bfactor*c[1]), int(bfactor*c[2]))
        matrix.set_rgb(x + 1, y + 1, int(bfactor*c[0]), int(bfactor*c[1]), int(bfactor*c[2]))

    # br += FIRE_INC * fireDir
    # if br >= 255:
    #     br = 255
    #     fireDir *= -1
    # elif br <= 0:
    #     br = 0
    #     fireDir *= -1


def setup():
    global ani, currLine, pixelStart
    #loads color palette and frame count from file
    loadFurnace(FURNACE_FILE)
    loadFire(FIRE_FILE)
    compressFireShape()

def drawFrame(flines):
    global palette, frame, frameCount, currLine, pixelStart

    #reset animation
    if frame == 0:
        currLine = pixelStart

    line = flines[currLine].strip()
    while line != "F":
        x = int(line)
        y = -1
        
        currLine += 1
        line = flines[currLine].strip()
        while line != "X":
            line = line.split(' ')
            y = int(line[0])
            c = palette[int(line[1])]

            #draw pixel
            matrix.set_rgb(x, y, c[0], c[1], c[2])

            #increment line
            currLine += 1
            line = flines[currLine].strip()

        currLine += 1
        line = flines[currLine].strip()

    currLine += 1
    frame = (frame + 1) % frameCount




##############
# MAIN LOOP
##############
matrix.start()

setup()
while True:
    #apparent fire brightness is 0
    if br == FIRE_INC and fireDir == 1: 
        time.sleep(REST / 1000.0)

    if br == 255 - FIRE_INC and fireDir == -1: 
        time.sleep(REST / 1000.0 / 2)

    generateFire()
    matrix.flip()
    time.sleep(750 / 1000.0)