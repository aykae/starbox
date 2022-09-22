import hub75, time, random

WIDTH = 64
HEIGHT = 64

matrix = hub75.Hub75(WIDTH, HEIGHT)
matrix.start()

while True:
    incrementalFill(255, 0, 0)

def shimmeringStars():
    #Create a WxH state matrix for stars and init to 0
        # 0 for off
        # 1 for currently brightening
        # -1 for currently dimming

    state = []
    for i in range(HEIGHT):
        temp = []
        for j in range(WIDTH):
            temp.append(0)
        state.append(temp)

    nextStar = (random.randint(WIDTH), random.randint(HEIGHT))
    if state[nextStar[0], nextStar[1]] == 0:
        state[nextStar[0], nextStar[1]] = 1

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
            time.sleep(0.25)

    #Erase matrix
    for y in range(HEIGHT-1, 0, -1):
        for x in range(WIDTH-1, 0, -1):
            matrix.set_rgb(x, y, 0, 0, 0)
        
            matrix.flip()
            time.sleep(0.25)