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
ani = []
frame = 0
frameCount = 0

if SIM:
    import pygame
    from matsim import MatrixSim
    matrix = MatrixSim(WIDTH, HEIGHT)
else:
    import hub75
    matrix = hub75.Hub75(WIDTH, HEIGHT)

def setup():
    global ani, frame, frameCount
    matrix.start()

    with open("ani.txt", "r") as file:
        #frameCount = int(file.readline().strip())
        frameCount = 2

        for _ in range(frameCount):
        #for _ in range(1):
            for x in range(WIDTH):
                ani.append([])
                for y in range(HEIGHT):
                    color = [int(c) for c in file.readline().strip().split(" ")]
                    ani[x].append(color)

    for x in range(WIDTH):
        for y in range(HEIGHT):
            color = ani[x][y]
            matrix.set_rgb(x, y, color[0], color[1], color[2])

    frame = (frame + 1) % frameCount


def loop():
    global ani, frame, frameCount
    matrix.flip()

    xOffset = frame * WIDTH
    #xOffset = 0
    for x in range(WIDTH):
        for y in range(HEIGHT):
            color = ani[xOffset + x][y]
            matrix.set_rgb(x, y, color[0], color[1], color[2])

    frame = (frame + 1) % frameCount

##############
# MAIN LOOP
##############

setup()
while True:
    loop()