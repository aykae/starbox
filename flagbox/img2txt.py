from PIL import Image
import os

INPUT = "img/final/usa.bmp"
OUTPUT = "img.txt"

def generateAni(dir, output="flag-txt/ani.txt"):
    num_frames = len(os.listdir(dir))
    with open(output, "a") as file:
        file.write(str(num_frames) + "\n")

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

        with open(dir, "a") as file:
            for x in range(size[0]):
                for y in range(size[1]):
                    color = list(pix[x,y])
                    file.write(" ".join(str(c) for c in color) + "\n")

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

generateImg(INPUT)