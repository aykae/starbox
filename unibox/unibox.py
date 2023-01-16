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
LOGO_FILE = "logo.txt"

#
palette = []

br = 0
fireDir = 1
FIRE_INC = 255 / 5

LIT_REST = 2000
DIM_REST = 1000

palette = []
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

def loadLogo(filename):
    global palette
    
    currLine = 0
    with open(filename, "r") as file:
        lines = file.readlines()
        line = lines[currLine].strip()
        while line != "P":
            data = [int(i) for i in line.split(" ")]
            color = (data[0], data[1], data[2])
            palette.append(color)

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
                c = palette[int(line[1])]

                #draw pixel
                matrix.set_rgb(x, y, c[0], c[1], c[2])

                #increment line
                currLine += 1
                line = lines[currLine].strip()

            currLine += 1
            line = lines[currLine].strip()

def drawLogo():
    global palette

    if len(furnace) <= 0:
        return

    for pixel in furnace.keys():
        cindex = furnace[pixel]
        c = palette[cindex]
        x, y = pixel.strip().split(" ")
        matrix.set_rgb(x, y, c[0], c[1], c[2])
    
def weightedRandom(weights):
    arr = []
    for wi in range(len(weights)):
        for _ in range(weights[wi]):
            arr.append(wi)
    
    return arr[random.randint(0, len(arr) - 1)]

def setup():
    global ani, currLine, pixelStart
    #loads color palette and frame count from file
    loadLogo(LOGO_FILE)

def loop():
    drawLogo()

##############
# MAIN LOOP
##############
matrix.start()
setup()
while True:
    loop()
    matrix.flip()