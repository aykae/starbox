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
REFRESH = 30

#
BG = (0, 0, 0)

SPARKLING = True
SCOUNT = 20
scolors = []
sparkles = {}
#
filename = ""

#
img = []
frame = 0
frameCount = 0

if SIM:
    import pygame
    from matsim import MatrixSim
    matrix = MatrixSim(WIDTH, HEIGHT)
else:
    import hub75
    matrix = hub75.Hub75(WIDTH, HEIGHT)

def loadImg(f):
    global img
    filename = f

    with open(filename, "r") as file:
        for x in range(WIDTH):
            img.append([])
            for _ in range(HEIGHT):
                color = [int(c) for c in file.readline().strip().split(" ")]
                img[x].append(color)
def drawImg():
    for x in range(WIDTH):
        for y in range(HEIGHT):
            color = img[x][y]
            if color != (0, 0, 0):
                matrix.set_rgb(x, y, color[0], color[1], color[2])

def drawSparkles(colors):
    for s in sparkles.keys():
        matrix.set_rgb(s[0], s[1], BG[0], BG[1], BG[2])
        sparkles.pop(s)

    print(sparkles)

    for _ in range(SCOUNT):
        x = random.randint(0, WIDTH-1)
        y = random.randint(0, HEIGHT-1)

        c = random.choice(colors)

        print(img[x][y])
        print(BG)
        #if img[x][y] == BG and (x,y) not in sparkles.keys():
        if img[x][y] == BG:
            matrix.set_rgb(x, y, c[0], c[1], c[2])
            img[x][y] = c
            sparkles[(x,y)] = c

    print(sparkles)
    print()

def setup():
    global img, filename, scolors
    matrix.start()
    loadImg("img.txt")
    drawImg()

    scolors = [(255,255,255), (52,76,80)]

    matrix.flip()


def loop():
    global ani, frame, frameCount, scolors
    drawImg()
    drawSparkles(scolors)
    matrix.flip()

    time.sleep(REFRESH / 1000)


##############
# MAIN LOOP
##############

setup()
while True:
    loop()