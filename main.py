import pygame
import sys
import math
import random

# Inicializar pygame
pygame.init()

# Tamaño de la ventana
ANCHO = 1000
ALTO = 700

# Crear ventana
pantalla = pygame.display.set_mode((ANCHO, ALTO))

# Título de la ventana
pygame.display.set_caption("PyRoids")

# Reloj para controlar FPS
clock = pygame.time.Clock()

# =========================
# DATOS DE LA NAVE
# =========================

nave_x = ANCHO // 2
nave_y = ALTO // 2

velocidad_x = 0
velocidad_y = 0

angulo = 0

aceleracion = 0.2
friccion = 0.99
velocidad_rotacion = 4

# =========================
# DISPAROS
# =========================

disparos = []

velocidad_disparo = 12

# =========================
# ASTEROIDES
# =========================

asteroides = []

cantidad_asteroides = 5
for i in range(cantidad_asteroides):

    x = random.randint(0, ANCHO)
    y = random.randint(0, ALTO)

    velocidad_x_asteroide = random.uniform(-2, 2)
    velocidad_y_asteroide = random.uniform(-2, 2)

    radio = random.randint(20, 40)

    asteroides.append([
        x,
        y,
        velocidad_x_asteroide,
        velocidad_y_asteroide,
        radio
    ])

# =========================
# BUCLE PRINCIPAL
# =========================

while True:

    # =========================
    # EVENTOS
    # =========================

    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
                    # Disparo
        if evento.type == pygame.KEYDOWN:

            if evento.key == pygame.K_SPACE:

                radianes = math.radians(angulo)

                disparo_x = nave_x
                disparo_y = nave_y

                disparo_vel_x = math.sin(radianes) * velocidad_disparo
                disparo_vel_y = -math.cos(radianes) * velocidad_disparo

                disparos.append([
                    disparo_x,
                    disparo_y,
                    disparo_vel_x,
                    disparo_vel_y
                ])

    # =========================
    # TECLAS
    # =========================

    teclas = pygame.key.get_pressed()

    # Girar izquierda
    if teclas[pygame.K_LEFT]:
        angulo += velocidad_rotacion

    # Girar derecha
    if teclas[pygame.K_RIGHT]:
        angulo -= velocidad_rotacion

    # Acelerar
    if teclas[pygame.K_UP]:

        radianes = math.radians(angulo)

        velocidad_x += math.sin(radianes) * aceleracion
        velocidad_y -= math.cos(radianes) * aceleracion

    # =========================
    # MOVIMIENTO
    # =========================

    nave_x += velocidad_x
    nave_y += velocidad_y

    # Fricción espacial leve
    velocidad_x *= friccion
    velocidad_y *= friccion

    # =========================
    # TELETRANSPORTE BORDES
    # =========================

    if nave_x > ANCHO:
        nave_x = 0

    if nave_x < 0:
        nave_x = ANCHO

    if nave_y > ALTO:
        nave_y = 0

    if nave_y < 0:
        nave_y = ALTO

    # =========================
    # ACTUALIZAR DISPAROS
    # =========================

    for disparo in disparos:

        disparo[0] += disparo[2]
        disparo[1] += disparo[3]

    # Eliminar disparos fuera de pantalla
    disparos = [
        disparo for disparo in disparos
        if 0 < disparo[0] < ANCHO
        and 0 < disparo[1] < ALTO
    ]
    
        # =========================
    # ACTUALIZAR ASTEROIDES
    # =========================

    for asteroide in asteroides:

        asteroide[0] += asteroide[2]
        asteroide[1] += asteroide[3]

        # Wrapping horizontal
        if asteroide[0] > ANCHO:
            asteroide[0] = 0

        if asteroide[0] < 0:
            asteroide[0] = ANCHO

        # Wrapping vertical
        if asteroide[1] > ALTO:
            asteroide[1] = 0

        if asteroide[1] < 0:
            asteroide[1] = ALTO
    
    # =========================
    # COLISIONES DISPAROS VS ASTEROIDES
    # =========================

    disparos_a_eliminar = []
    asteroides_a_eliminar = []

    for disparo in disparos:

        for asteroide in asteroides:

            distancia = math.sqrt(
                (disparo[0] - asteroide[0]) ** 2 +
                (disparo[1] - asteroide[1]) ** 2
            )

            if distancia < asteroide[4]:

                disparos_a_eliminar.append(disparo)
                asteroides_a_eliminar.append(asteroide)

    # Eliminar disparos
    for disparo in disparos_a_eliminar:

        if disparo in disparos:
            disparos.remove(disparo)

    # Eliminar asteroides
    for asteroide in asteroides_a_eliminar:

        if asteroide in asteroides:
            asteroides.remove(asteroide)

            # Crear nuevo asteroide
            x = random.randint(0, ANCHO)
            y = random.randint(0, ALTO)

            velocidad_x_asteroide = random.uniform(-2, 2)
            velocidad_y_asteroide = random.uniform(-2, 2)

            radio = random.randint(20, 40)

            asteroides.append([
                x,
                y,
                velocidad_x_asteroide,
                velocidad_y_asteroide,
                radio
            ])

    # =========================
    # DIBUJO
    # =========================

    pantalla.fill((0, 0, 0))

    # Punta de la nave
    radianes = math.radians(angulo)

    punta_x = nave_x + math.sin(radianes) * 20
    punta_y = nave_y - math.cos(radianes) * 20

    # Parte trasera izquierda
    izquierda_x = nave_x + math.sin(radianes + 2.5) * 15
    izquierda_y = nave_y - math.cos(radianes + 2.5) * 15

    # Parte trasera derecha
    derecha_x = nave_x + math.sin(radianes - 2.5) * 15
    derecha_y = nave_y - math.cos(radianes - 2.5) * 15

    # Dibujar triángulo
    pygame.draw.polygon(
        pantalla,
        (255, 255, 255),
        [
            (punta_x, punta_y),
            (izquierda_x, izquierda_y),
            (derecha_x, derecha_y)
        ],
        2
    )

        # Dibujar asteroides
    for asteroide in asteroides:

        pygame.draw.circle(
            pantalla,
            (180, 180, 180),
            (int(asteroide[0]), int(asteroide[1])),
            asteroide[4],
            2
        )

    # Dibujar disparos
    for disparo in disparos:

        pygame.draw.circle(
            pantalla,
            (0, 255, 255),
            (int(disparo[0]), int(disparo[1])),
            3
        )

    # =========================
    # ACTUALIZAR
    # =========================

    pygame.display.update()

    clock.tick(60)#aaaaaaa f