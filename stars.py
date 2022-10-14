import time, random

################
#MATRIX VARS
################
SIM = True

WIDTH = 32
HEIGHT = 32

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
WHITE = (255, 255, 255)
LIGHT_BLUE = (204, 224, 255)
LIGHT_PURPLE = (201, 170, 242)

################
#STAR VARS
################
MAX_BRIGHTNESS = 255
MIN_FLICKER = 20 
MAX_FLICKER = 25
MAX_STARS = 500
SPEED = 1

starCount = 0
stars = {}
prevStarTime = 0
starDelay = 0

################
#SHOOTING STAR VARS
################
SS_FADE_SPEED = 10
SH_DELAY_HIGH = 30
SH_DELAY_LOW = SH_DELAY_HIGH // 2

shStarTrail = {}
shStarData = {}
prevShStarTime = time.time_ns()
shStarDelay = (10**9) * random.randint(SH_DELAY_LOW, SH_DELAY_HIGH)

shStarColor = LIGHT_BLUE

######################################

def setup():
    global prevShStarTime

    matrix.start()


def starLoop():
    global starCount, stars, prevStarTime, prevStarCount, starDelay

    #SELECT RANDOM STAR
    if starCount < MAX_STARS:
        prevStarCount = starCount
        if (time.time_ns() - prevStarTime) >= starDelay:
            while starCount == prevStarCount: #while new star not yet added
                nextStar = (random.randint(0, WIDTH-1), random.randint(0, HEIGHT-1))
                hasAdjacent = checkForAdjacent(nextStar)
                if nextStar not in stars.keys() and (time.time_ns() - prevStarTime) >= starDelay and not hasAdjacent:
                    prevStarTime = time.time_ns()
                    starDelay = (10**9) * random.randint(0, 1)

                    # [starState, dimLevel, dimDelay, flickerDir]
                        # starState: 0 -> inactive, 1 -> brightening, 2 -> peaking, -1 -> dimming
                        # color: (0 -> 255, 0 -> 255, 0 -> 255) (color value)
                        # dimDelay: float of a time at which to begin the dimming process
                        # flickerDir: direction of flicker, either -1 or 1
                    stars[nextStar] = [1, (0, 0, 0), 0, -1] 
                    starCount += 1

    #INCREMENT STAR BRIGHTNESS ACCORDING TO DIRECTION
    for star in list(stars.keys()): #added list for python3.7 compat
        if stars[star][0] == 1: #brightenining
            if stars[star][1][0] == MAX_BRIGHTNESS:
                stars[star][0] = 2
                dimDelay = (10**9) * random.randint(3, 6)
                stars[star][2] = time.time_ns() + dimDelay #assign dim delay
            else:
                whiteVal = min(stars[star][1][0] + SPEED, MAX_BRIGHTNESS) #brighten star
                stars[star][1] = (whiteVal, whiteVal, whiteVal)
        elif stars[star][0] == -1: #dimming
            if stars[star][1][0] == 0:
                stars.pop(star) #remove star from active dict
                starCount -= 1
            else:
                whiteVal = max(stars[star][1][0] - SPEED, 0) #dim star
                stars[star][1] = (whiteVal, whiteVal, whiteVal)
        elif stars[star][0] == 2: #shining (static)
            if time.time_ns() > stars[star][2]: #begin dimming
                stars[star][2] = 0
                stars[star][0] = -1
            else: #flicker
                #flickerVal = random.randint(0, MAX_FLICKER)
                flickerVal = 0
                flickerDir = stars[star][3]
                flickerDir = 0 #PREVENT FLICKER
                if flickerDir == 1:
                    stars[star][1] = min(MAX_BRIGHTNESS, stars[star][1] + flickerVal)
                    stars[star][3] = -1
                if flickerDir == -1:
                    stars[star][1] = max(0, stars[star][1] - flickerVal)
                    stars[star][3] = 1

    drawStars()

def drawStars():
    for star in stars.keys():
        starColor = stars[star][1]
        matrix.set_rgb(star[0], star[1], starColor[0], starColor[1], starColor[2])

    matrix.flip()

def shStarLoop():
    global prevShStarTime, shStarDelay, shStarData, shStarTrail, shStarColor

    if len(shStarTrail) == 0 and (time.time_ns() - prevShStarTime) >= shStarDelay:
        edge = random.randint(0, 4) #top, right, bot, left
        xStart = yStart = -1
        slope = dx = 0

        if edge == 0:
            xStart = random.randint((WIDTH-1)//2, WIDTH-1)
            yStart = 0
            slope = 1
            dx = -1
        elif edge == 1:
            xStart = WIDTH - 1
            yStart = random.randint((HEIGHT-1)//2, HEIGHT-1)
            slope = -1
            dx = -1
        elif edge == 2:
            xStart = random.randint(0, (WIDTH-1)//2)
            yStart = HEIGHT - 1
            slope = -1
            dx = 1
        elif edge == 3:
            xStart = 0
            yStart = random.randint(0, (HEIGHT-1)//2)
            slope = 1 
            dx = 1

        shStarData['head'] = (xStart, yStart)
        shStarData['slope'] = slope
        shStarData['dx'] = dx

        shStarTrail[shStarData['head']] = shStarColor

        prevShStarTime = time.time_ns()
        shStarDelay = (10**9) * random.randint(SH_DELAY_LOW, SH_DELAY_HIGH)

    #compute shooting star trail
    if len(shStarTrail) > 0:
        drawShStars()

        for t in list(shStarTrail.keys()):
            tColor = shStarTrail[t]
            if tColor == (0, 0, 0):
                shStarTrail.pop(t)
            else:
                shStarTrail[t] = (max(0, tColor[0] - SS_FADE_SPEED), max(0, tColor[1] - SS_FADE_SPEED), max(0, tColor[2] - SS_FADE_SPEED))

        head = shStarData['head']
        dx = shStarData['dx']
        slope = shStarData['slope']
        newHead = (head[0] + dx, head[1] + slope)
        if (newHead[0] >= 0) and (newHead[0] < WIDTH) and (newHead[1] >= 0) and (newHead[1] < HEIGHT): #head trailed off screen
            shStarData['head'] = newHead
            shStarTrail[newHead] = shStarColor
    else:
        shStarData = {}
        shStarTrail = {}




def drawShStars():
    for sh in shStarTrail.keys():
        starColor = shStarTrail[sh]
        matrix.set_rgb(sh[0], sh[1], starColor[0], starColor[1], starColor[2])

    matrix.flip()
        




def checkForAdjacent(nextStar):
    global stars

    keys = stars.keys()
    nsX = nextStar[0]
    nsY = nextStar[1]

    if (nsX + 1, nsY) in keys:
        return True
    elif (nsX - 1, nsY) in keys:
        return True
    elif (nsX, nsY + 1) in keys:
        return True
    elif (nsX, nsY - 1) in keys:
        return True

    return False


##############
# MAIN LOOP
##############

setup()
while True:
    starLoop()
    shStarLoop()

    if SIM:
        #time.sleep(10 / 1000.0) #delay to better simulate screen fps
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
