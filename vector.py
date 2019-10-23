import math

def punto(este, otro):
    return otro[0] * este[0] + otro[1] * este[1]

def cruz(este, otro):
    return este[0] * otro[1] - este[1] * otro[0]

def mag(este):
    return math.sqrt(este[0]**2 + este[1]**2)

def sub(este, otro):
    return (este[0] - otro[0], este[1] - otro[1])

def add(este, otro):
    return (este[0] + otro[0], este[1] + otro[1])

def mult(este, escalar):
    return (este[0] * escalar, este[1] * escalar)

def normalizar(este):
    m = mag(este)
    return (este[0] / m, este[1] / m)
