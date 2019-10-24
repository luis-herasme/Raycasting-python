import math
import random
import pygame
import rotar
import renderizador
from utils import getTexture
from vector import add, sub, mult, punto, normalizar

# Constants
WIDTH = 800
RAYOS_AMT = 200
CAMPO_VISTA = math.pi / 4
DELT_ANG = CAMPO_VISTA / RAYOS_AMT
SIZE_TALL = 25
LINEWIDTH = int(WIDTH / RAYOS_AMT)
SPEED = 100
ANGLE_SPEED = 2
SCREEN = pygame.display.set_mode((WIDTH, WIDTH))

def plane_rendering(position, distancias, camera, objetos, rayos):
    '''
    Renderiza en modo plano
    '''
    pygame.draw.rect(SCREEN, (0, 0, 0), (0, 0, WIDTH, WIDTH))
    for i in range(RAYOS_AMT):
        pygame.draw.line(
            SCREEN,
            (0, 0, 255),
            (int(position[0]), int(position[1])),
            (int(position[0] + rayos[i][0] * distancias[i]),
             int(position[1] + rayos[i][1] * distancias[i]))
        )

    pygame.draw.circle(SCREEN, (255, 255, 255), (int(position[0]), int(position[1])), 5)
    renderizador.draw(objetos, SCREEN, pygame)
    pygame.draw.line(
        SCREEN,
        (255, 0, 255),
        (int(position[0]), int(position[1])),
        (int(position[0] + camera[0] * 20), int(position[1] + camera[1] * 20)),
        3
    )

def raycasting(rayos, camera, distancias, atibutos, eses):
    '''
    raycasting de la escena
    '''
    pygame.draw.rect(SCREEN, (135, 206, 235), (0, 0, WIDTH, WIDTH/2))
    pygame.draw.rect(SCREEN, (0, 100, 0), (0, WIDTH/2, WIDTH, WIDTH/2))

    for i, val in enumerate(distancias):
        val *= punto(rayos[i], camera)

    for i in range(RAYOS_AMT):
        if not atibutos[i] is None:
            if not atibutos[i]["textured"]:
                pygame.draw.rect(
                    SCREEN,
                    atibutos[i]["color"],
                    pygame.Rect(
                        (LINEWIDTH + 1) * i,
                        (WIDTH - SIZE_TALL * (WIDTH / distancias[i])) / 2,
                        LINEWIDTH + 1,
                        SIZE_TALL * WIDTH / distancias[i]
                    )
                )
            elif atibutos[i]["textured"]:
                lon = len(atibutos[i]["texture"][0])
                index = math.floor(eses[i] * lon)
                for pixel in range(len(atibutos[i]["texture"][index])):
                    if not atibutos[i]["texture"][index][pixel][3] == 0:
                        k = SIZE_TALL * WIDTH / distancias[i]
                        pygame.draw.rect(
                            SCREEN,
                            atibutos[i]["texture"][index][pixel],
                            pygame.Rect(
                                (LINEWIDTH + 1) * i,
                                pixel * k / lon + ((WIDTH - k)/2),
                                LINEWIDTH + 1,
                                (k / lon) + 1)
                            )
def calcular_rayos(camera):
    '''
    Calcula la direccion de cada rayo
    '''
    rayos = [0] * RAYOS_AMT
    rayo = rotar.rot(camera, -CAMPO_VISTA / 2)
    for i in range(RAYOS_AMT):
        rayos[i] = rotar.rot(rayo, DELT_ANG * i)
    return rayos

def update_enemy(position, malo_pos, delta_time, camera):
    '''
    Actualiza el estado de la calabaza
    '''
    vertex = [0, 0]
    malo_velocity = mult(normalizar(sub(position, malo_pos)), SPEED * 0.25 * delta_time)
    orientacion = rotar.rot(camera, math.pi / 2)
    malo_pos = add(malo_pos, malo_velocity)
    vertex[0] = add(malo_pos, mult(orientacion, 12.5))
    vertex[1] = add(malo_pos, mult(orientacion, -12.5))
    return (vertex, malo_pos)

def hadle_events(rayos, delta_time, objetos, modo, en_creacion, position, camera):
    '''
    Manejador de eventos
    '''
    en_creacion = en_creacion
    rayos = rayos
    running = True
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        camera = rotar.rot(camera, -ANGLE_SPEED * delta_time)
        rayos = calcular_rayos(camera)
    elif keys[pygame.K_RIGHT]:
        #OPTIMAZACION ROTAR RAYOS SOLO CUANDO ROTA LA CAMARA
        camera = rotar.rot(camera, ANGLE_SPEED * delta_time)
        rayos = calcular_rayos(camera)
    elif keys[pygame.K_UP]:
        position = add(position, mult(camera, SPEED * delta_time))
    elif keys[pygame.K_DOWN]:
        position = sub(position, mult(camera, SPEED * delta_time))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                if not en_creacion:
                    en_creacion = {
                        "vertex": [pygame.mouse.get_pos(), 0],
                        "color": (100, 100, 255),
                        "textured": False
                    }
                else:
                    en_creacion["vertex"][1] = pygame.mouse.get_pos()
                    en_creacion["color"] = (
                        random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
                    )
                    objetos.append(en_creacion.copy())
                    en_creacion = 0
                print("Posicion", pygame.mouse.get_pos())

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                modo = not modo
    return (modo, running, rayos, en_creacion, position, camera)

def main():
    '''
    Main function
    '''
    position = (200, 200)
    malo_pos = (200, 100)
    camera = (0, -1)
    modo = True
    en_creacion = 0
    clock = pygame.time.Clock()

    objetos = [
        {
            "vertex": [(100, 300), (100, 325)],
            "color": (100, 100, 255),
            "textured": False
        },
        {
            "vertex": [(200, 100), (225, 100)],
            "color": (0, 255, 0),
            "textured": True,
            "texture": getTexture('wall.png')
        },
        {
            "vertex": [(200, 50), (225, 50)],
            "color": (0, 255, 0),
            "textured": True,
            "texture": getTexture('malo.png')
        },
        {
            "vertex": [(300, 100), (325, 100)],
            "color": (0, 255, 0),
            "textured": True,
            "texture": getTexture('tree.png')
        },
        {
            "vertex": [(100, 200), (100, 225)],
            "color": (0, 255, 0),
            "textured": True,
            "texture": getTexture('tree.png')
        },
        {
            "vertex": [(100, 100), (125, 100)],
            "color": (255, 0, 0),
            "textured": True,
            "texture": getTexture('mario.png')
        }
    ]

    pygame.display.flip()
    rayos = calcular_rayos(camera)
    running = True
    while running:
        delta_time = clock.tick() / 1000
        # Manejar la calabaza
        (objetos[2]["vertex"], malo_pos) = update_enemy(position, malo_pos, delta_time, camera)
        # Todos los datos de renderizado
        (distancias, atibutos, eses) = renderizador.render(rayos, position, objetos)
        # Dibujar plano
        if modo:
            plane_rendering(position, distancias, camera, objetos, rayos)
        # Raycasting
        else:
            raycasting(rayos, camera, distancias, atibutos, eses)
        (modo, running, rayos, en_creacion, position, camera) = hadle_events(
            rayos, delta_time, objetos, modo, en_creacion, position, camera
        )
        pygame.display.update()

if __name__ == '__main__':
    main()
