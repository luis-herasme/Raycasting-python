from vector import *

def render(rayos, camara, objetos):
    pantalla = ['Nada'] * len(rayos)
    atibutos = [None] * len(rayos)
    eses = [0] * len(rayos)

    for obj in objetos:
        for rayo in range(len(rayos)):
            y = sub(obj["vertex"][1], obj["vertex"][0])
            x = rayos[rayo]

            if (cruz(y, x)):
                t = (cruz(y, obj["vertex"][0]) - cruz(y, camara)) / cruz(y, x)
                s = (cruz(x, camara) - cruz(x, obj["vertex"][0])) / cruz(x, y)

                if (t < 0):
                    t = 'Nada'

                if (s > 1 or s < 0):
                    t = 'Nada'
                else:
                    if (pantalla[rayo] == 'Nada'):
                        if (not ( t == 'Nada' ) ):
                            eses[rayo] = s
                    elif (not ( t == 'Nada' ) ):
                        if (pantalla[rayo] > t):
                            eses[rayo] = s

                if (pantalla[rayo] == 'Nada'):
                    if (not( t == 'Nada' )):
                        atibutos[rayo] = obj
                        pantalla[rayo] = t
                else:
                    if (not( t == 'Nada' )):
                        if (pantalla[rayo] > t):
                            atibutos[rayo] = obj
                            pantalla[rayo] = t

    for i in range(len(pantalla)):
        if (pantalla[i] == 'Nada'):
            pantalla[i] = 0
            eses[i] = 0

    return (pantalla, atibutos, eses)

def draw(objetos, screen, pygame):
    for obj in objetos:
        pygame.draw.line(screen, obj['color'], obj["vertex"][0], obj["vertex"][1])
