import time, random, math

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
barrier = []

#
ball = [0, 0]
dball = [1, 1]

#
PADDLE_WIDTH = 2
PADDLE_HEIGHT = 6
PADDLE_SPEED = 1
lpaddle = []
rpaddle = []
ldir = 1
rdir = -1

if SIM:
    import pygame
    from matsim import MatrixSim
    matrix = MatrixSim(WIDTH, HEIGHT)
else:
    import hub75
    matrix = hub75.Hub75(WIDTH, HEIGHT)

################
#COLORS
################
COLOR_DICT = {
    "WHITE": (255, 255, 255),
    "GRAY": (50, 50, 50),
    "LIGHT_BLUE":(204, 224, 255),
    #"CYAN2": (150, 204, 255),
    "LIGHT_PURPLE": (201, 170, 242),
    "MID_PURPLE": (170, 127, 225),
    #"YELLOW": (255, 254, 166)
}

def setup():
    global barrier, lpaddle, rpaddle
    
    matrix.start()

    if WIDTH % 2 == 0:
        barrier.append(WIDTH // 2 - 1) 
        #barrier.append(WIDTH // 2)
    else:
        barrier.append(WIDTH // 2)

    lpaddle = [2, HEIGHT // 2 - (PADDLE_HEIGHT // 2)]
    rpaddle = [WIDTH-1-PADDLE_WIDTH-2, HEIGHT // 2 - (PADDLE_HEIGHT // 2)]

def set_pixel(x, y, r, g, b):
    #matrix.set_rgb(WIDTH - 1 - x, y, r, g, b)
    matrix.set_rgb(x, y, r, g, b)

def drawBarrier():
    global barrier

    color = COLOR_DICT["GRAY"]
    for y in range(HEIGHT):
        for b in barrier:
            set_pixel(b, y, color[0], color[1], color[2])

def drawBall():
    global ball, dball

    ball[0] += dball[0]
    ball[1] += dball[1]
    
    if ball[0] >= WIDTH - 1:
        ball[0] = WIDTH - 1;
        dball[0] *= -1
    elif ball[0] <= 0:
        ball[0] = 0
        dball[0] *= -1
    elif dball[0] < 0 and ball[0] == lpaddle[0] + PADDLE_WIDTH:
        if ball[1] >= lpaddle[1] and ball[1] <= lpaddle[1] + PADDLE_HEIGHT:
            dball[0] *= -1
    elif dball[0] > 0 and ball[0] == rpaddle[0]:
        if ball[1] >= rpaddle[1] and ball[1] <= rpaddle[1] + PADDLE_HEIGHT:
            dball[0] *= -1


    if ball[1] >= HEIGHT - 1:
        ball[1] = HEIGHT - 1
        dball[1] *= -1
    elif ball[1] <= 0:
        ball[1] = 0
        dball[1] *= -1

    

    color = COLOR_DICT["WHITE"] 
    set_pixel(ball[0], ball[1], color[0], color[1], color[2])

def drawPaddles():
    global lpaddle, rpaddle, ldir, rdir, ball, dball

    lpaddle[1] += ldir * PADDLE_SPEED
    rpaddle[1] += rdir * PADDLE_SPEED

    if lpaddle[1] + PADDLE_HEIGHT >= HEIGHT - 1:
        lpaddle[1] = HEIGHT - 1 - PADDLE_HEIGHT
        ldir *= -1
    elif lpaddle[1] <= 0: 
        lpaddle[1] = 0
        ldir *= -1

    if rpaddle[1] + PADDLE_HEIGHT >= HEIGHT - 1:
        rpaddle[1] = HEIGHT - 1 - PADDLE_HEIGHT
        rdir *= -1
    elif rpaddle[1] <= 0: 
        rpaddle[1] = 0
        rdir *= -1

    color = COLOR_DICT["WHITE"] 

    for y in range(lpaddle[1], lpaddle[1] + PADDLE_HEIGHT):
        for x in range(lpaddle[0], lpaddle[0] + PADDLE_WIDTH):
            set_pixel(x, y, 0, 255, 0)
            #set_pixel(x, y, color[0], color[1], color[2])

    for y in range(rpaddle[1], rpaddle[1] + PADDLE_HEIGHT):
        for x in range(rpaddle[0], rpaddle[0] + PADDLE_WIDTH):
            set_pixel(x, y, 0, 0, 255)
            #set_pixel(x, y, color[0], color[1], color[2])

def loop():
    matrix.clear()
    #drawBarrier()
    drawBall()
    drawPaddles()
    matrix.flip()

##############
# MAIN LOOP
##############

setup()
while True:
    loop()
    # set_pixel(5, 5, 255, 0, 0)
    # set_pixel(5, 10, 0, 255, 0)
    # set_pixel(10, 5, 0, 0, 255)
    # matrix.flip()
    time.sleep(REFRESH / 1000.0)

    if SIM:
        time.sleep(5 / 1000.0) #delay to better simulate screen fps
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
