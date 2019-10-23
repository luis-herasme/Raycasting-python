import math
from vector import *

def rotar(objeto, angulo, pivote):
    v1 = sub(objeto[0], pivote)
    v2 = sub(objeto[1], pivote)

    objeto[0] = add(pivote, rot(v1, angulo))
    objeto[1] = add(pivote, rot(v2, angulo))

def rot(vec, angulo):
    return (vec[0] * math.cos(angulo) - vec[1] * math.sin(angulo), vec[0] * math.sin(angulo) + vec[1] * math.cos(angulo))
