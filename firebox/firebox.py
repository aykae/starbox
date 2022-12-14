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

#
fireshape = []
fire = {}

logs = {}

#list of frame dictionaries mapping pixels to colors
ani = []
palette = {}

#list of smoke objects: [position, color]
smoke = []
SMOKE_COLOR = (50, 50, 50)

#line in the ani file where pixel map begins
pixelStart = 0

#current line in ani file
currLine = 0

#frames
frame = 0
frameCount = 0

if SIM:
    import pygame
    from matsim import MatrixSim
    matrix = MatrixSim(WIDTH, HEIGHT)
else:
    import hub75
    matrix = hub75.Hub75(WIDTH, HEIGHT)


def loadLogs(filename):
    with open(filename, "r") as file:
        #Extract img data
        for x in range(WIDTH):
            for y in range(HEIGHT):
                color = [int(c) for c in file.readline().strip().split(" ")]

                #storing black is redundant
                if sum(color) > 0:
                    logs[(x,y)] = color

def drawLogs():
    global logs

    for k in logs.keys():
        color = logs[k]
        matrix.set_rgb(k[0], k[1], color[0], color[1], color[2])

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
    
def loadAniData(flines):
    global palette, frameCount, currLine, pixelStart
    pixelStart = 0
    frameCount = 0

    frameCount = int(flines[0].strip().split(" ")[0])
    currLine = 1

    for line in flines[1:]:
        currLine += 1
        if line.strip() == "P":
            pixelStart = currLine
            break
        elif pixelStart <= 0: #still reading palette
            data = [int(i) for i in line.strip().split(" ")]
            color = (data[0], data[1], data[2])
            cindex = data[3]
            palette[cindex] = color


def setup(flines):
    global ani, frame, frameCount, currLine, pixelStart
    #loads color palette and frame count from file
    loadAniData(flines)
    frame = 0

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

lines = []
with open("ani.txt") as file:
    lines = file.readlines()

# loglines = []
# with open("logs.txt") as file:
#     loglines = file.readlines()

loadLogs("logs.txt")
setup(lines)
while True:
    drawFrame(lines)
    drawLogs()
    matrix.flip()
    #time.sleep(REFRESH / 1000.0)