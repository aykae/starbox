import hub75, time, random

WIDTH = 32
HEIGHT = 32
MAX_BRIGHTNESS = 255
MIN_FLICKER = 20 
MAX_FLICKER = 25
MAX_STARS = 500
SPEED = 1

matrix = hub75.Hub75(WIDTH, HEIGHT)
matrix.start()

starCount = 0
stars = {}

prevStarTime = 0
delay = -1

def setup():
    return


def starLoop():
    global starCount, stars, prevStarTime, prevStarCount, delay

    #SELECT RANDOM STAR
    if starCount < MAX_STARS:
        prevStarCount = starCount
        if (time.time_ns() - prevStarTime) >= delay:
            while starCount == prevStarCount: #while new star not yet added
                nextStar = (random.randint(0, WIDTH-1), random.randint(0, HEIGHT-1))
                hasAdjacent = checkForAdjacent(nextStar)
                if nextStar not in stars.keys() and (time.time_ns() - prevStarTime) >= delay and not hasAdjacent:
                    prevStarTime = time.time_ns()
                    delay = (10**9) * random.randint(0, 1)

                    # [starState, dimLevel, dimDelay, flickerDir]
                        # starState: 0 -> inactive, 1 -> brightening, 2 -> peaking, -1 -> dimming
                        # color: (0 -> 255, 0 -> 255, 0 -> 255) (color value)
                        # dimDelay: float of a time at which to begin the dimming process
                        # flickerDir: direction of flicker, either -1 or 1
                    stars[nextStar] = [1, (0, 0, 0), 0, -1] 
                    starCount += 1

    #INCREMENT STAR BRIGHTNESS ACCORDING TO DIRECTION
    for star in stars.keys():
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
            
    updateMatrix()

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

def updateMatrix():
    for star in stars.keys():
        starColor = stars[star][1]
        matrix.set_rgb(star[0], star[1], starColor[0], starColor[1], starColor[2])

    matrix.flip()

##############
# MAIN LOOP
##############

setup()
while True:
    starLoop()