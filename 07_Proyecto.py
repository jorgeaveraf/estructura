import random, cv2, numpy as np, keyboard

mapa = np.zeros((20, 20), dtype=np.uint8)

nodos = random.randint(3, 10)
grafo = {}

# Mapas
def posicionAleatoria(mapa):
    mx, my = mapa.shape
    mxa = random.randint(0, mx - 1)
    mya = random.randint(0, my - 1)
    mapa[mxa, mya] = 255
    return mxa, mya

def porcentajeNavegable(mapa):
    porcentaje = random.randint(60, 85)
    return int(porcentaje / 100 * mapa.size)

def areaNavegable(mapa):
    areanavegable = []
    for i in range(mapa.shape[1]):
        for j in range(mapa.shape[0]):
            if mapa[i, j] == 255:
                areanavegable.append([i, j])
    return areanavegable

def caminoAleatorioMapa(mapa, mxa, mya, area):
    visitadas = []
    visitadas.append([mxa, mya])
    i = 0
    while area > 0:
        direccion = random.randint(1, 4)
        dx, dy = 0, 0
        if direccion == 1 and mxa > 0:
            dx, dy = -1, 0
        elif direccion == 2 and mxa < mapa.shape[0] - 1:
            dx, dy = 1, 0
        elif direccion == 3 and mya > 0:
            dx, dy = 0, -1
        elif direccion == 4 and mya < mapa.shape[1] - 1:
            dx, dy = 0, 1

        if [mxa + dx, mya + dy] not in visitadas:
            mxa += dx
            mya += dy
            mapa[mxa, mya] = 255
            visitadas.append([mxa, mya])
            area -= 1
            i = 0
        else:
            i += 1
            if i >= 10:
                mxa, mya = posicionAleatoria(mapa)
                visitadas.append([mxa, mya])
                area -= 1
                i = 0
    # Asegurar que todas las esquinas sean no navegables
    mapa[0, 0] = mapa[0, -1] = mapa[-1, 0] = mapa[-1, -1] = 0
    return mapa

def creacionMapas(nodos, mapa, mx, my, area):
    mapas = {}
    for i in range(nodos):
        # Inicializar todas las esquinas como no navegables
        mapa[0, 0] = mapa[0, -1] = mapa[-1, 0] = mapa[-1, -1] = 0
        mapa = caminoAleatorioMapa(mapa, mx, my, area)
        mapas[i + 1] = mapa.copy()
        mapa.fill(0)
    return mapas

# Grafo
def preconexion(grafo, nodos, c):
    for i in range(1, nodos + 1):
        grafo[i] = []
        if i != nodos:
            grafo[i].append(i + 1)
    c -= nodos - 1
    return grafo, nodos, c

def conexiones(grafo, nodos, c):
    grafo, nodos, c = preconexion(grafo, nodos, c)
    while c != 0:
        randn = random.randint(1, nodos)
        randc = random.randint(1, nodos)
        if randc in grafo[randn]:
            return c, grafo
        else:
            if randn in grafo[randc]:
                return c, grafo
            else:
                if randc != randn:
                    if len(grafo[randn]) < 3:
                        grafo[randn].append(randc)
                        grafo[randc].append(randn)
                        c -= 1
                    else:
                        c = 0
    return grafo

# Juego
def identificar_salidas(mapa):
    salidas = {}
    nsalidas = 0

    # Norte
    norte_indices = np.where(mapa[0, :] == 255)[0]
    for indice in norte_indices:
        nsalidas += 1
        salidas[nsalidas] = [[0, i] for i in range(indice, mapa.shape[1]) if mapa[0, i] == 255]

    # Este
    este_indices = np.where(mapa[:, -1] == 255)[0]
    for indice in este_indices:
        nsalidas += 1
        salidas[nsalidas] = [[i, mapa.shape[1] - 1] for i in range(indice, mapa.shape[0]) if
                             mapa[i, mapa.shape[1] - 1] == 255]

    # Sur
    sur_indices = np.where(mapa[-1, :] == 255)[0]
    for indice in sur_indices:
        nsalidas += 1
        salidas[nsalidas] = [[mapa.shape[0] - 1, i] for i in range(indice, mapa.shape[1]) if mapa[
            mapa.shape[0] - 1, i] == 255]

    # Oeste
    oeste_indices = np.where(mapa[:, 0] == 255)[0]
    for indice in oeste_indices:
        nsalidas += 1
        salidas[nsalidas] = [[i, 0] for i in range(indice, mapa.shape[0]) if mapa[i, 0] == 255]

    return salidas

def punto_aparicion(mapa, moving_image):
    height, width = mapa.shape
    h, w = moving_image.shape
    while True:
        frame = mapa.copy()
        x, y = random.choice(areaNavegable(mapa))
        y_start, y_end = max(0, y - h // 2), min(height, y + h // 2)
        x_start, x_end = max(0, x - w // 2), min(width, x + w // 2)
        if not (0 in mapa[y_start:y_end, x_start:x_end]):
            return x, y

ESCAPE_KEY = 27
UP_KEY, DOWN_KEY, LEFT_KEY, RIGHT_KEY = 'up', 'down', 'left', 'right'

def jugador(mapa, salidas):
    puntos = 100
    height, width = mapa.shape
    square_size = 20
    moving_image = np.ones((square_size, square_size), dtype=np.uint8) * 127
    h, w = moving_image.shape
    x, y = punto_aparicion(mapa, moving_image)
    prev_x, prev_y = x, y

    while True:
        frame = mapa.copy()
        y_start, y_end = max(0, y - h // 2), min(height, y + h // 2)
        x_start, x_end = max(0, x - w // 2), min(width, x + w // 2)
        frame[y_start:y_end, x_start:x_end] = moving_image[:y_end - y_start, :x_end - x_start]

        for salida, coordenadas in salidas.items():
            esquina_superior_izquierda = [x_start, y_start]
            esquina_superior_derecha = [x_end, y_start]
            esquina_inferior_izquierda = [x_start, y_end]
            esquina_inferior_derecha = [x_end, y_end]
            if (esquina_superior_izquierda in coordenadas or
                    esquina_superior_derecha in coordenadas or
                    esquina_inferior_izquierda in coordenadas or
                    esquina_inferior_derecha in coordenadas):
                print("¡Has tocado una salida! Cambiando de mapa...")
                return True

        cv2.imshow('Mover Cuadrado', frame)
        collision = False  # Flag to check if there's a collision

        for i in range(y_start, y_end):
            for j in range(x_start, x_end):
                if mapa[i, j] == 0:
                    collision = True
                    break
            if collision:
                break

        if collision:
            x, y = prev_x, prev_y

        prev_x, prev_y = x, y

        if keyboard.is_pressed(UP_KEY) and y > h // 2:
            y -= 2
        elif keyboard.is_pressed(DOWN_KEY) and y < height - h // 2:
            y += 2
        elif keyboard.is_pressed(LEFT_KEY) and x > w // 2:
            x -= 2
        elif keyboard.is_pressed(RIGHT_KEY) and x < width - w // 2:
            x += 2

        if collision:
            puntos = puntos_decremento(puntos)
        else:
            puntos = puntos_incremento(puntos)

        if cv2.waitKey(1) & 0xFF == ESCAPE_KEY:
            break

    return False
    

def puntos_incremento(puntos):
    puntos += 1
    return puntos

def puntos_decremento(puntos):
    puntos -= 1
    return puntos

# Principal
mx, my = posicionAleatoria(mapa)
area = porcentajeNavegable(mapa)
mapas = creacionMapas(nodos, mapa, mx, my, area)
grafo = conexiones(grafo, nodos, nodos - 1)

# Imprimir el grafo
print("Grafo:")
for nodo, salidas in grafo.items():
    print(f"Nodo {nodo}: Salidas conectadas a nodos {salidas}")

# Seleccionar el primer mapa
mapa = next(iter(mapas.values()))

mapa = cv2.resize(mapa, (600, 600), interpolation=cv2.INTER_NEAREST)
salidas = identificar_salidas(mapa)
jugador(mapa, salidas)

while True:
    toco_salida = jugador(mapa, salidas)
    if toco_salida:
        if not mapas:
            print("¡Felicidades, has completado todos los mapas!")
            break  # Puedes decidir qué hacer cuando se completan todos los mapas
        else:
            # Eliminar el mapa actual de la colección
            del mapas[next(iter(mapas))]
            
            # Cargar el siguiente mapa
            if mapas:
                mapa = next(iter(mapas.values()))
                mapa = cv2.resize(mapa, (600, 600), interpolation=cv2.INTER_NEAREST)
                salidas = identificar_salidas(mapa)
            else:
                print("¡Felicidades, has completado todos los mapas!")
                break
    if cv2.waitKey(1) & 0xFF == ESCAPE_KEY:  # Verifica si se presiona "esc"
        break
'''

'''