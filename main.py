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

mensaje = ""
tiempo_mensaje = 0

game_over = False
victoria = False

doble_disparo = False
triple_disparo = False
disparo_seis = False
escudo_activo = False

# =========================
# JEFE FINAL
# =========================

boss_activo = False

boss_x = 0
boss_y = 0

boss_spawn_x = 0
boss_spawn_y = 0

boss_target_x = ANCHO // 2
boss_target_y = 100

boss_entrando = False

boss_warning = False
boss_warning_tiempo = 0

boss_direccion_texto = ""
boss_entrada_vel = 2

boss_entrando = False
boss_entrada_vel = 2

boss_radio = 120

boss_vida = 700
boss_vida_max = 700

boss_fase = 1

boss_disparos = []
boss_tiempo_disparo = 0


powerup_vida_aparecio = False
tiempo_powerup_vida = 0

powerup_escudo_aparecio = False
tiempo_powerup_escudo = 0

powerup_doble_aparecio = False
tiempo_powerup_doble = 0

powerup_rojo_aparecio = False
tiempo_powerup_rojo = 0

def reposicionar_boss():
    global boss_x, boss_y

    lado = random.randint(1, 4)

    if lado == 1:
        boss_x = random.randint(0, ANCHO)
        boss_y = 0
    elif lado == 2:
        boss_x = random.randint(0, ANCHO)
        boss_y = ALTO
    elif lado == 3:
        boss_x = 0
        boss_y = random.randint(0, ALTO)
    else:
        boss_x = ANCHO
        boss_y = random.randint(0, ALTO)

    boss_x = max(-200, min(ANCHO + 200, boss_x))
    boss_y = max(-200, min(ALTO + 200, boss_y)) 

def elegir_esquina_boss():
    global boss_spawn_x, boss_spawn_y, boss_direccion_texto

    lado = random.randint(1, 4)

    if lado == 1:
        boss_spawn_x = -200
        boss_spawn_y = -200
        boss_direccion_texto = "TOP LEFT"

    elif lado == 2:
        boss_spawn_x = ANCHO + 200
        boss_spawn_y = -200
        boss_direccion_texto = "TOP RIGHT"

    elif lado == 3:
        boss_spawn_x = -200
        boss_spawn_y = ALTO + 200
        boss_direccion_texto = "BOTTOM LEFT"

    else:
        boss_spawn_x = ANCHO + 200
        boss_spawn_y = ALTO + 200
        boss_direccion_texto = "BOTTOM RIGHT"

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

                if disparo_seis:

                    radianes = math.radians(angulo)

                    apertura = 0.35  # más alto = más abierto

                    offsets = [-2, -1, 0, 1, 2, 3]  # 6 balas

                    for i in offsets:

                        ang = radianes + (i * apertura * 0.2)

                        disparos.append([
                            nave_x,
                            nave_y,
                            math.sin(ang) * velocidad_disparo,
                            -math.cos(ang) * velocidad_disparo
                        ])


                if triple_disparo:

                    radianes = math.radians(angulo)

                    separacion_angulo = 0.15  # apertura del disparo

                    # centro
                    disparos.append([
                        nave_x,
                        nave_y,
                        math.sin(radianes) * velocidad_disparo,
                        -math.cos(radianes) * velocidad_disparo
                    ])

                    # izquierda
                    rad_izq = radianes - separacion_angulo
                    disparos.append([
                        nave_x,
                        nave_y,
                        math.sin(rad_izq) * velocidad_disparo,
                        -math.cos(rad_izq) * velocidad_disparo
                    ])

                    # derecha
                    rad_der = radianes + separacion_angulo
                    disparos.append([
                        nave_x,
                        nave_y,
                        math.sin(rad_der) * velocidad_disparo,
                        -math.cos(rad_der) * velocidad_disparo
                    ])


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

    if not game_over and not victoria:
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
        # DISPAROS DEL BOSS
        # =========================

        for b in boss_disparos:
            b[0] += b[2]
            b[1] += b[3]

        boss_disparos = [
            b for b in boss_disparos
            if 0 < b[0] < ANCHO and 0 < b[1] < ALTO
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
        # MOVIMIENTO DEL JEFE (CORRECTO)
        # =========================

        if boss_activo:

            # 1) ENTRADA INICIAL (desde esquina)
            if boss_entrando:

                dx = boss_target_x - boss_x
                dy = boss_target_y - boss_y

                distancia = math.sqrt(dx**2 + dy**2)

                if distancia != 0:
                    dx /= distancia
                    dy /= distancia

                    boss_x += dx * boss_entrada_vel
                    boss_y += dy * boss_entrada_vel

                if distancia < 5:
                    boss_entrando = False
                    boss_activo_real = True

            # 2) MOVIMIENTO NORMAL (cuando ya entró)
            else:

                # persecución simple a la nave
                dx = nave_x - boss_x
                dy = nave_y - boss_y

                distancia = math.sqrt(dx**2 + dy**2)

                if distancia != 0:
                    dx /= distancia
                    dy /= distancia

                    velocidad_boss = 2.0

                    boss_x += dx * velocidad_boss
                    boss_y += dy * velocidad_boss
        
        # =========================
        # DISPAROS DEL JEFE
        # =========================

        if boss_activo:

            tiempo_actual = pygame.time.get_ticks()

            intervalo = 2000  # cada 2 segundos

            if boss_fase == 2:
                intervalo = 400  # más agresivo

            if tiempo_actual - boss_tiempo_disparo > intervalo:

                dx = nave_x - boss_x
                dy = nave_y - boss_y

                distancia = math.sqrt(dx**2 + dy**2)

                if distancia != 0:
                    dx /= distancia
                    dy /= distancia

                boss_disparos.append([
                    boss_x,
                    boss_y,
                    dx * 3,   # velocidad bala
                    dy * 3
                ])

                boss_tiempo_disparo = tiempo_actual



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
        # COLISION DISPAROS VS BOSS
        # =========================

        if boss_activo:

            disparos_a_boss = []

            for disparo in disparos:

                distancia_boss = math.sqrt(
                    (disparo[0] - boss_x) ** 2 +
                    (disparo[1] - boss_y) ** 2
                )

                if distancia_boss < boss_radio:

                    boss_vida -= 1

                    if boss_fase == 1 and boss_vida <= boss_vida_max * 0.5:
                        boss_fase = 2

                    if boss_vida <= 0:
                        boss_activo = False
                        victoria = True

                    disparos_a_boss.append(disparo)

                for disparo in disparos_a_boss:
                    if disparo in disparos:
                        disparos.remove(disparo)

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
        # COLISION NAVE VS JEFE FINAL
        # =========================

        if boss_activo:

            distancia_boss = math.sqrt(
                (nave_x - boss_x) ** 2 +
                (nave_y - boss_y) ** 2
            )

            if distancia_boss < boss_radio:

                # Si tienes escudo
                if escudo_activo:
                    escudo_activo = False
                else:
                    vidas -= 1

                    if vidas <= 0:
                        vidas = 0
                        game_over = True
                        boss_activo = False

                    else:
                        # mover boss lejos para evitar spawn kill
                        reposicionar_boss()

                    # Reaparecer nave en el centro
                    nave_x = ANCHO // 2
                    nave_y = ALTO // 2

                    velocidad_x = 0
                    velocidad_y = 0

        # =========================
        # COLISION BALAS DEL BOSS
        # =========================

        for b in boss_disparos:

            distancia = math.sqrt(
                (nave_x - b[0]) ** 2 +
                (nave_y - b[1]) ** 2
            )

            if distancia < 10:

                if escudo_activo:
                    escudo_activo = False
                else:
                    vidas -= 1

                    if vidas <= 0:
                        vidas = 0
                        game_over = True
                        boss_activo = False

                boss_disparos.remove(b)
                break
        


    # =========================
    # APARICION POWER UP DOBLE
    # =========================

    if score >= 12500 and not powerup_doble_aparecio:

        powerups.append([
            random.randint(100, ANCHO - 100),
            random.randint(100, ALTO - 100),
            "doble"
        ])

        powerup_doble_aparecio = True

        tiempo_powerup_doble = pygame.time.get_ticks()


    # =========================
    # APARICION POWER UP VIDA
    # =========================

    if score >= 25000 and not powerup_vida_aparecio:

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

    if score >= 35000 and not powerup_escudo_aparecio:

        powerups.append([
            random.randint(100, ANCHO - 100),
            random.randint(100, ALTO - 100),
            "escudo"
        ])

        powerup_escudo_aparecio = True

        tiempo_powerup_escudo = pygame.time.get_ticks()

    # =========================
    # APARICION POWER UP ROJO Triple
    # =========================

    if score >= 50000 and not powerup_rojo_aparecio:

        powerups.append([
            random.randint(100, ANCHO - 100),
            random.randint(100, ALTO - 100),
            "rojo"
        ])

        powerup_rojo_aparecio = True
        tiempo_powerup_rojo = pygame.time.get_ticks()

    # =========================
    # DESAPARECER POWER UP ROJO
    # =========================

    if powerup_rojo_aparecio:

        tiempo_actual = pygame.time.get_ticks()

        if tiempo_actual - tiempo_powerup_rojo > 20000:

            for powerup in powerups:

                if powerup[2] == "rojo":

                    if powerup in powerups:
                        powerups.remove(powerup)

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
    # DESAPARECER POWER UP DOBLE
    # =========================

    if powerup_doble_aparecio:

        tiempo_actual = pygame.time.get_ticks()

        if tiempo_actual - tiempo_powerup_doble > 20000:

            for powerup in powerups:

                if powerup[2] == "doble":

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
    # APARICION JEFE FINAL
    # =========================

    if score >= 100000 and not boss_activo and not boss_entrando:

        boss_activo = True
        boss_entrando = True
        boss_activo_real = False

        elegir_esquina_boss()

        boss_x = boss_spawn_x
        boss_y = boss_spawn_y

        asteroides.clear()
        powerups.clear()

        mensaje = "BOSS INCOMING"
        tiempo_mensaje = pygame.time.get_ticks()

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
                mensaje = "EXTRA LIFE AVAILABLE"
                tiempo_mensaje = pygame.time.get_ticks()

            # Power up doble disparo
            if powerup[2] == "doble":
                doble_disparo = True
                mensaje = "DOUBLE SHOT AVAILABLE"
                tiempo_mensaje = pygame.time.get_ticks()

            # Power up escudo
            if powerup[2] == "escudo":
                escudo_activo = True
                mensaje = "SHIELD AVAILABLE"
                tiempo_mensaje = pygame.time.get_ticks()


            # Power up rojo (nuevo)
            if powerup[2] == "rojo":
                triple_disparo = True
                doble_disparo = False  # opcional: evita conflictos
                disparo_seis = True
                mensaje = "SIX SHOT AVAILABLE"
                tiempo_mensaje = pygame.time.get_ticks()

            powerups_a_eliminar.append(powerup)

    # Eliminar power ups recogidos
    for powerup in powerups_a_eliminar:

        if powerup in powerups:
            powerups.remove(powerup)

    # =========================
    # LIMPIEZA DE MENSAJE
    # =========================

    if mensaje != "":
        if pygame.time.get_ticks() - tiempo_mensaje > 2000:
            mensaje = ""

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

    # =========================
    # DIBUJAR JEFE FINAL
    # =========================

    if boss_activo:

        # Color base (fase 1)
        color_boss = (200, 0, 0)
        borde_boss = (255, 100, 100)

        # FASE 2: enojado (más rojo intenso)
        if boss_fase == 2:
            color_boss = (255, 0, 0)
            borde_boss = (255, 255, 255)  # borde blanco agresivo

        pygame.draw.circle(
            pantalla,
            color_boss,
            (int(boss_x), int(boss_y)),
            boss_radio
        )

        pygame.draw.circle(
            pantalla,
            borde_boss,
            (int(boss_x), int(boss_y)),
            boss_radio,
            4
        )

        # =========================
        # BARRA DE VIDA DEL JEFE
        # =========================

        # Fondo gris
        pygame.draw.rect(
            pantalla,
            (60, 60, 60),
            (ANCHO // 2 - 150, 20, 300, 20)
        )

        # Vida actual (rojo)
        vida_porcentaje = boss_vida / boss_vida_max

        if vida_porcentaje < 0:
            vida_porcentaje = 0

        pygame.draw.rect(
            pantalla,
            (255, 0, 0),
            (ANCHO // 2 - 150, 20, int(300 * vida_porcentaje), 20)
        )


    # Dibujar disparos
    for disparo in disparos:

        pygame.draw.circle(
            pantalla,
            (0, 255, 255),
            (int(disparo[0]), int(disparo[1])),
            3
        )

    for b in boss_disparos:
        pygame.draw.circle(
            pantalla,
            (255, 50, 50),
            (int(b[0]), int(b[1])),
            5
        )

    # Dibujar power ups
    for powerup in powerups:

        color_powerup = (0, 255, 0)

        # Power up rojo
        if powerup[2] == "rojo":
            color_powerup = (255, 0, 0)

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

    if victoria:

        texto_win = fuente.render(
            "YOU WIN!",
            True,
            (0, 255, 0)
        )

        pantalla.blit(
            texto_win,
            (
                ANCHO // 2 - 100,
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


    if mensaje != "":



        texto_mensaje = fuente.render(
            mensaje,
            True,
            (255, 255, 0)
        )

        pantalla.blit(
            texto_mensaje,
            (ANCHO // 2 - 200, 100)
        )

    if boss_warning:

        texto_warning = fuente.render(
            f"BOSS FROM {boss_direccion_texto}",
            True,
            (255, 0, 0)
        )

        pantalla.blit(
            texto_warning,
            (ANCHO // 2 - 180, 200)
        )


    pygame.display.update()

    clock.tick(60)#aaaaaaa f