import hub75, time, random

WIDTH = 64
HEIGHT = 64
MAX_BRIGHTNESS = 255
MAX_STARS = 50
SPEED = 20

matrix = hub75.Hub75(WIDTH, HEIGHT)
matrix.start()

starCount = 0
stars = {}

def setup():
    return


def loop():
    #global starCount, stars

    #SELECT RANDOM STAR 
    nextStar = (random.randint(0, WIDTH-1), random.randint(0, HEIGHT-1))
    if nextStar not in stars.keys() and starCount < MAX_STARS:
        stars[nextStar] = [1, 0] #THIS MAY
        starCount += 1

    #INCREMENT STAR BRIGHTNESS ACCORDING TO DIRECTION
    for star in stars.keys():
        if stars[star][0] == 1:
            if stars[star][1] >= MAX_BRIGHTNESS:
                stars[star][0] = -1
            else:
                stars[star][1] = min(stars[star][1] + SPEED, MAX_BRIGHTNESS) #brighten star
        elif stars[star][0] == -1:
            if stars[star] <= 0:
                stars.pop(star) #remove star from active dict
                starCount -= 1
            else:
                stars[star] = max(stars[star][1] - SPEED, 0) #dim star
            
    updateMatrix()

def updateMatrix():
    for star in stars.keys():
        starVal = stars[star][1]
        matrix.set_rgb(star[0], star[1], starVal, starVal, starVal)

    matrix.flip()

setup()
while True:
    loop()
