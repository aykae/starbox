import hub75, time, random

WIDTH = 64
HEIGHT = 64
MAX_BRIGHTNESS = 255
MAX_STARS = 50
SPEED = 20

matrix = hub75.Hub75(WIDTH, HEIGHT)
matrix.start()

starCount = 0
stars = []

def setup():
    global stars
    #Create a WxH state matrix for stars and init to 0
        # 0 for off
        # 1 for currently brightening
        # -1 for currently dimming

    for _ in range(HEIGHT):
        temp = []
        for _ in range(WIDTH):
            # [state, brightness] (assuming white stars, so single val for brightness)
            temp.append([0,0])
        stars.append(temp)


def loop():
    global starCount, stars
    
    nextStar = (random.randint(0, WIDTH-1), random.randint(0, HEIGHT-1))
    if stars[nextStar[1]][nextStar[0]][0] == 0 and starCount < MAX_STARS:
        stars[nextStar[1]][nextStar[0]][0] = 1
        starCount += 1

    #FUTURE OPTIMIZATION
        # use a dictionary instead of a matrix, only store non zero directions

    # -- Loop through entire state matrix, if brightening, increase brightness by some BRIGHTENING_SPEED constant
    # -- If reached max brightness (could be a variable defaulting to 255), switch state to -1 and begin dimming process
    # -- If dimming star reaches 0's, set state to 0
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if stars[y][x][0] == 1:
                if stars[y][x][1] >= MAX_BRIGHTNESS:
                    stars[y][x][0] = -1 #flip direction
                else:
                    stars[y][x][1] = min(stars[y][x][1] + SPEED, MAX_BRIGHTNESS) #brighten star

            elif stars[y][x][0] == -1:
                if stars[y][x][1] <= 0:
                    stars[y][x][0] = 0 #set star to idle
                    starCount -= 1
                else:
                    stars[y][x][1] = max(stars[y][x][1] - SPEED, 0) #dim star
            
    updateMatrix()

    #POTENTIAL
        #let stars shimmer(jitter in brightness) at their peak before dimming

def updateMatrix():
    for y in range(HEIGHT):
        for x in range(WIDTH):
            starState = stars[y][x][0]
            starVal = stars[y][x][1]
            if starState != 0:
                matrix.set_rgb(x, y, starVal, starVal, starVal)
        
    matrix.flip()

setup()
while True:
    loop()
