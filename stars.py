import hub75, time, random

WIDTH = 32
HEIGHT = 32
MAX_BRIGHTNESS = 255
MAX_STARS = 50
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
    if starCount < MAX_STARS:
        nextStar = (random.randint(0, WIDTH-1), random.randint(0, HEIGHT-1))
        currTime = time.time_ns()
        if nextStar not in stars.keys() and (currTime - prevStarTime) >= delay:
            prevStarTime = time.time_ns()
            delay = random.random()

            # [star_state, dim_level, dim_delay]
                # star_state: 0 -> inactive, 1 -> brightening, 2 -> peaking, -1 -> dimming
                # dim_level: 0 -> 255 (white value)
                # dim_delay: float of a time at which to begin the dimming process
            stars[nextStar] = [1, 0, 0] 
            starCount += 1

    #INCREMENT STAR BRIGHTNESS ACCORDING TO DIRECTION
    for star in stars.keys():
        if stars[star][0] == 1: #brightenining
            if stars[star][1] >= MAX_BRIGHTNESS:
                stars[star][0] = 2
                dimDelay = (10**9) * random.randint(1,2) # 1-2 seconds
                stars[star][2] = time.time_ns() + dimDelay #assign dim delay
            else:
                stars[star][1] = min(stars[star][1] + SPEED, MAX_BRIGHTNESS) #brighten star
        elif stars[star][0] == -1: #dimming
            if stars[star][1] <= 0:
                stars.pop(star) #remove star from active dict
                starCount -= 1
            else:
                stars[star][1] = max(stars[star][1] - SPEED, 0) #dim star
        elif stars[star][0] == 2: #shining (static)
            if time.time() > stars[star][2]:
                stars[star][2] = 0
                stars[star][0] = -1
            
    updateMatrix()

def updateMatrix():
    for star in stars.keys():
        starVal = int(stars[star][1])
        matrix.set_rgb(star[0], star[1], starVal, starVal, starVal)

    matrix.flip()

##############
# MAIN LOOP
##############

setup()
while True:
    loop()