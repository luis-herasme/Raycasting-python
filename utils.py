import math
from PIL import Image

def getTexture(src):
    data = list(Image.open(src, 'r').getdata())
    length = round(math.sqrt(len(data)))
    result = [0] * length

    for x in range(length):
        line = [0] * length
        for y in range(length):
            line[y] = data[(y * length) + x]
        result[x] = line
        #line.reverse()
        #result[length - x - 1] = line
    #result.reverse()
    #print(result)
    return result