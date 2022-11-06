import hub75

WIDTH = 32
HEIGHT = 32 

matrix = hub75.Hub75(WIDTH, HEIGHT)
matrix.set_rgb(star[0], star[1], starColor[0], starColor[1], starColor[2])

matrix.flip()