import hub75, time, random

WIDTH = 64
HEIGHT = 64
MAX_BRIGHTNESS = 255
MAX_STARS = 1
SPEED = 1

matrix = hub75.Hub75(WIDTH, HEIGHT)
matrix.start()

starCount = 0
stars = {}

prevStarTime = 0
delay = -1

def setup():
    return


def loop():
    global starCount, stars, prevStarTime, delay

    #SELECT RANDOM STAR 
    nextStar = (random.randint(0, WIDTH-1), random.randint(0, HEIGHT-1))
    currTime = time.time()
    if nextStar not in stars.keys() and starCount < MAX_STARS and (currTime - prevStarTime) >= delay:
        prevStarTime = time.time()
        delay = 0.1 * random.random()

        stars[nextStar] = [1, 0, 0] #
        starCount += 1

    #INCREMENT STAR BRIGHTNESS ACCORDING TO DIRECTION
    for star in stars.keys():
        if stars[star][0] == 1:
            if stars[star][1] >= MAX_BRIGHTNESS:
                stars[star][0] = 2
                dimDelay = 2.0 * random.random()
                stars[star][2] = time.time() + dimDelay #assign dim delay
            else:
                stars[star][1] = min(stars[star][1] + SPEED, MAX_BRIGHTNESS) #brighten star
        elif stars[star][0] == -1:
            if stars[star][1] <= 0:
                stars.pop(star) #remove star from active dict
                starCount -= 1
            else:
                stars[star][1] = max(stars[star][1] - SPEED, 0) #dim star
        elif stars[star][0] == 2:
            if int(time.time()) > int(stars[star][2]):
                stars[star][2] = 0
                stars[star][0] = -1
            
    updateMatrix()

def updateMatrix():
    for star in stars.keys():
        starVal = int(stars[star][1])
        matrix.set_rgb(star[0], star[1], starVal, starVal, starVal)

    matrix.flip()

setup()
while True:
    loop()