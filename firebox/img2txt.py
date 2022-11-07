from PIL import Image
import os

num_frames = len(os.listdir('frames'))
with open("ani.txt", "a") as file:
    file.write(str(num_frames) + "\n")

for filename in os.listdir('frames'):
    im = Image.open("frames/" + filename)
    im = im.convert('RGB')
    size = im.size
    pix = im.load()

    arr = []
    for x in range(size[0]):
        arr.append([])
        for y in range(size[1]):
            arr[x].append(pix[x, y])

    with open("ani.txt", "a") as file:
        for x in range(size[0]):
            for y in range(size[1]):
                color = list(pix[x,y])
                file.write(" ".join(str(c) for c in color) + "\n")
