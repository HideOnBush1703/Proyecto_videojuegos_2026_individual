import pygame
import sys
import math

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

    # =========================
    # ACTUALIZAR
    # =========================

    pygame.display.update()

    clock.tick(60)