import time, random, math

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
FORE_FILE = "furnace.txt"
BACK_FILE = "fire.txt"

#
fireshape = []

firePalette = []
fireShape = []
fire = {}

br = 0
fireDir = 1
FIRE_INC = 255 / 5

LIT_REST = 2000
DIM_REST = 1000

furnacePalette = []
furnace = {}

#list of frame dictionaries mapping pixels to colors
ani = []

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
        #cindex = random.randint(1, len(firePalette) - 1)
        cindex = weightedRandom([3, 5, 0, 2]) + 1
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


def weightedRandom(weights):
    arr = []
    for wi in range(len(weights)):
        for _ in range(weights[wi]):
            arr.append(wi)
    
    return arr[random.randint(0, len(arr) - 1)]

def setup():
    global ani, currLine, pixelStart
    #loads color palette and frame count from file
    loadFurnace(FURNACE_FILE)
    loadFire(FIRE_FILE)
    compressFireShape()

##############
# MAIN LOOP
##############
matrix.start()

setup()
while True:
    #apparent fire brightness is 0
    if br == FIRE_INC and fireDir == 1: 
        time.sleep(DIM_REST / 1000.0)

    if br == 255 - FIRE_INC and fireDir == -1: 
        time.sleep(LIT_REST / 1000.0)

    drawFire()
    matrix.flip()