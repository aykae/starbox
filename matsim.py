import pygame

class MatrixSim:

    BG_GRAY = 25
    BG_COLOR = (BG_GRAY, BG_GRAY, BG_GRAY)

    PIXEL_SIZE = 12
    PIXEL_SPACING = 2

    X_OFFSET = 20
    Y_OFFSET = 20

    def __init__(self, width, height):
        pygame.init()
        self.display = pygame.display


        self.matrix_width = width
        self.matrix_height = height

        self.window_width = (self.matrix_width * (self.PIXEL_SIZE + self.PIXEL_SPACING)) + 2 * (self.X_OFFSET)
        self.window_height = (self.matrix_height * (self.PIXEL_SIZE + self.PIXEL_SPACING)) + 2 * (self.Y_OFFSET)

        self.window = self.display.set_mode((self.window_width, self.window_height))
        self.window.fill(self.BG_COLOR)

    
    def start(self):
        dx = 0
        dy = 0
        px = 0
        py = 0
        for y in range(self.window_height):
            for x in range(self.window_width):
                if px < self.matrix_width and dx <= x < (dx + self.PIXEL_SIZE):
                    if py < self.matrix_height and dy <= y < (dy + self.PIXEL_SIZE):
                        self.window.set_at((x + self.X_OFFSET, y + self.Y_OFFSET), ("0x000000"))
                else:
                    #increment x pixel
                    if x - dx == (self.PIXEL_SIZE + self.PIXEL_SPACING - 1) and px < self.matrix_width:
                        px += 1
                        dx += (self.PIXEL_SIZE + self.PIXEL_SPACING)

            #increment y pixel
            if y - dy == (self.PIXEL_SIZE + self.PIXEL_SPACING - 1) and py < self.matrix_height:
                py += 1
                dy += (self.PIXEL_SIZE + self.PIXEL_SPACING)

            #reset x vars for next row
            dx = 0
            px = 0

        self.display.flip()

    def set_rgb(self, x, y, r, g, b):
        color = pygame.Color(r, g, b)
        dx = x * (self.PIXEL_SIZE + self.PIXEL_SPACING) + self.X_OFFSET
        dy = y * (self.PIXEL_SIZE + self.PIXEL_SPACING) + self.Y_OFFSET

        for y in range(self.PIXEL_SIZE):
            for x in range(self.PIXEL_SIZE):
                self.window.set_at((dx + x, dy + y), color)

    def flip(self):
        self.display.flip()


# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False

# pygame.quit()
# exit()