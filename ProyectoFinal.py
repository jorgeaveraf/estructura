import random,cv2,numpy as np, keyboard



mapa = np.zeros((20,20), dtype=np.uint8)

nodos = 1 #random.randint(2,10)

grafo = {}

#Mapas

def posicionAleatoria(mapa):
    mx, my = mapa.shape
    mxa = random.randint(0, mx - 1)
    mya = random.randint(0, my - 1)
    mapa[mxa, mya] = 255
    return mxa, mya

def porcentajeNavegable(mapa):
    porcentaje = random.randint(50,70)
    return int(porcentaje/100 * mapa.size)

def areaNavegable(mapa):
    areanavegable = []
    for i in range(mapa.shape[1]):
        for j in range(mapa.shape[0]):
            if mapa[i,j] == 255:
                areanavegable.append([i,j])
    return areanavegable

def caminoAleatorioMapa(mapa, mxa, mya, area):
    visitadas = []  
    visitadas.append([mxa,mya])  
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
                visitadas.append([mxa,mya])
                area -= 1
                i = 0
        else:
            i+=1
            if i >= 10:
                mxa, mya = posicionAleatoria(mapa)
                visitadas.append([mxa,mya])
                area-=1
                i = 0
    return mapa

def creacionMapas(nodos,mapa,mx, my, area):
    mapas = {}
    for i in range(nodos):
        mapa = caminoAleatorioMapa(mapa, mx, my, area)
        mapas.update({i+1:mapa})
        mapa = np.zeros((mapa.shape[0],mapa.shape[1]), dtype=np.uint8)
    return mapas

#Grafo

def preconexion(grafo,nodos,c):
    for i in range(1,nodos+1):
        grafo[i] = []
        if i != nodos:
            grafo[i].append(i+1)
    c-=nodos-1
    return grafo,nodos,c

def conexiones(grafo,nodos,c):
    grafo,nodos,c = preconexion(grafo,nodos,c)
    while c != 0:
        randn = random.randint(1,nodos)
        randc = random.randint(1,nodos)
        if randc in grafo[randn]:
            return c,grafo
        else:
            if randn in grafo[randc]:
                return c,grafo
            else:
                if randc != randn:
                    if len(grafo[randn]) < 3:
                        grafo[randn].append(randc)
                        c-=1
                    else:
                        c = 0 
    return  grafo

#Juego 
def identificar_salidas(mapa):
    salidas = {}
    nsalidas = 0
    i=0
    # Norte
    while i < mapa.shape[1]:
        if mapa[0, i] == 255 and i < mapa.shape[1]:
            j = i
            nsalidas += 1
            salidas[nsalidas] = []
            while j < mapa.shape[1] and mapa[0, j] == 255:
                salidas[nsalidas].append([0,j ])
                j += 1
            i = j
        else:
            i += 1
    # Este
    i = 0
    while i < mapa.shape[0]:
        if mapa[ i,mapa.shape[1]-1] == 255 and i < mapa.shape[1]:
            j = i
            nsalidas += 1
            salidas[nsalidas] = []
            while j < mapa.shape[1] and mapa[ j,mapa.shape[1]-1] == 255:
                salidas[nsalidas].append([ j,mapa.shape[1]-1 ])
                j += 1
            i = j
        else:
            i += 1
    # Sur
    i = 0
    while i < mapa.shape[1]:
        if mapa[mapa.shape[0] - 1, i] == 255 and i < mapa.shape[1]:
            j = i
            nsalidas += 1
            salidas[nsalidas] = []
            while j < mapa.shape[1] and mapa[mapa.shape[0] - 1, j] == 255:
                salidas[nsalidas].append([mapa.shape[0] - 1,j ])
                j += 1
            i = j
        else:
            i += 1
    # Oeste
    i = 0
    while i < mapa.shape[0]:
        if mapa[ i,0] == 255 and i < mapa.shape[1]:
            j = i
            nsalidas += 1
            salidas[nsalidas] = []
            while j < mapa.shape[1] and mapa[ j,0] == 255:
                salidas[nsalidas].append([ j,0 ])
                j += 1
            i = j
        else:
            i += 1
    return salidas


def jugador(mapa):
    height, width = mapa.shape
    square_size = 5
    moving_image = np.ones((square_size, square_size), dtype=np.uint8) * 127
    h, w = moving_image.shape

    x, y =  random.choice(areaNavegable(mapa))
    prev_x, prev_y = x, y

    while True:
        frame = mapa.copy()

        y_start, y_end = max(0, y - h // 2), min(height, y + h // 2)
        x_start, x_end = max(0, x - w // 2), min(width, x + w // 2)

        frame[y_start:y_end, x_start:x_end] = moving_image[:y_end-y_start, :x_end-x_start]

        cv2.imshow('Mover Cuadrado', frame)

        collision = False  # Flag to check if there's a collision

        # Check for collisions with black pixels in the player's area
        for i in range(y_start, y_end):
            for j in range(x_start, x_end):
                if mapa[i, j] == 0:
                    collision = True
                    break
                if collision:
                    break


        # If there's a collision, revert to the previous position
        if collision:
            x, y = prev_x, prev_y

        prev_x, prev_y = x, y

        if keyboard.is_pressed('up'):
            y -= 1
        elif keyboard.is_pressed('down'):
            y += 1
        elif keyboard.is_pressed('left'):
            x -= 1
        elif keyboard.is_pressed('right'):
            x += 1

        if cv2.waitKey(1) == 27:
            break

    cv2.destroyAllWindows()



#principal

mx, my = posicionAleatoria(mapa)

area = porcentajeNavegable(mapa)

mapas = creacionMapas(nodos,mapa,mx, my, area)

for mapa in mapas.values():
    mapa = cv2.resize(mapa, (600, 600),interpolation=cv2.INTER_NEAREST)
    jugador(mapa)
    
