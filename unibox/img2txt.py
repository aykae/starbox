from PIL import Image
import os

INPUT = "final/neu-final-2.bmp"
OUTPUT = "data/logo2.txt"

BLACK = (0, 0, 0)

#CREATES A SINGLE ANIMATION FILES THAT IS LIGHTWEIGHT AND EFFICIENT
#DON'T STORE NOR REDRAW REDUNDENCIES or BLACK PIXELS
#MAYBE DON'T EVEN DRAW LOGS (using a darkness threshold check e.g. > 700 (brown))

#FILE BEGINS WITH COLOR PALETTE (ENDS W/ P)
#THEN EACH X VALUES OF A FRAME IS ENUMERATED (ENDS W/ X)
    #EVERY Y w/ COLOR VAL IS LISTED
#REPEATED FOR EACH FRAME (ENDS W/ F)

def generateAni(dir, output):
    #clear output file
    with open(output, "w") as file:
        numFrames = len(os.listdir(dir))
        file.write(str(numFrames) + " FRAMES\n")

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

            for x in range(size[0]):
                file.write(str(x) + "\n")
                for y in range(size[1]):
                    if prevdict.get((x,y)) and prevdict.get((x,y)) != pix[x,y]:
                            currdict[(x,y)] = pix[x,y]

                            ystr = str(y) + " "
                            color = list(pix[x,y])
                            cstr = " ".join(str(c) for c in color)
                            cindex = palette[cstr]
                            file.write(ystr + str(cindex) + "\n")
                    elif not prevdict.get((x,y)) and pix[x,y] != BLACK:
                            currdict[(x,y)] = pix[x,y]

                            ystr = str(y) + " "
                            color = list(pix[x,y])
                            cstr = " ".join(str(c) for c in color)
                            cindex = palette[cstr]
                            file.write(ystr + str(cindex) + "\n")


                file.write("X\n")

            #denote end of frame 
            file.write("F\n")

            prevdict = currdict
            currdict = {}

def generateAniIneff(dir, output):
    #clear output file
    with open(output, "w") as file:
        numFrames = len(os.listdir(dir))
        file.write(str(numFrames) + " FRAMES\n")

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
                    # if sum(color) < sum(BLACK_THRESH):
                    #     color = (0, 0, 0)

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

            for x in range(size[0]):
                file.write(str(x) + "\n")
                for y in range(size[1]):
                    ystr = str(y) + " "
                    color = list(pix[x,y])
                    cstr = " ".join(str(c) for c in color)
                    cindex = palette[cstr]
                    file.write(ystr + str(cindex) + "\n")
                file.write("X\n")

            #denote end of frame 
            file.write("F\n")

def generateImg(filename, output):
    paletteindex = 0
    palette = {}

    # generating color palette
    with open(output, "w") as file:
        im = Image.open(filename)
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
        im = Image.open(filename)
        im = im.convert('RGB')
        size = im.size
        pix = im.load()

        for x in range(size[0]):
            file.write(str(x) + "\n")
            for y in range(size[1]):
                if sum(pix[x,y]) > 0:
                    ystr = str(y) + " "
                    color = list(pix[x,y])
                    cstr = " ".join(str(c) for c in color)
                    cindex = palette[cstr]
                    file.write(ystr + str(cindex) + "\n")

            file.write("X\n")
        file.write("F\n")

def generateImgIneff(filename, output=OUTPUT):
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
generateImg(INPUT, OUTPUT)