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
# FUENTE Y SCORE
# =========================

fuente = pygame.font.SysFont("Arial", 30)

score = 0
vidas = 3

game_over = False
doble_disparo = False
escudo_activo = False

powerup_vida_aparecio = False
tiempo_powerup_vida = 0

powerup_escudo_aparecio = False
tiempo_powerup_escudo = 0

# =========================
# DATOS DE LA NAVE
# =========================

nave_x = ANCHO // 2
nave_y = ALTO // 2

velocidad_x = 0
velocidad_y = 0

angulo = 0

aceleracion = 0.2 #2
friccion = 0.96 #0.99
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

cantidad_asteroides = 3
for i in range(cantidad_asteroides):

    lado = random.randint(1, 4)

    # Arriba
    if lado == 1:
        x = random.randint(0, ANCHO)
        y = 0

    # Abajo
    elif lado == 2:
        x = random.randint(0, ANCHO)
        y = ALTO

    # Izquierda
    elif lado == 3:
        x = 0
        y = random.randint(0, ALTO)

    # Derecha
    else:
        x = ANCHO
        y = random.randint(0, ALTO)

    velocidad_x_asteroide = random.uniform(-2, 2)
    velocidad_y_asteroide = random.uniform(-2, 2)

    radio = random.randint(20, 40)

    asteroides.append([
        x,
        y,
        velocidad_x_asteroide,
        velocidad_y_asteroide,
        radio,
        1,
        "gris"
    ])

# =========================
# POWER UPS
# =========================

powerups = []

# =========================
# ASTEROIDES ROJOS ELITE
# =========================

for i in range(3):

    lado = random.randint(1, 4)

    # Arriba
    if lado == 1:
        x = random.randint(0, ANCHO)
        y = 0

    # Abajo
    elif lado == 2:
        x = random.randint(0, ANCHO)
        y = ALTO

    # Izquierda
    elif lado == 3:
        x = 0
        y = random.randint(0, ALTO)

    # Derecha
    else:
        x = ANCHO
        y = random.randint(0, ALTO)

    velocidad_x_asteroide = 0
    velocidad_y_asteroide = 0

    radio = random.randint(25, 45)

    asteroides.append([
        x,
        y,
        velocidad_x_asteroide,
        velocidad_y_asteroide,
        radio,
        2,
        "rojo"
    ])


# Crear power up de doble disparo

powerups.append([
    random.randint(100, ANCHO - 100),
    random.randint(100, ALTO - 100),
    "doble"
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

                # =========================
                # DOBLE DISPARO
                # =========================

                if doble_disparo:

                    separacion = 10

                    # Bala izquierda
                    disparos.append([
                        nave_x - math.cos(radianes) * separacion,
                        nave_y - math.sin(radianes) * separacion,
                        math.sin(radianes) * velocidad_disparo,
                        -math.cos(radianes) * velocidad_disparo
                    ])

                    # Bala derecha
                    disparos.append([
                        nave_x + math.cos(radianes) * separacion,
                        nave_y + math.sin(radianes) * separacion,
                        math.sin(radianes) * velocidad_disparo,
                        -math.cos(radianes) * velocidad_disparo
                    ])

                # =========================
                # DISPARO NORMAL
                # =========================

                else:

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

    if not game_over:
        # =========================
        # TECLAS
        # =========================

        teclas = pygame.key.get_pressed()

        # Girar izquierda
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            angulo -= velocidad_rotacion

        # Girar derecha
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            angulo += velocidad_rotacion

        # Acelerar
        if teclas[pygame.K_UP] or teclas[pygame.K_w]:

            radianes = math.radians(angulo)

            velocidad_x += math.sin(radianes) * aceleracion
            velocidad_y -= math.cos(radianes) * aceleracion

        # Retroceder
        if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:

            radianes = math.radians(angulo)

            velocidad_x -= math.sin(radianes) * aceleracion * 0.7
            velocidad_y += math.cos(radianes) * aceleracion * 0.7


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

            # Asteroides rojos perseguidores
            if asteroide[6] == "rojo":

                dx = nave_x - asteroide[0]
                dy = nave_y - asteroide[1]

                distancia = math.sqrt(dx**2 + dy**2)

                if distancia != 0:

                    dx /= distancia
                    dy /= distancia

                    velocidad_persecucion = 1.5
    
                    asteroide[0] += dx * velocidad_persecucion
                    asteroide[1] += dy * velocidad_persecucion

            # Asteroides normales
            else:

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

                    # Quitar vida al asteroide
                    asteroide[5] -= 1

                    # Destruir si ya no tiene vida
                    if asteroide[5] <= 0:

                        asteroides_a_eliminar.append(asteroide)

                        if asteroide[6] == "gris":
                            score += 100

                        if asteroide[6] == "rojo":
                            score += 250

        # Eliminar disparos
        for disparo in disparos_a_eliminar:

            if disparo in disparos:
                disparos.remove(disparo)

        # Eliminar asteroides
        for asteroide in asteroides_a_eliminar:

            if asteroide in asteroides:
                asteroides.remove(asteroide)

                # =========================
                # DIVISION DE ASTEROIDES
                # =========================

                if asteroide[6] == "gris" and asteroide[4] > 39: ################### división

                    for i in range(2):

                        nuevo_radio = asteroide[4] // 2

                        nueva_vel_x = random.uniform(-3, 3)
                        nueva_vel_y = random.uniform(-3, 3)

                        asteroides.append([
                            asteroide[0],
                            asteroide[1],
                            nueva_vel_x,
                            nueva_vel_y,
                            nuevo_radio,
                            1,
                            "gris"
                        ])



                # =========================
                # RESPAWN ASTEROIDES
                # =========================

                # ASTEROIDE GRIS
                if asteroide[6] == "gris":

                    lado = random.randint(1, 4)

                    # Arriba
                    if lado == 1:
                        x = random.randint(0, ANCHO)
                        y = 0

                    # Abajo
                    elif lado == 2:
                        x = random.randint(0, ANCHO)
                        y = ALTO

                    # Izquierda
                    elif lado == 3:
                        x = 0
                        y = random.randint(0, ALTO)

                    # Derecha
                    else:
                        x = ANCHO
                        y = random.randint(0, ALTO)

                    velocidad_x_asteroide = random.uniform(-2, 2)
                    velocidad_y_asteroide = random.uniform(-2, 2)

                    radio = random.randint(20, 40)

                    asteroides.append([
                        x,
                        y,
                        velocidad_x_asteroide,
                        velocidad_y_asteroide,
                        radio,
                        1,
                        "gris"
                    ])

                # ASTEROIDE ROJO PERSEGUIDOR
                if asteroide[6] == "rojo":

                    lado = random.randint(1, 4)

                    # Arriba
                    if lado == 1:
                        x = random.randint(0, ANCHO)
                        y = 0

                    # Abajo
                    elif lado == 2:
                        x = random.randint(0, ANCHO)
                        y = ALTO

                    # Izquierda
                    elif lado == 3:
                        x = 0
                        y = random.randint(0, ALTO)

                    # Derecha
                    else:
                        x = ANCHO
                        y = random.randint(0, ALTO)

                    radio = random.randint(25, 45)

                    asteroides.append([
                        x,
                        y,
                        0,
                        0,
                        radio,
                        2,
                        "rojo"
                    ])

        # =========================
        # COLISION NAVE VS ASTEROIDES
        # =========================

        for asteroide in asteroides:

            distancia_nave = math.sqrt(
                (nave_x - asteroide[0]) ** 2 +
                (nave_y - asteroide[1]) ** 2
            )

            if distancia_nave < asteroide[4] + 10:

                # Escudo absorbe daño
                if escudo_activo:

                    escudo_activo = False

                    # Eliminar asteroide que golpeó
                    if asteroide in asteroides:
                        asteroides.remove(asteroide)

                    break

                else:

                    vidas -= 1

                    if vidas <= 0:
                        game_over = True

                    # Reaparecer nave en el centro
                    nave_x = ANCHO // 2
                    nave_y = ALTO // 2

                    velocidad_x = 0
                    velocidad_y = 0

                    # Reposicionar asteroides
                    for asteroide_actual in asteroides:

                        lado = random.randint(1, 4)

                        # Arriba
                        if lado == 1:
                            asteroide_actual[0] = random.randint(0, ANCHO)
                            asteroide_actual[1] = 0

                        # Abajo
                        elif lado == 2:
                            asteroide_actual[0] = random.randint(0, ANCHO)
                            asteroide_actual[1] = ALTO

                        # Izquierda
                        elif lado == 3:
                            asteroide_actual[0] = 0
                            asteroide_actual[1] = random.randint(0, ALTO)

                        # Derecha
                        else:
                            asteroide_actual[0] = ANCHO
                            asteroide_actual[1] = random.randint(0, ALTO)

                    break


    # =========================
    # APARICION POWER UP VIDA
    # =========================

    if score >= 10000 and not powerup_vida_aparecio:

        powerups.append([
            random.randint(100, ANCHO - 100),
            random.randint(100, ALTO - 100),
            "vida"
        ])

        powerup_vida_aparecio = True

        tiempo_powerup_vida = pygame.time.get_ticks()

    # =========================
    # APARICION POWER UP ESCUDO
    # =========================

    if score >= 15000 and not powerup_escudo_aparecio:

        powerups.append([
            random.randint(100, ANCHO - 100),
            random.randint(100, ALTO - 100),
            "escudo"
        ])

        powerup_escudo_aparecio = True

        tiempo_powerup_escudo = pygame.time.get_ticks()

    # =========================
    # DESAPARECER POWER UP ESCUDO
    # =========================

    if powerup_escudo_aparecio:

        tiempo_actual = pygame.time.get_ticks()

        if tiempo_actual - tiempo_powerup_escudo > 20000:

            for powerup in powerups:

                if powerup[2] == "escudo":

                    if powerup in powerups:
                        powerups.remove(powerup)

    # =========================
    # DESAPARECER POWER UP VIDA
    # =========================

    if powerup_vida_aparecio:

        tiempo_actual = pygame.time.get_ticks()

        if tiempo_actual - tiempo_powerup_vida > 20000:

            for powerup in powerups:

                if powerup[2] == "vida":

                    if powerup in powerups:
                        powerups.remove(powerup)

    # =========================
    # COLISION POWER UPS
    # =========================

    powerups_a_eliminar = []

    for powerup in powerups:

        distancia_powerup = math.sqrt(
            (nave_x - powerup[0]) ** 2 +
            (nave_y - powerup[1]) ** 2
        )

        if distancia_powerup < 20:

            # Power up de vida
            if powerup[2] == "vida":
                vidas += 1

            # Power up doble disparo
            if powerup[2] == "doble":
                doble_disparo = True

            # Power up escudo
            if powerup[2] == "escudo":
                escudo_activo = True

            powerups_a_eliminar.append(powerup)

    # Eliminar power ups recogidos
    for powerup in powerups_a_eliminar:

        if powerup in powerups:
            powerups.remove(powerup)


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
    # ESCUDO VISUAL
    # =========================

    if escudo_activo:

        pygame.draw.circle(
            pantalla,
            (255, 255, 0),
            (int(nave_x), int(nave_y)),
            28,
            3
        )


        # Dibujar asteroides
    for asteroide in asteroides:

        color_asteroide = (180, 180, 180)

        if asteroide[6] == "rojo":
            color_asteroide = (255, 60, 60)

        pygame.draw.circle(
            pantalla,
            color_asteroide,
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

    # Dibujar power ups
    for powerup in powerups:

        color_powerup = (0, 255, 0)

        # Power up doble disparo
        if powerup[2] == "doble":
            color_powerup = (0, 150, 255)

        # Power up escudo
        if powerup[2] == "escudo":
            color_powerup = (255, 255, 0)

        pygame.draw.circle(
            pantalla,
            color_powerup,
            (int(powerup[0]), int(powerup[1])),
            12
        )

    # =========================
    # ACTUALIZAR
    # =========================

    # =========================
    # GAME OVER
    # =========================

    if game_over:

        texto_game_over = fuente.render(
            "GAME OVER",
            True,
            (255, 0, 0)
        )

        pantalla.blit(
            texto_game_over,
            (
                ANCHO // 2 - 120,
                ALTO // 2
            )
        )

        # =========================
        # MOSTRAR SCORE
        # =========================

        texto_score = fuente.render(
            f"Score: {score}",
            True,
            (255, 255, 255)
        )

        pantalla.blit(texto_score, (20, 20))

    texto_vidas = fuente.render(
        f"Vidas: {vidas}",
        True,
        (255, 255, 255)
    )

    pantalla.blit(texto_vidas, (20, 60))

    pygame.display.update()

    clock.tick(60)#aaaaaaa f