from vector import *

def render(rayos, camara, objetos):
    pantalla = ['Nada'] * len(rayos)
    colores = ['Nada'] * len(rayos)
    eses = [0] * len(rayos)

    for obj in objetos:
        for rayo in range(len(rayos)):
            y = sub(obj[1], obj[0])
            x = rayos[rayo]

            if (cruz(y, x)):
                t = (cruz(y, obj[0]) - cruz(y, camara)) / cruz(y, x)
                s = (cruz(x, camara) - cruz(x, obj[0])) / cruz(x, y)

                eses[rayo] = s

                if (t < 0):
                    t = 'Nada'

                if (s > 1 or s < 0):
                    t = 'Nada'

                if (pantalla[rayo] == 'Nada'):
                    if (not( t == 'Nada' )):
                        colores[rayo] = obj[2]
                        pantalla[rayo] = t
                else:
                    if (not( t == 'Nada' )):
                        if (pantalla[rayo] > t):
                            colores[rayo] = obj[2]
                            pantalla[rayo] = t

    for i in range(len(pantalla)):
        if (pantalla[i] == 'Nada'):
            pantalla[i] = 0
        if (colores[i] == 'Nada'):
            colores[i] = (0, 0, 0)

    return (pantalla, colores, eses)

def draw(objetos, screen, pygame):
    for obj in objetos:
        pygame.draw.line(screen, obj[2], obj[0], obj[1])
