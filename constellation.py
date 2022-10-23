import hub75, math

WIDTH = HEIGHT = 32
matrix = hub75.Hub75(WIDTH, HEIGHT)
ORANGE = (230, 184, 46)
offsetX = 20
offsetY = 20
currConst = "bigdipper"
#constellations structured with points from left to right of form (relative position->brightness)
const = {
    "cancer": {
        (0, 1): 200,
        (2, 4): 255,
        (1, 12): 200,
        (3, 7): 150,
        (6, 0): 200
    },
    "bigdipper": {
        (0, 9): 255,
        (1, 7): 200,
        (2, 2): 255,
        (2, 6): 255,
        (3, 4): 200,
        (4, 0): 255,
        (6, 1): 255 
    }

}

def setup():
    matrix.start()

def drawStars():
    for star in const[currConst]:
        starBrightness = const[currConst][star] / 255.0

        #flip constellation for accuracy
        starX = HEIGHT - (star[1]) - offsetX
        starY = WIDTH - (star[0]) - offsetY

        matrix.set_rgb(starX, starY, math.floor(starBrightness * ORANGE[0]), math.floor(starBrightness * ORANGE[1]), math.floor(starBrightness * ORANGE[2]))
        #matrix.set_rgb(0, 0, math.floor(starBrightness * ORANGE[0]), math.floor(starBrightness * ORANGE[1]), math.floor(starBrightness * ORANGE[2]))
    matrix.flip()



setup()
while True:
    drawStars()