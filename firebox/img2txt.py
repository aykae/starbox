from PIL import Image
import json

im = Image.open('fireframe.jpg')
im = im.convert('RGB')
size = im.size
print(size)
pix = im.load()

arr = []
for x in range(size[0]):
    arr.append([])
    for y in range(size[1]):
        arr[x].append(pix[x, y])

with open("ani.txt", "w") as file:
    for x in range(size[0]):
        for y in range(size[1]):
            color = list(pix[x,y])
            file.write(" ".join(str(c) for c in color) + "\n")
