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

if SIM:
    import pygame
    from matsim import MatrixSim
    matrix = MatrixSim(WIDTH, HEIGHT)
else:
    import hub75
    matrix = hub75.Hub75(WIDTH, HEIGHT)

def setup():
    global ani
    matrix.start()

    with open("ani.txt", "r") as file:
        for x in range(WIDTH):
            ani.append([])
            for y in range(HEIGHT):
                color = [int(c) for c in file.readline().strip().split(" ")]
                ani[x].append(color)

    for x in range(WIDTH):
        for y in range(HEIGHT):
            color = ani[x][y]
            matrix.set_rgb(x, y, color[0], color[1], color[2])


def loop():
    matrix.flip()
    pass

##############
# MAIN LOOP
##############

setup()
while True:
    loop()