import pygame
import math
import rotar
import renderizador
import random
from PIL import Image
from vector import *

im = Image.open('mario.png', 'r')

textura = list(im.getdata() )
print(textura)

def convert(li):
    length = round(math.sqrt(len(li)))
    result = [0] * length

    for x in range(length):
        line = [0] * length
        for y in range(length):
            line[y] = li[y + (x * length)]
        result[x] = line
        #result[length - x - 1] = line
    result.reverse()
    return result
textura = convert(textura)
print(textura)


width = 400
pantalla = []
objetos = [
    [ (200, 100), (225, 100), (255, 0, 0)], 
   # [ (175, 300), (225, 300), (255, 0, 0)], 
   # [ (300, 100), (300, 300), (0, 255, 0) ],
   # [ (100, 300), (200, 300), (100, 0, 150) ],
]
'''
textura = [
    [(255, 0, 0), (255, 0, 0), (255, 255, 255), (0, 0, 255), (0, 0, 255)], #Columna
    [(255, 0, 0), (255, 0, 0), (255, 255, 255), (0, 0, 255), (0, 0, 255)],
    [(255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255)],
    [(0, 0, 255), (0, 0, 255), (255, 255, 255), (255, 0, 0), (255, 0, 0)],
    [(0, 0, 255), (0, 0, 255), (255, 255, 255), (255, 0, 0), (255, 0, 0)]
]
'''

position = (200, 200)
vel = (0, -1)
speed = 100
ang = 2
RAYOS_AMT = 128
CAMPO_VISTA = math.pi / 4
DELT_ANG = CAMPO_VISTA / RAYOS_AMT
sizeLine = int(width/RAYOS_AMT)
modo = True
sizeWall = 0.5 #mas pequeno mas grande
SIZE_TALL = 25
MAX_WALL_TEX = 25
def realColor(color, a):
    a = a ** 2
    return (color[0] * a, color[1]*a, color[2] * a)

en_creacion = 0

if __name__ == '__main__':
    screen = pygame.display.set_mode((width, width))
    screen2 = pygame.display.set_mode((width, width))
    Rayos = [None] * RAYOS_AMT
    pygame.display.flip()
    clock = pygame.time.Clock()

    running = True
    while running:
        dt = clock.tick() / 1000
        #Rayos
        rayo = rotar.rot(vel, -CAMPO_VISTA / 2)
        for i in range(RAYOS_AMT):
            Rayos[i] = rotar.rot(rayo, DELT_ANG * i)
        
        (ts, colores, eses) = renderizador.render(Rayos, position, objetos)

        if (modo):
            pygame.draw.rect(screen, (0, 0, 0), (0, 0, width, width))
            
            for i in range(RAYOS_AMT):
                pygame.draw.line(screen, (0, 0, 255), (int(position[0]), int(position[1])), (int(position[0] + Rayos[i][0] * ts[i] ), int(position[1] + Rayos[i][1] * ts[i])))

            pygame.draw.circle(screen, (255, 255, 255), (int(position[0]), int(position[1])), 5)
            renderizador.draw(objetos, screen, pygame)
            pygame.draw.line(screen, (255, 0, 255), (int(position[0]), int(position[1])), (int(position[0] + vel[0] * 20 ), int(position[1] + vel[1] * 20)), 3)

        else:   # Raycasting
            pygame.draw.rect(screen, (0, 0, 0), (0, 0, width, width))

            for i in range(len(ts)):
                ts[i] *= punto(Rayos[i], vel)

            for i in range(RAYOS_AMT):
                if (not(colores[i] == (0,0,0))):
                    if (eses[i]):
                        R = len(textura[0])

                        index = math.floor(eses[i] * R)

                        #print(index)

                        for pixel in range(len(textura[index])):
                            offset = pixel * (SIZE_TALL * (width/ts[i]) / R) + ((width - SIZE_TALL * (width/ts[i]))/2)
                            rect = pygame.Rect((sizeLine + 1) * i, offset, sizeLine + 1, (SIZE_TALL * (width/ts[i]) / R) + 1)
                            pygame.draw.rect(screen, textura[index][pixel], rect)
                        #pygame.draw.rect(screen, realColor(colores[i], 1 - (ts[i] / width)), pygame.Rect((sizeLine + 1) * i, (width - SIZE_TALL * (width/ts[i]))/2 , sizeLine + 1 , SIZE_TALL * (width/ts[i])))

        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT]:
            vel = rotar.rot(vel, -ang * dt)
        if keys[pygame.K_RIGHT]:
            vel = rotar.rot(vel, ang * dt)
        if keys[pygame.K_UP]:
            position = add(position, mult(vel, speed * dt))
        if keys[pygame.K_DOWN]:
            position = sub(position, mult(vel, speed * dt))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            '''
            if (pygame.MOUSEBUTTONDOWN):
                if (pygame.mouse.get_pressed()[0]):
                    if (not en_creacion):
                        en_creacion = [pygame.mouse.get_pos()]
                    else:
                        en_creacion.append(pygame.mouse.get_pos())
                        en_creacion.append((255*random.random(), 255*random.random(), 255*random.random()))
                        objetos.append(en_creacion.copy())
                        en_creacion = 0
                    print("Posicion", pygame.mouse.get_pos())
            '''

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    modo = not modo           
        pygame.display.update()
