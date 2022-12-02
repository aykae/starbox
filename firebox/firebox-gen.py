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
REFRESH = 50

#
fireshape = []
fire = {}

logs = {}

#list of frame dictionaries mapping pixels to colors
ani = []

#
frame = 0
frameCount = 0

if SIM:
    import pygame
    from matsim import MatrixSim
    matrix = MatrixSim(WIDTH, HEIGHT)
else:
    import hub75
    matrix = hub75.Hub75(WIDTH, HEIGHT)

def genFireshape(filename):
    # fw = 16
    # fh = 16
    # fxoffset = (WIDTH - fw) // 2
    # fyoffset = (HEIGHT - fh) // 2 + 5
    # for x in range(fxoffset, fxoffset + fw):
    #     for y in range(fyoffset, fyoffset + fh):
    #         fireshape.append((x,y))
    with open(filename, "r") as file:
        for x in range(WIDTH):
            for y in range(HEIGHT):
                color = [int(c) for c in file.readline().strip().split(" ")]
                if sum(color) > 0:
                    #store position but not color
                    fireshape.append((x,y))

def genFire():
    fcolors = {
        # "WHITE": (255, 255, 255),
        "DARK_ORANGE": (230, 54, 19),
        "LIGHT_ORANGE": (237, 109, 25),
        "DARK_YELLOW": (248, 191, 34),
        "RED_ORANGE": (227, 27, 16)
    }

    for f in fireshape:
        fire[f] = random.choice(list(fcolors.values()))

def drawFire():
    global fire

    for k in fire.keys():
        color = fire[k]
        matrix.set_rgb(k[0], k[1], color[0], color[1], color[2])

def loadLogs(filename):
    with open(filename, "r") as file:
        #Extract img data
        for x in range(WIDTH):
            for y in range(HEIGHT):
                color = [int(c) for c in file.readline().strip().split(" ")]

                #soring black is redundant
                if sum(color) > 0:
                    logs[(x,y)] = color

def drawLogs():
    global logs

    for k in logs.keys():
        color = logs[k]
        matrix.set_rgb(k[0], k[1], color[0], color[1], color[2])

def loadFireFromAni(filename):
    global ani

    ani_index = 0
    with open(filename, "r") as file:
        line = file.readline().strip().split(' ')
        if line[0] == "FRAME":
            ani.append({})
            ani_index += 1
        else:
            px = line[0]
            py = line[1]
            r = line[2]
            g = line[3]
            b = line[4]

            ani[ani_index][(px, py)] = (r, g, b)

def drawFireFromAni():
    global ani, frame

    for f in ani:
        for p in f.keys():
            c = f[pixel]
            matrix.set_rgb(p[0], p[1], c[0], c[1], c[2])
            
        time.sleep(REFRESH / 1000.0)


def setup():
    global ani, frame, frameCount
    matrix.start()

    loadLogs("logs.txt")
    drawLogs()

    genFireshape("fireshape.txt")
    genFire()

def loop():
    global ani, frame, frameCount

    drawFire()
    drawLogs()
    matrix.flip()

    genFire()


##############
# MAIN LOOP
##############

setup()
while True:
    loop()