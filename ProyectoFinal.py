import random,cv2,numpy as np



mapa = np.zeros((30,30), dtype=np.uint8)

nodos = 1 #random.randint(2,10)

grafo = {}

#Mapas

def posicionAleatoria(mapa):
    mx, my = mapa.shape
    mxa = random.randint(0, mx - 1)
    mya = random.randint(0, my - 1)
    mapa[mxa, mya] = 255
    return mxa, mya

def areaNavegable(mapa):
    porcentaje = random.randint(50,70)
    return int(porcentaje/100 * mapa.size)

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
    #salidas['norte'] = [(0, j) for j in range(mapa.shape[1]) if mapa[0, j] == 255]

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
    # salidas['sur'] = [(mapa.shape[0] - 1, j) for j in range(mapa.shape[1]) if mapa[mapa.shape[0] - 1, j] == 255]

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
    #salidas['este'] = [(i, mapa.shape[1] - 1) for i in range(mapa.shape[0]) if mapa[i, mapa.shape[1] - 1] == 255]

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
    #salidas['oeste'] = [(i, 0) for i in range(mapa.shape[0]) if mapa[i, 0] == 255]

    return salidas



#principal

mx, my = posicionAleatoria(mapa)

area = areaNavegable(mapa)

mapas = creacionMapas(nodos,mapa,mx, my, area)

for mapa in mapas.values():
    mapa = cv2.resize(mapa, (600, 600),interpolation=cv2.INTER_NEAREST)
    cv2.imshow('Nueva Imagen',mapa)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

salidas = identificar_salidas(mapa)
print(salidas.keys())