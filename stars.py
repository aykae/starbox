import time, random, math

################
#MATRIX VARS
################
SIM = False

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
COLOR_DICT = {
    "WHITE": (255, 255, 255),
    "WHITE2": (255, 255, 255),
    "WHITE3": (255, 255, 255), #extra whites for higher chance of random selection
    "LIGHT_BLUE":(204, 224, 255),
    #"CYAN2": (150, 204, 255),
    "LIGHT_PURPLE": (201, 170, 242),
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
SPEED = 10
REFRESH = 0

starCount = 0
starsBuffer = {}
stars = {}
prevStarTime = 0
starDelay = 0
starsLevel = 0
starsLevelPeak = 0
shineDelay = 2500

dx = 2
dy = -1

haveStarsPeaked = False
haveStarsDimmed = False
readyToShine = False

################
#SHOOTING STAR VARS
################
SS_FADE_SPEED = 10
SH_DELAY_HIGH = 8
SH_DELAY_LOW = SH_DELAY_HIGH // 2

shStarTrail = {}
shStarData = {}
prevShStarTime = time.time_ns()
shStarDelay = (10**9) * random.randint(SH_DELAY_LOW, SH_DELAY_HIGH)

shStarColor = COLOR_DICT["LIGHT_BLUE"]


######################################

def fadeSetup():
    global stars, starsBuffer
    matrix.start()

    genStars()
    stars = starsBuffer
    starsBuffer = {}

def overlapFadeSetup():
    global stars, starsBuffer, starsLevel, haveStarsPeaked, haveStarsDimmed, readyToShine
    matrix.start()

    starsLevel = 0
    # haveStarsPeaked = False
    # haveStarsDimmed = False
    # readyToShine = False

    genStars()
    stars = starsBuffer
    starsBuffer = {}

def scrollSetup():
    global stars
    matrix.start()
    genStars()
    drawScrollStars()

def hybridSetup():
    global stars, starsBuffer
    matrix.start()
    genStars()

    stars = starsBuffer
    starsBuffer = {}

    hybridStarInit()

def starLoop():
    global starCount, stars, prevStarTime, starDelay

    #SELECT RANDOM STAR
    #addStar():
    if starCount < MAX_STARS:
        prevStarCount = starCount
        if (time.time_ns() - prevStarTime) >= starDelay:
            while starCount == prevStarCount: #while new star not yet added
                nextStar = (random.randint(0, WIDTH-1), random.randint(0, HEIGHT-1))
                hasAdjacent = checkForAdjacent(nextStar)
                if not hasAdjacent and (time.time_ns() - prevStarTime) >= starDelay:
                    prevStarTime = time.time_ns()
                    #starDelay = (10**9) * random.random() / 5
                    starDelay = (10**9) * 0.001

                    # [starState, dimLevel, dimDelay, flickerDir]
                        # starState: 0 -> inactive, 1 -> brightening, 2 -> peaking, -1 -> dimming
                        # color: (0 -> 255, 0 -> 255, 0 -> 255) (color value)
                        # dimDelay: float of a time at which to begin the dimming process
                        # flickerDir: direction of flicker, either -1 or 1
                    stars[nextStar] = [1, (0, 0, 0), 0, -1] 
                    starCount += 1

    #INCREMENT STAR BRIGHTNESS ACCORDING TO DIRECTION
    if SIM:
        keys = list(stars.keys())
    else:
        keys = stars.keys()

    for star in keys: #added list for python3.7 compat
        if stars[star][0] == 1: #brightenining
            if stars[star][1][0] == MAX_BRIGHTNESS:
                stars[star][0] = 2
                dimDelay = (10**9) * ((2 * random.random()) + 1.0)
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

def genStar():
    global starCount, stars

    nextStar = (-1, -1)
    hasAdjacent = True
    while hasAdjacent:
        nextStar = (random.randint(0, WIDTH - 1), random.randint(0, HEIGHT - 1))
        hasAdjacent = checkForAdjacent(nextStar)
        if not hasAdjacent:
            randBrightness = random.randint(20, 255) / 255.0
            randInd = random.randint(0, len(COLOR_DICT) - 1)
            baseColor = list(COLOR_DICT.values())[randInd]
            targetColor = tuple([randBrightness * i for i in baseColor])
            fadeFactor = (targetColor[0] / (255.0 * 3), targetColor[1] / (255.0 * 3), targetColor[2] / (255.0 * 3))

            stars[nextStar] = {
                "state": 1, #0 -> inactive, 1 -> brightening, 2 -> peaking, -1 -> dimming
                "currColor": [0, 0, 0], # rgb 
                "targetColor": targetColor, #rgb
                "fadeFactor": fadeFactor, #float for incrementing stars proportionally
                "dimDelay": 0, # int, nanoseconds
                "flickerDir": 0, # -1 or 1; direction of flicker
            }

            starCount += 1
            return nextStar

def genStars():
    global starCount, starsBuffer, stars

    while starCount < MAX_STARS:
        nextStar = (random.randint(0, WIDTH - 1), random.randint(0, HEIGHT - 1))
        hasAdjacent = checkForAdjacent(nextStar)
        if not hasAdjacent:
            randBrightness = random.randint(20, 255) / 255.0
            randInd = random.randint(0, len(COLOR_DICT) - 1)
            baseColor = list(COLOR_DICT.values())[randInd]
            targetColor = tuple([randBrightness * i for i in baseColor])
            fadeFactor = (targetColor[0] / (255.0 * 3), targetColor[1] / (255.0 * 3), targetColor[2] / (255.0 * 3))

            starsBuffer[nextStar] = {
                "state": 1, #0 -> inactive, 1 -> brightening, 2 -> peaking, -1 -> dimming
                "currColor": [0, 0, 0], # rgb 
                "targetColor": targetColor, #rgb
                "fadeFactor": fadeFactor, #float for incrementing stars proportionally
                "dimDelay": 0, # int, nanoseconds
                "flickerDir": 0, # -1 or 1; direction of flicker
            }

            starCount += 1

def clearStars():
    global starCount, starsBuffer, stars, starsLevel, haveStarsPeaked, haveStarsDimmed

    starCount = 0
    starsLevel = 0
    haveStarsPeaked = False
    haveStarsDimmed = False

def fadeStarLoop():
    global starCount, stars, starsBuffer, shineDelay, haveStarsPeaked, readyToShine, haveStarsDimmed

    if SIM:
        keys = list(stars.keys())
    else:
        keys = stars.keys()

    if not haveStarsPeaked:
        haveStarsPeaked = True
        for star in keys:
            if stars[star]["state"] == 1:
                haveStarsPeaked = False

                if stars[star]["currColor"][0] < stars[star]["targetColor"][0]:
                    stars[star]["currColor"][0] += SPEED
                if stars[star]["currColor"][1] < stars[star]["targetColor"][1]:
                    stars[star]["currColor"][1] += SPEED
                if stars[star]["currColor"][2] < stars[star]["targetColor"][2]:
                    stars[star]["currColor"][2] += SPEED

                if sum(stars[star]["currColor"]) >= sum(stars[star]["targetColor"]):
                    stars[star]["state"] = 2
    elif not haveStarsDimmed:
        haveStarsDimmed = True
        for star in keys:
            if stars[star]["state"] == 2:
                haveStarsDimmed = False

                if stars[star]["currColor"][0] > 0:
                    stars[star]["currColor"][0] -= SPEED
                if stars[star]["currColor"][1] > 0:
                    stars[star]["currColor"][1] -= SPEED
                if stars[star]["currColor"][2] > 0:
                    stars[star]["currColor"][2] -= SPEED

                if sum(stars[star]["currColor"]) <= 0:
                    stars[star]["state"] = 0
    else:
        clearStars()
        genStars()
        stars = starsBuffer
        starsBuffer = {}

        time.sleep(1500 / 1000.0)

    drawStars()

def newFadeStarLoop():
    global starCount, stars, starsBuffer, starsLevel, haveStarsPeaked, readyToShine, haveStarsDimmed

    if SIM:
        keys = list(stars.keys())
    else:
        keys = stars.keys()

    if not haveStarsPeaked:
        haveStarsPeaked = True
        for star in keys:
            if stars[star]["state"] == 1:
                haveStarsPeaked = False
                currColor = stars[star]["currColor"]
                targetColor = stars[star]["targetColor"]
                fadeFactor = stars[star]["fadeFactor"]

                if currColor[0] < targetColor[0]:
                    stars[star]["currColor"][0] = min(MAX_BRIGHTNESS, math.floor(starsLevel * fadeFactor[0]  * SPEED))
                if currColor[1] < targetColor[1]:
                    stars[star]["currColor"][1] = min(MAX_BRIGHTNESS, math.floor(starsLevel * fadeFactor[1]  * SPEED))
                if currColor[2] < targetColor[2]:
                    stars[star]["currColor"][2] = min(MAX_BRIGHTNESS, math.floor(starsLevel * fadeFactor[2]  * SPEED))

                if sum(stars[star]["currColor"]) >= sum(stars[star]["targetColor"]):
                    stars[star]["state"] = 2
                    readyToShine = True

        starsLevel += 1
    elif readyToShine:
        starsLevel -= 1
        time.sleep(shineDelay / 1000.0)
        readyToShine = False
        genStars()
    elif not haveStarsDimmed:
        haveStarsDimmed = True
        for star in keys:
            if stars[star]["state"] == 2:
                haveStarsDimmed = False
                currColor = stars[star]["currColor"]
                fadeFactor = stars[star]["fadeFactor"]

                if currColor[0] > 0:
                    stars[star]["currColor"][0] = max(0, min(MAX_BRIGHTNESS, math.floor(starsLevel * fadeFactor[0]  * SPEED)))
                if currColor[1] > 0:
                    stars[star]["currColor"][1] = max(0, min(MAX_BRIGHTNESS, math.floor(starsLevel * fadeFactor[1]  * SPEED)))
                if currColor[2] > 0:
                    stars[star]["currColor"][2] = max(0, min(MAX_BRIGHTNESS, math.floor(starsLevel * fadeFactor[2]  * SPEED)))

                if sum(stars[star]["currColor"]) <= 0:
                    stars[star]["state"] = 0

        starsLevel -= 1
    else:
        clearStars()
        genStars()
        stars = starsBuffer
        starsBuffer = {}

        #time.sleep(1500 / 1000.0)

    drawStars()

def overlapFadeStarLoop():
    global starCount, stars, starsBuffer, starsLevel, haveStarsPeaked, readyToShine, haveStarsDimmed

    if starsLevel <= 255 and not haveStarsPeaked:
        readyToShine = True
        for star in stars.keys():
            currColor = stars[star]["currColor"]
            targetColor = stars[star]["targetColor"]
            fadeFactor = stars[star]["fadeFactor"]

            if currColor[0] < targetColor[0]:
                stars[star]["currColor"][0] = min(MAX_BRIGHTNESS, math.floor(starsLevel * fadeFactor[0]  * SPEED))
            if currColor[1] < targetColor[1]:
                stars[star]["currColor"][1] = min(MAX_BRIGHTNESS, math.floor(starsLevel * fadeFactor[1]  * SPEED))
            if currColor[2] < targetColor[2]:
                stars[star]["currColor"][2] = min(MAX_BRIGHTNESS, math.floor(starsLevel * fadeFactor[2]  * SPEED))

        starsLevel += 1
    else:
        #starsLevel reached max brightness
        starsLevel -= 1
        starsLevelPeak = starsLevel
        haveStarsPeaked = True

    if haveStarsPeaked and readyToShine:
        time.sleep(shineDelay / 1000.0)
        readyToShine = False
        #potentially include this line v within genStars()
        starCount = 0
        genStars()

    if starsLevel >= 0 and haveStarsPeaked and not readyToShine:
        for star in stars.keys():
            haveStarsDimmed = False
            currColor = stars[star]["currColor"]
            fadeFactor = stars[star]["fadeFactor"]

            if currColor[0] > 0:
                stars[star]["currColor"][0] = max(0, min(MAX_BRIGHTNESS, math.floor(starsLevel * fadeFactor[0]  * SPEED)))
            if currColor[1] > 0:
                stars[star]["currColor"][1] = max(0, min(MAX_BRIGHTNESS, math.floor(starsLevel * fadeFactor[1]  * SPEED)))
            if currColor[2] > 0:
                stars[star]["currColor"][2] = max(0, min(MAX_BRIGHTNESS, math.floor(starsLevel * fadeFactor[2]  * SPEED)))

        for star in starsBuffer.keys():
            invStarsLevel = starsLevelPeak - starsLevel
            #invStarsLevel = 255 - starsLevel
            currColor = starsBuffer[star]["currColor"]
            targetColor = starsBuffer[star]["targetColor"]
            fadeFactor = starsBuffer[star]["fadeFactor"]

            if currColor[0] < targetColor[0]:
                starsBuffer[star]["currColor"][0] = min(MAX_BRIGHTNESS, math.floor(invStarsLevel * fadeFactor[0]  * SPEED))
            if currColor[1] < targetColor[1]:
                starsBuffer[star]["currColor"][1] = min(MAX_BRIGHTNESS, math.floor(invStarsLevel * fadeFactor[1]  * SPEED))
            if currColor[2] < targetColor[2]:
                starsBuffer[star]["currColor"][2] = min(MAX_BRIGHTNESS, math.floor(invStarsLevel * fadeFactor[2]  * SPEED))

        starsLevel -= 1
        haveStarsDimmed = True
    elif haveStarsDimmed:
        haveStarsDimmed = False
        clearStars()
        stars = starsBuffer
        starsBuffer = {}

        #time.sleep(1500 / 1000.0)

    overlapFadeDrawStars()
    
    #init already generated stars and begun thei
    #call function to


def hybridStarInit():
    global starCount, stars, starsBuffer, starsLevel, haveStarsPeaked, readyToShine, haveStarsDimmed

    starsLevel = 0
    while starsLevel <= 255:
        for star in stars.keys():
            fadeFactor = stars[star]["fadeFactor"]

            stars[star]["currColor"][0] = min(MAX_BRIGHTNESS, math.floor(starsLevel * fadeFactor[0]  * SPEED))
            stars[star]["currColor"][1] = min(MAX_BRIGHTNESS, math.floor(starsLevel * fadeFactor[1]  * SPEED))
            stars[star]["currColor"][2] = min(MAX_BRIGHTNESS, math.floor(starsLevel * fadeFactor[2]  * SPEED))

        starsLevel += 1

        drawStars()

def hybridStarLoop():
    global starCount, stars, starsBuffer, starsLevel, haveStarsPeaked, readyToShine, haveStarsDimmed

    activeStars = len(stars)
    if activeStars <= 0:
        return

    #Remove star
    oldStar = list(stars.keys())[random.randint(0, activeStars - 1)]

    starsLevel = 255
    while starsLevel >= 0:
        fadeFactor = stars[oldStar]["fadeFactor"]

        stars[oldStar]["currColor"][0] = max(0, math.floor(starsLevel * fadeFactor[0]  * SPEED))
        stars[oldStar]["currColor"][1] = max(0, math.floor(starsLevel * fadeFactor[1]  * SPEED))
        stars[oldStar]["currColor"][2] = max(0, math.floor(starsLevel * fadeFactor[2]  * SPEED))

        starsLevel -= 1

        drawStars()

    #remove star
    stars.pop(oldStar)
    starCount -= 1

    #Add new star
    newStar = genStar()

    starsLevel = 0
    while starsLevel <= 255:
        fadeFactor = stars[newStar]["fadeFactor"]

        stars[newStar]["currColor"][0] = min(MAX_BRIGHTNESS, math.floor(starsLevel * fadeFactor[0]  * SPEED))
        stars[newStar]["currColor"][1] = min(MAX_BRIGHTNESS, math.floor(starsLevel * fadeFactor[1]  * SPEED))
        stars[newStar]["currColor"][2] = min(MAX_BRIGHTNESS, math.floor(starsLevel * fadeFactor[2]  * SPEED))

        starsLevel += 1

        drawStars()

    starCount += 1


    time.sleep(0 / 1000.0)

def drawStars():
    for star in stars.keys():
        starColor = stars[star]["currColor"]
        matrix.set_rgb(star[0], star[1], starColor[0], starColor[1], starColor[2])

    matrix.flip()

def overlapFadeDrawStars():
    for star in stars.keys():
        starColor = stars[star]["currColor"]
        matrix.set_rgb(star[0], star[1], starColor[0], starColor[1], starColor[2])

    for star in starsBuffer.keys():
        starColor = starsBuffer[star]["currColor"]
        matrix.set_rgb(star[0], star[1], starColor[0], starColor[1], starColor[2])

    matrix.flip()

def scrollStarLoop():
    global stars, starsBuffer, dx, dy

    for star in stars.keys():
        newX = (star[0] + dx) % WIDTH
        newY = (star[1] + dy) % HEIGHT
        starsBuffer[(newX, newY)] = stars[star]

    removeStars()

    stars = starsBuffer
    starsBuffer = {}

    drawScrollStars()

def removeStars():
    for star in stars.keys():
        matrix.set_rgb(star[0], star[1], 0, 0, 0)

def drawScrollStars():
    for star in stars.keys():
        
        starColor = stars[star]["targetColor"]
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

        if SIM:
            keys = list(shStarTrail.keys())
        else:
            keys = shStarTrail.keys()

        for t in keys:
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

def constellationLoop():
    pass

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


##############
# MAIN LOOP
##############

overlapFadeSetup()
#hybridSetup()
while True:
    #newFadeStarLoop()
    #hybridStarLoop()
    overlapFadeStarLoop()
    #shStarLoop()
    time.sleep(REFRESH / 1000.0)

    if SIM:
        time.sleep(5 / 1000.0) #delay to better simulate screen fps
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
