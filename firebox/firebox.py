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
palette = {}

#list of smoke objects: [position, color]
smoke = []
SMOKE_COLOR = (50, 50, 50)

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
    
def loadAniData(filename):
    global palette, frameCount

    frameCount = 0

    with open(filename, "r") as file:
        for line in file.readlines():
            if line.strip() == "P":
                break
            else:
                data = [int(i) for i in line.strip().split(" ")]
                color = (data[0], data[1], data[2])
                palette[color] = data[3]

        for line in file.readlines():
            if line.strip() == "F":
                frameCount += 1




def loadFireFromAni(filename):
    global ani

    ani.append({})
    ani_index = 0
    with open(filename, "r") as file:
        for line in file.readlines():
            print(ani_index)
            line = line.strip().split(' ')
            if line[0] == "-1":
                ani.append({})
                ani_index += 1
            else:
                px = line[0]
                py = line[1]
                r = line[2]
                g = line[3]
                b = line[4]

                ani[ani_index][(px, py)] = (r, g, b)

def drawFireFromAni(filename):
    global ani, frame

    with open(filename, "r") as file:
        pass

    matrix.set_rgb(int(p[0]), int(p[1]), int(c[0]), int(c[1]), int(c[2]))
            
def setup():
    global ani, frame, frameCount
    matrix.start()

    #loads color palette and frame count from file
    loadAniData("ani.txt")

    frame = 0

def loop():
    global ani, frame, frameCount

    drawFireFromAni()
    matrix.flip()
    #time.sleep(REFRESH / 1000.0)

    frame = (frame + 1) % frameCount

##############
# MAIN LOOP
##############

setup()
while True:
    loop()