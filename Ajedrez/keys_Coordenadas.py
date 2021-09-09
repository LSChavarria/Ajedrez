from tablero import coordenadas

def coordenadasToKey(x, y):
    return coordenadas[x][y]

def keyToCoordenadas(key):
    return [(x, y) for x in range(len(coordenadas)) for y in range(len(coordenadas[x])) if coordenadas[x][y] == key][0]