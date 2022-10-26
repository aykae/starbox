import time, random, math

################
#MATRIX VARS
################
SIM = False

#DIM OF MATRIX
WIDTH = 32
HEIGHT = 32

#DIM OF STAR DISPLAY
STARWIDTH = 28
STARHEIGHT = 28
XPADDING = (WIDTH - STARWIDTH) // 2
YPADDING = (HEIGHT - STARHEIGHT) // 2

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
    "LIGHT_BLUE":(204, 224, 255),
    #"CYAN2": (150, 204, 255),
    "LIGHT_PURPLE": (201, 170, 242),
    "MID_PURPLE": (170, 127, 225),
    #"YELLOW": (255, 254, 166)
}

################
#CONSTELLATIONS
################

################
#STAR VARS
################
MAX_BRIGHTNESS = 255
MIN_FLICKER = 20 
MAX_FLICKER = 25
MAX_STARS = 50 
SPEED = 5
REFRESH = 0

starCount = 0
starsBuffer = {}
stars = {}
prevStarTime = 0

starDelay = 0
starsLevel = 0

starsLevelPeak = 0
peakStartTime = 0
shineDelay = 10

dx = 2
dy = -1

isFirstStars = True
isPeaking = False
isDimming = False
isShining = False
isShooting = False

################
#SHOOTING STAR VARS
################
SH_FADE_SPEED = 10
SH_DELAY_HIGH = 8
SH_DELAY_LOW = SH_DELAY_HIGH // 2
SH_ODDS = 0.1
shStarTrail = {}
shStarData = {}
prevShStarTime = time.time_ns()
shStarDelay = (10**9) * random.randint(SH_DELAY_LOW, SH_DELAY_HIGH)

shStarColor = COLOR_DICT["LIGHT_BLUE"]


######################################

def overlapFadeSetup():
    global stars, starsBuffer, starsLevel, isFirstStars, isPeaking, isDimming, isShining
    matrix.start()

    isFirstStars = True
    starsLevel = 0

    genStars()
    stars = starsBuffer
    starsBuffer = {}

def overlapFadeStarLoop():
    global starCount, stars, starsBuffer, starsLevel, starsLevelPeak, shStarTrail
    global isFirstStars, isPeaking, isShining, isDimming, isShooting
    global peakStartTime

    #Edge case for drawing first group of stars
    if isFirstStars:
        if starsLevel <= 255:
            isShining = True
            for star in stars.keys():
                fadeFactor = stars[star]["fadeFactor"]
                #
                #currColor = stars[star]["currColor"]
                #fadeFactor = bezierFade(currColor)

                stars[star]["currColor"][0] = maximin(math.floor(starsLevel * fadeFactor[0]))
                stars[star]["currColor"][1] = maximin(math.floor(starsLevel * fadeFactor[1]))
                stars[star]["currColor"][2] = maximin(math.floor(starsLevel * fadeFactor[2]))

            starsLevel += SPEED
        else:
            #starsLevel reached max brightness
            starsLevel = 255
            starsLevelPeak = 255
            isFirstStars = False
            isPeaking = True
            isShooting = False
            peakStartTime = time.time_ns()

    if isPeaking:
        if time.time_ns() - peakStartTime >= (10**9) * shineDelay:
            isPeaking = False
            isDimming = True

            #potentially include this line v within genStars()
            starCount = 0
            genStars()
        else:
            #flicker
            numStars = len(stars)
            keys = list(stars.keys())

            #for i in range(1):
            randStar = keys[random.randint(0, numStars-1)]
            currColor = stars[randStar]["currColor"]
            fadeFactor = stars[randStar]["fadeFactor"]
            flickerFactor = sum(fadeFactor) * 255 / 3
            flickerFactor = random.randint(20, 30)

            dir = stars[randStar]["flickerDir"]
            # limit stars affected
            if dir == 1:
                ff = flickerFactor
            elif dir == -1:
                ff = -flickerFactor
            else:
                ff = 0

            stars[randStar]["currColor"][0] = maximin(math.floor(ff + currColor[0]))
            stars[randStar]["currColor"][1] = maximin(math.floor(ff + currColor[1]))
            stars[randStar]["currColor"][2] = maximin(math.floor(ff + currColor[2]))

            stars[randStar]["flickerDir"] = -dir


        overlapShStarLoop()
    
    if isDimming:
        if starsLevel >= 0:
            for star in stars.keys():
                fadeFactor = stars[star]["fadeFactor"]

                stars[star]["currColor"][0] = maximin(math.floor(starsLevel * fadeFactor[0]))
                stars[star]["currColor"][1] = maximin(math.floor(starsLevel * fadeFactor[1]))
                stars[star]["currColor"][2] = maximin(math.floor(starsLevel * fadeFactor[2]))

            for star in starsBuffer.keys():
                invStarsLevel = max(0, min(MAX_BRIGHTNESS, starsLevelPeak - starsLevel))
                fadeFactor = starsBuffer[star]["fadeFactor"]

                starsBuffer[star]["currColor"][0] = maximin(math.floor(invStarsLevel * fadeFactor[0]))
                starsBuffer[star]["currColor"][1] = maximin(math.floor(invStarsLevel * fadeFactor[1]))
                starsBuffer[star]["currColor"][2] = maximin(math.floor(invStarsLevel * fadeFactor[2]))

            starsLevel -= SPEED
        else:
            isDimming = False
            isPeaking = True
            peakStartTime = time.time_ns()
            if random.random() < SH_ODDS:
                isShooting = True

            starsLevel = 255

            stars = starsBuffer
            starsBuffer = {}

    overlapFadeDrawStars()

def bezierFade(color):

    r = color[0] / 255.0
    b = color[1] / 255.0
    g = color[2] / 255.0

    rSq = r ** 2
    rPara = rSq / (2.0 * (rSq - r) + 1.0)

    rPara = 2.0 * r * (1.0 - r)


    bSq = b ** 2
    bPara = 2.0 * b * (1.0 - b)

    gSq = g ** 2
    gPara = 2.0 * g * (1.0 - g)
    
    return (rPara, bPara, gPara)

def overlapShStarLoop():
    global shStarDelay, shStarData, shStarTrail, shStarColor, isShining, isShooting, peakStartTime

    if len(shStarTrail) == 0 and isPeaking and isShooting and (time.time_ns() - peakStartTime > (10**9) * 1):
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

    #compute shooting star trail
    if len(shStarTrail) > 0:
        drawShStars()

        if SIM:
            keys = list(shStarTrail.keys())
        else:
            keys = shStarTrail.keys()

        for t in keys:
            tColor = shStarTrail[t]
            if tColor == (0, 0, 0):
                shStarTrail.pop(t)
            else:
                shStarTrail[t] = (max(0, tColor[0] - SH_FADE_SPEED), max(0, tColor[1] - SH_FADE_SPEED), max(0, tColor[2] - SH_FADE_SPEED))

        head = shStarData['head']
        dx = shStarData['dx']
        slope = shStarData['slope']
        newHead = (head[0] + dx, head[1] + slope)
        if (newHead[0] >= 0) and (newHead[0] < WIDTH) and (newHead[1] >= 0) and (newHead[1] < HEIGHT): #head trailed off screen
            shStarData['head'] = newHead
            shStarTrail[newHead] = shStarColor

        isShooting = False
    else:
        shStarData = {}
        shStarTrail = {}

def overlapFadeDrawStars():
    #draw brightening stars
    for star in stars.keys():
        starColor = stars[star]["currColor"]
        matrix.set_rgb(star[0], star[1], starColor[0], starColor[1], starColor[2])

    #draw dimming stars
    for star in starsBuffer.keys():
        starColor = starsBuffer[star]["currColor"]
        matrix.set_rgb(star[0], star[1], starColor[0], starColor[1], starColor[2])

    #draw shooting stars
    for sh in shStarTrail.keys():
        starColor = shStarTrail[sh]
        matrix.set_rgb(sh[0], sh[1], starColor[0], starColor[1], starColor[2])

    matrix.flip()

def drawShStars():
    for sh in shStarTrail.keys():
        starColor = shStarTrail[sh]
        matrix.set_rgb(sh[0], sh[1], starColor[0], starColor[1], starColor[2])

    matrix.flip()

def constellationLoop():
    pass

def clearStars():
    global starCount, starsBuffer, stars, starsLevel, isPeaking, isDimming

    starCount = 0
    starsLevel = 0
    isDimming = False

def checkForAdjacent(nextStar):
    global stars

    keys = stars.keys()
    nsX = nextStar[0]
    nsY = nextStar[1]
    
    if (nsX, nsY) in keys:
        return True
    elif (nsX + 1, nsY) in keys:
        return True
    elif (nsX - 1, nsY) in keys:
        return True
    elif (nsX, nsY + 1) in keys:
        return True
    elif (nsX, nsY - 1) in keys:
        return True

    return False

def genStars():
    global starCount, starsBuffer, stars

    while starCount < MAX_STARS:
        nextStar = (random.randint(XPADDING, XPADDING + STARWIDTH - 1), random.randint(YPADDING, YPADDING + STARHEIGHT - 1))
        hasAdjacent = checkForAdjacent(nextStar)
        if not hasAdjacent:

            randBrightness = weightedRandom(
                [10, 20, 60, 80, 100, 150, 255],
                [10, 8, 5, 4, 3, 2, 5]
            ) / 255.0

            #randInd = random.randint(0, len(COLOR_DICT) - 1)
            randInd = weightedRandom(
                [0, 1, 2, 3],
                [3, 1, 1, 2]
            )
            baseColor = list(COLOR_DICT.values())[randInd]
            targetColor = tuple([int(randBrightness * i) for i in baseColor])
            fadeFactor = (targetColor[0] / 255.0, targetColor[1] / 255.0, targetColor[2] / 255.0)

            colorSum = sum(targetColor)
            fdir = random.choice([-1, 1]) if colorSum > 250 else 0


            starsBuffer[nextStar] = {
                "state": 1, #0 -> inactive, 1 -> brightening, 2 -> peaking, -1 -> dimming
                "currColor": [0, 0, 0], # rgb 
                "targetColor": targetColor, #rgb
                "fadeFactor": fadeFactor, #float for incrementing stars proportionally
                "dimDelay": 0, # int, nanoseconds
                "flickerDir": fdir, # -1 or 1; direction of flicker
            }

            starCount += 1

def maximin(val):
    return max(0, min(MAX_BRIGHTNESS, val))

def weightedRandom(vals, weights):
    arr = []
    if len(vals) != len(weights):
        print("must be weight for each element in list")
        return
    for i in range(len(vals)):
        for _ in range(weights[i]):
            arr.append(vals[i])

    #random.shuffle(arr)
    return random.choice(arr)

##############
# MAIN LOOP
##############

overlapFadeSetup()
while True:
    overlapFadeStarLoop()
    time.sleep(REFRESH / 1000.0)

    if SIM:
        time.sleep(5 / 1000.0) #delay to better simulate screen fps
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
