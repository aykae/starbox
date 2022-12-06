from PIL import Image
import os

INPUT = "final/fire-ani"
OUTPUT = "data/ani.txt"

BLACK_THRESH = (25, 25, 25)

#CREATES A SINGLE ANIMATION FILES THAT IS LIGHTWEIGHT AND EFFICIENT
#DON'T STORE NOR REDRAW REDUNDENCIES or BLACK PIXELS
#MAYBE DON'T EVEN DRAW LOGS (using a darkness threshold check e.g. > 700 (brown))

def generateAni(dir, output):
    #clear output file
    with open(output, "w") as file:
        pass

    #dicts used to prevent redundant pixel redraws
    prevdict = {}
    currdict = {}

    #maps colors to their index
    paletteindex = 0
    palette = {}

    # generating color palette
    with open(output, "a") as file:
        for filename in os.listdir(dir):
            im = Image.open(dir + "/" + filename)
            im = im.convert('RGB')
            size = im.size
            pix = im.load()

            for x in range(size[0]):
                for y in range(size[1]):
                    color = list(pix[x,y])
                    cstr = " ".join(str(c) for c in color)

                    if cstr not in palette.keys():
                        palette[cstr] = paletteindex
                        file.write(cstr + " " + str(paletteindex) + "\n")
                        paletteindex += 1

        #marks end of palette
        file.write("P\n")

    with open(output, "a") as file:
        for filename in os.listdir(dir):
            im = Image.open(dir + "/" + filename)
            im = im.convert('RGB')
            size = im.size
            pix = im.load()

            arr = []
            for x in range(size[0]):
                arr.append([])
                for y in range(size[1]):
                    arr[x].append(pix[x, y])

                for x in range(size[0]):
                    file.write(str(x) + "\n")
                    for y in range(size[1]):
                        if sum(pix[x,y]) > sum(BLACK_THRESH):
                            if prevdict.get((x,y)) is None or (prevdict.get((x,y)) and prevdict.get((x,y)) != pix[x,y]):
                                currdict[(x,y)] = pix[x,y]

                                ystr = str(y) + " "
                                color = list(pix[x,y])
                                cstr = " ".join(str(c) for c in color)
                                cindex = palette[cstr]
                                file.write(ystr + str(cindex) + "\n")

                prevdict = currdict
                currdict = {}
                #denote end of frame 
                file.write("X\n")

def generateImg(filename, output=OUTPUT):
    im = Image.open(filename)
    im = im.convert('RGB')
    size = im.size
    pix = im.load()
    with open(output, "w") as file:
        for x in range(size[0]):
            for y in range(size[1]):
                color = list(pix[x,y])
                file.write(" ".join(str(c) for c in color) + "\n")

#MAIN
#generateImg(INPUT)
generateAni(INPUT, OUTPUT)