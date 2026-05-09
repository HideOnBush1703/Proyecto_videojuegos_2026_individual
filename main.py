import pygame
import sys

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

# Bucle principal del juego
while True:

    # Revisar eventos
    for evento in pygame.event.get():

        # Cerrar ventana
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Color de fondo (negro)
    pantalla.fill((0, 0, 0))

    # Actualizar pantalla
    pygame.display.update()

    # FPS
    clock.tick(60)