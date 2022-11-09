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
REFRESH = 25

#
SPARKLING = True
SCOUNT = 20
scolors = []
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
            matrix.set_rgb(x, y, color[0], color[1], color[2])

def drawSparkles(colors):
    for i in range(SCOUNT):
        x = random.randint(0, WIDTH-1)
        y = random.randint(0, HEIGHT-1)

        c = random.choice(colors)

        if sum(img[x][y]) <= 3:
            matrix.set_rgb(x, y, c[0], c[1], c[2])



def setup():
    global img, filename, scolors
    matrix.start()
    loadImg("img.txt")
    drawImg()

    #scolors = [(80,80,80), (52,76,80)]
    scolors = [(255,255,255), (52,76,80)]

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