import random

SIM = False

WIDTH = 32
HEIGHT = 32

currColor = (0, 0, 0)

if SIM:
    import pygame
    from matsim import MatrixSim
    matrix = MatrixSim(WIDTH, HEIGHT)
else:
    import hub75
    matrix = hub75.Hub75(WIDTH, HEIGHT)

def draw():
    global currColor

    #c = currColor
    for y in range(HEIGHT):
        for x in range(WIDTH):
            c = random.randint(0, 255)
            #matrix.set_rgb(x, y, c[0], c[1], c[2])
            matrix.set_rgb(x, y, c, c, c)


def setup():
    #loads color palette and frame count from file
    pass

def loop():
    global currColor

    #newc = random.randint(0, 255)
    #currColor = (newc, newc, newc)
    draw()

##############
# MAIN LOOP
##############
matrix.start()
setup()
while True:
    loop()
    matrix.flip()