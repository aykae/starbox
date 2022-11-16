import time, random, math
import json

################
#MATRIX VARS
################
SIM = False

#DIM OF MATRIX
WIDTH = 32
HEIGHT = 32
BORDER = 2

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
    global img, scolors
    filename = f

    with open(filename, "r") as file:
        #Extract Two Sparkle Colors
        sc1 = [int(c) for c in file.readline().strip().split(" ")]
        sc2 = [int(c) for c in file.readline().strip().split(" ")]
        scolors = [sc1, sc2]

        #Extract Img Data
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

    for _ in range(SCOUNT):
        x = random.randint(BORDER, WIDTH-1-BORDER)
        y = random.randint(BORDER, HEIGHT-1-BORDER)

        c = random.choice(colors)

        if sum(img[x][y]) == 0 and (x,y) not in sparkles.keys():
            matrix.set_rgb(x, y, c[0], c[1], c[2])
            sparkles[(x,y)] = c

def setup():
    global img, filename
    matrix.start()
    loadImg("img.txt")
    drawImg()

    matrix.flip()


def loop():
    global ani, frame, frameCount, scolors

    matrix.clear()
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