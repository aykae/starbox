import hub75, time, random

WIDTH = 64
HEIGHT = 64
MAX_BRIGHTNESS = 255
MAX_STARS = 10

matrix = hub75.Hub75(WIDTH, HEIGHT)
matrix.start()

def shimmeringStars():
    #Create a WxH state matrix for stars and init to 0
        # 0 for off
        # 1 for currently brightening
        # -1 for currently dimming

    starCount = 0
    stars = []
    for _ in range(HEIGHT):
        temp = []
        for _ in range(WIDTH):
            # [direction, brightness] (assuming white stars, so 1 val for brightness)
            temp.append([0,0])
        stars.append(temp)

    nextStar = (random.randint(WIDTH), random.randint(HEIGHT))
    if stars[nextStar[1]][nextStar[0]] == 0 and starCount < MAX_STARS:
        stars[nextStar[1]][nextStar[0]] = 1
        starCount += 1


    #OPTIMIZATION
        # use a dictionary instead of a matrix, only store non zero directions

    for y in range(HEIGHT):
        for x in range(WIDTH):
            if stars[y][x][0] == 1:
                if stars[y][x][1] == MAX_BRIGHTNESS:
                    stars[y][x][0] = -1 #flip direction
                    stars[y][x][1] -= 1 #begin dimming process
                else:
                    stars[y][x][1] += 1 #brighten star

            elif stars[y][x][0] == -1:
                if stars[y][x][1] == 0:
                    stars[y][x][0] = 0 #set star to idle
                    starCount -= 1
                else:
                    stars[y][x][1] -= 1 #dim star
            


    # -- Loop through entire state matrix, if brightening, increase brightness by some BRIGHTENING_SPEED constant
    # -- If reached max brightness (could be a variable defaulting to 255), switch state to -1 and begin dimming process
    # -- If dimming star reaches 0's, set state to 0

    #POTENTIAL
        #let stars shimmer(jitter in brightness) at their peak before dimming


def incrementalFill(r, g, b):
    #Fill matrix with red
    for y in range(HEIGHT):
        for x in range(WIDTH):
            matrix.set_rgb(x, y, r, g, b)
        
            matrix.flip()

    #Erase matrix
    for y in range(HEIGHT-1, 0, -1):
        for x in range(WIDTH-1, 0, -1):
            matrix.set_rgb(x, y, 0, 0, 0)
        
            matrix.flip()


while True:
    # r = random.randint(0, 256)
    # g = random.randint(0, 256)
    # b = random.randint(0, 256)
    # incrementalFill(r, b, g)

    shimmeringStars()