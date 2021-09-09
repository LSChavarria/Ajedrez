from clases.Piezas import lista 
from tablero import tablero, coordenadas
from keys_Coordenadas import *

contCoronacionesBlancas = 2
contCoronacionesNegras = 2
permitirCapturaAlPaso = False
contPermitirCapturaAlPaso = 0

def bloqueado(x, y):
    #print("tablero[coordenadasToKey(x,y)]: ", coordenadasToKey(x,y), " : ", tablero[coordenadasToKey(x,y)])
    return tablero[coordenadasToKey(abs(x),abs(y))] != "..."

def coronacion(posActual, posAnterior):
    global contCoronacionesBlancas
    global contCoronacionesNegras
    p = tablero[coordenadasToKey(*posAnterior)]
    lista.getPieza(p).setEstado()
    color = lista.getPieza(p).getColor()
    if color == "B":
        contCoronacionesBlancas += 1
        contadorNeutro = contCoronacionesBlancas
    else:
        contCoronacionesNegras += 1
        contadorNeutro = contCoronacionesNegras
    nombre = "D" + str(contadorNeutro) + color
    lista.nuevaPiezaCoronacion(nombre, color, coordenadasToKey(*posActual))
    tablero[coordenadasToKey(*posAnterior)] = nombre

def capturaAlPaso(posActual, posAnterior, aux):
    x = posActual[0] - 1 * aux
    y = posActual[1]
    if bloqueado(x, y):
        pVictima = lista.getPieza(tablero[coordenadasToKey(x, y)])
        pAtacante = lista.getPieza(tablero[coordenadasToKey(*posAnterior)])
        if pVictima.getColor() != pAtacante.getColor():
            pVictima.setEstado()
            tablero[coordenadasToKey(x, y)] = "..."
            return True
    return False

def bloqueadoTorre(posActual, posAnterior):
    v = posActual[0] - posAnterior[0]
    h = posActual[1] - posAnterior[1]
    if v != 0:
        if v > 0:
            posicion = posAnterior
        else:
            posicion = posActual
        for i in range(abs(v)):
            if i == 0:
                continue
            if bloqueado(posicion[0] + i, posicion[1]):
                return False, [posicion[0] + i, posicion[1]]
    else:
        if h > 0:
            posicion = posAnterior
        else:
            posicion = posActual
        for i in range(abs(h)):
            if i == 0:
                continue
            if bloqueado(posicion[0], posicion[1] + i):
                return False, [posicion[0], posicion[1] + i]
    return True, []

def bloqueadoAlfil(posActual, posAnterior):
    v = posActual[0] - posAnterior[0]
    h = posActual[1] - posAnterior[1]
    if (v > 0 and h > 0)  or (v < 0 and h < 0):
        if v > 0 and h > 0:
            posicion = posAnterior
        else:
            posicion = posActual
        for i in range(abs(v)):
            if i == 0:
                continue
            if bloqueado(posicion[0] + i, posicion[1] + i):
                return False, [posicion[0] + i, posicion[1] + i]
    else: 
        if v < 0 and h > 0:
            posicion = posAnterior
        else:
            posicion = posActual
        for i in range(abs(v)):
            if i == 0:
                continue
            if bloqueado(posicion[0] - i, posicion[1] + i):
                return False, [posicion[0] - i, posicion[1] + i]
    return True, []

def bloqueadoPeon(posActual, posAnterior): #Retorna true si esta libre el paso
    if bloqueado(*posActual):
        return False, posActual
    return True, []

def noJaqueRectasPrimeraRevision(posAnterior, color):
    if bloqueado(*posAnterior):
        p = lista.getPieza(tablero[coordenadasToKey(*posAnterior)])
        if p.getColor() != color:
            tipoPieza = p.getPieza()[0]
            if tipoPieza == "T" or tipoPieza == "D":
                return True
        return False
                
def noJaqueRectas(posActual, posAnterior, color):
    jaque = []
    v = posActual[0] - posAnterior[0]
    h = posActual[1] - posAnterior[1]
    if v == 0 and h == 0:
        return False
    if v > 0 or h > 0:
        jaque.append(noJaqueRectasPrimeraRevision(posAnterior, color))
        posConst = posActual
        posVar = posAnterior
    else:
        posConst = posAnterior
        posVar = posActual
    while posVar != []:
        libre, posicionBloqueada = bloqueadoTorre(posConst, posVar)
        if posicionBloqueada != []:
            p = lista.getPieza(tablero[coordenadasToKey(*posicionBloqueada)])
        if not libre:
            colorBloquea = p.getColor()
            if color != colorBloquea:
                tipoPieza = p.getPieza()[0]
                if tipoPieza == "T" or tipoPieza == "D":
                    jaque.append(True)
            else:
                jaque.append(False)
        posVar = posicionBloqueada
    if v > 0 or h > 0:
        return jaque[-1]
    else:
        jaque.append(noJaqueRectasPrimeraRevision(posAnterior, color))
        return jaque[0]

def noJaqueCaballo(posAnterior, color):
    if posAnterior[0] < 0 or posAnterior[0] > 7:
        return False
    if posAnterior[1] < 0 or posAnterior[1] > 7:
        return False
    if bloqueado(*posAnterior):
        p = lista.getPieza(tablero[coordenadasToKey(*posAnterior)])
        if p.getPieza()[0] == "C":
            if p.getColor() != color:
                return True
    return False

def noJaqueDiagonalesRevision(posActual, color):
    p = lista.getPieza(tablero[coordenadasToKey(*posActual)])
    if p.getColor() != color:
        if p.getPieza()[0] == "A" or p.getPieza()[0] == "D":
            return True
    return False

def noJaqueDiagonales(posActual, color):
    posAuxiliar = posActual
    while posAuxiliar[0] + 1 <= 7 and posAuxiliar[1] + 1 <= 7:
        posAuxiliar = [posAuxiliar[0] + 1, posAuxiliar[1] + 1]
        if bloqueado(*posAuxiliar):
            if noJaqueDiagonalesRevision(posAuxiliar, color):
                return True
            else:
                break 
    posAuxiliar = posActual
    while posAuxiliar[0] + 1 <= 7 and posAuxiliar[1] - 1 >= 0:
        posAuxiliar = [posAuxiliar[0] + 1, posAuxiliar[1] - 1]
        if bloqueado(*posAuxiliar):
            if noJaqueDiagonalesRevision(posAuxiliar, color):
                return True
            else:
                break 
    posAuxiliar = posActual
    while posAuxiliar[0] - 1 >= 0 and posAuxiliar[1] + 1 <= 7:
        posAuxiliar = [posAuxiliar[0] - 1, posAuxiliar[1] + 1]
        if bloqueado(*posAuxiliar):
            if noJaqueDiagonalesRevision(posAuxiliar, color):
                return True
            else:
                break 
    posAuxiliar = posActual
    while posAuxiliar[0] - 1 >= 0 and posAuxiliar[1] - 1 >= 0:
        posAuxiliar = [posAuxiliar[0] - 1, posAuxiliar[1] - 1]
        if bloqueado(*posAuxiliar):
            if noJaqueDiagonalesRevision(posAuxiliar, color):
                return True
            else:
                break 
    return False

def noJaquePeonRevision(posActual, color):
    p = lista.getPieza(tablero[coordenadasToKey(*posActual)])
    if p.getColor() != color:
        if p.getPieza()[0] == "P":
            return True
    return False

def noJaquePeon(posActual, color):
    if color == "B":
        aux = 1
    else:
        aux = -1
    posAuxiliar = [posActual[0] + 1 * aux, posActual[1] + 1]
    if posAuxiliar[0] >= 0 and posAuxiliar[0] <= 7:
        if posAuxiliar[1] >= 0 and posAuxiliar[1] <= 7:
            if bloqueado(*posAuxiliar):
                if noJaquePeonRevision(posAuxiliar, color):
                    return True
    posAuxiliar = [posActual[0] + 1 * aux, posActual[1] - 1]
    if posAuxiliar[0] >= 0 and posAuxiliar[0] <= 7:
        if posAuxiliar[1] >= 0 and posAuxiliar[1] <= 7:
            if bloqueado(*posAuxiliar):
                if noJaquePeonRevision(posAuxiliar, color):
                    return True
    return False
    
def noJaqueRey(posActual, color):
    if posActual[0] >= 0 and posActual[0] <= 7:
        if posActual[1] >= 0 and posActual[1] <= 7:
            if bloqueado(*posActual):
                p = lista.getPieza(tablero[coordenadasToKey(*posActual)])
                if p.getColor() != color:
                    if p.getPieza()[0] == "R":
                        return True
    return False

def noJaque(posActual, color):
    posAnterior = []
    posAnterior.append([posActual[0], 0])
    posAnterior.append([posActual[0], 7])
    posAnterior.append([0, posActual[1]])
    posAnterior.append([7, posActual[1]])
    for i in posAnterior:
        if noJaqueRectas(posActual, i, color):
            return True
    posAnterior = []
    posAnterior.append([posActual[0] + 1, posActual[1] + 2])
    posAnterior.append([posActual[0] + 2, posActual[1] + 1])
    posAnterior.append([posActual[0] + 1, posActual[1] - 2])
    posAnterior.append([posActual[0] + 2, posActual[1] - 1])
    posAnterior.append([posActual[0] - 1, posActual[1] + 2])
    posAnterior.append([posActual[0] - 2, posActual[1] + 1])
    posAnterior.append([posActual[0] - 1, posActual[1] - 2])
    posAnterior.append([posActual[0] - 2, posActual[1] - 1])
    for i in posAnterior:
        if noJaqueCaballo(i, color):
            return True
    posAnterior = []
    if noJaqueDiagonales(posActual, color):
        return True
    if noJaquePeon(posActual, color):
        return True
    posAnterior.append([posActual[0] + 1, posActual[1]])
    posAnterior.append([posActual[0] + 1, posActual[1] + 1])
    posAnterior.append([posActual[0] + 1, posActual[1] - 1])
    posAnterior.append([posActual[0] - 1, posActual[1]])
    posAnterior.append([posActual[0] - 1, posActual[1] + 1])
    posAnterior.append([posActual[0] - 1, posActual[1] - 1])
    posAnterior.append([posActual[0], posActual[1] + 1])
    posAnterior.append([posActual[0], posActual[1] - 1])
    for i in posAnterior:
        if noJaqueRey(i, color):
            return True
    posAnterior = []
    return False

def torre(posActual, posAnterior):
    posActual = keyToCoordenadas(posActual)
    posAnterior = keyToCoordenadas(posAnterior)
    if posActual[0] == posAnterior[0] and posActual[1] != posAnterior[1]:
        if bloqueadoTorre(posActual, posAnterior)[0]:
            return True
    if posActual[0] != posAnterior[0] and posActual[1] == posAnterior[1]:
        if bloqueadoTorre(posActual, posAnterior)[0]:
            return True
    return False

def alfil(posActual, posAnterior):
    posActual = keyToCoordenadas(posActual)
    posAnterior = keyToCoordenadas(posAnterior)
    v = abs(posActual[0] - posAnterior[0])
    h = abs(posActual[1] - posAnterior[1])
    if v == h:
        if bloqueadoAlfil(posActual, posAnterior)[0]:
            return True
    return False

def dama(posActual, posAnterior):
    if alfil(posActual, posAnterior):
        return True
    if torre(posActual, posAnterior):
        return True
    return False

def caballo(posActual, posAnterior):
    posActual = keyToCoordenadas(posActual)
    posAnterior = keyToCoordenadas(posAnterior)
    v = abs(posActual[0] - posAnterior[0])
    h = abs(posActual[1] - posAnterior[1])
    if v == 2 and h == 1:
        return True
    if v == 1 and h == 2:
        return True
    return False

def peon(posActual, posAnterior, color):
    global permitirCapturaAlPaso
    global contPermitirCapturaAlPaso
    if color == "B":
        aux = 1
    else:
        aux = -1
    posActual = keyToCoordenadas(posActual)
    posAnterior = keyToCoordenadas(posAnterior)
    v = posActual[0] - posAnterior[0]
    h = posActual[1] - posAnterior[1]
    if v == 1 * aux and posActual[1] == posAnterior[1]:
        if bloqueadoPeon(posActual, posAnterior)[0]:
            if color == "B":
                if posActual[0] == 7:
                    coronacion(posActual, posAnterior)
            else:
                if posActual[0] == 0:
                    coronacion(posActual, posAnterior)
            return True
    if v == 1 * aux and abs(h) == 1:
        if bloqueado(*posActual):
            if color == "B":
                if posActual[0] == 7:
                    coronacion(posActual, posAnterior)
            else:
                if posActual[0] == 0:
                    coronacion(posActual, posAnterior)
            return True
        if permitirCapturaAlPaso:
            return capturaAlPaso(posActual, posAnterior, aux)
    p = lista.getPieza(tablero[coordenadasToKey(*posAnterior)])
    if p.getPrimerMovimiento():
        p.setPrimerMovimiento()
        if bloqueado(*posActual):
            return False
        guardarPosicion = posActual
        posActualArray = [posActual[0], posActual[1]]
        posActualArray[0] -= 1 * aux
        if peon(coordenadasToKey(*posActualArray), coordenadasToKey(*posAnterior), p.getColor()):
            posAnterior = posActualArray
            posActual = guardarPosicion
            if peon(coordenadasToKey(*posActual), coordenadasToKey(*posAnterior), p.getColor()):
                permitirCapturaAlPaso = True
                contPermitirCapturaAlPaso = 0
                return True
    return False

def rey(posActual, posAnterior, color):
    posActual = keyToCoordenadas(posActual)
    posAnterior = keyToCoordenadas(posAnterior)
    v = abs(posActual[0] - posAnterior[0])
    h = abs(posActual[1] - posAnterior[1])
    if v == 1 and h == 0:
        if not noJaque(posActual, color):
            return True
    if v == 0 and h == 1:
        if not noJaque(posActual, color):
            return True
    if v == 1 and h == 1:
        if not noJaque(posActual, color):
            return True
    return False

def movimiento(pieza, posicion):
    global permitirCapturaAlPaso
    global contPermitirCapturaAlPaso
    jaqueMate = False
    piezas = lista.getListaPiezas()
    posAnterior = piezas[pieza].getPosicion()
    aux = True
    if bloqueado(*keyToCoordenadas(posicion)):
        aux = piezas[pieza].getColor() != piezas[tablero[posicion]].getColor()
    if aux and piezas[pieza].getEstado():
        if pieza[0] == "T":
            movimientoValido = torre(posicion, posAnterior)
            if movimientoValido:
                print("Movimiento valido torre")
            else:
                print("Movimiento invalido torre")
        if pieza[0] == "A":
            movimientoValido = alfil(posicion, posAnterior)
            if movimientoValido:
                print("Movimiento valido alfil")
            else:
                print("Movimiento invalido alfil")
        if pieza[0] == "D":
            movimientoValido = dama(posicion, posAnterior)
            if movimientoValido:
                print("Movimiento valido dama")
            else:
                print("Movimiento invalido dama")
        if pieza[0] == "C":
            movimientoValido = caballo(posicion, posAnterior)
            if movimientoValido:
                print("Movimiento valido caballo")
            else:
                print("Movimiento invalido caballo")
        if pieza[0] == "P":
            movimientoValido = peon(posicion, posAnterior, piezas[pieza].getColor())
            if movimientoValido:
                print("Movimiento valido peon")
            else:
                print("Movimiento invalido peon")
        if pieza[0] == "R":
            movimientoValido = rey(posicion, posAnterior, piezas[pieza].getColor())
            if movimientoValido:
                print("Movimiento valido rey")
            else:
                print("Movimiento invalido rey")
        if movimientoValido:
            if tablero[posicion] == "R1N" or tablero[posicion] == "R1B":
                print("Jaque mate!!!")
                jaqueMate = True
            if tablero[posicion] != "...":
                piezas[tablero[posicion]].setEstado(False)
            piezas[pieza].setPrimerMovimiento()
            piezas[pieza].setPosicion(posicion)
            tablero[posicion] = tablero[posAnterior]
            tablero[posAnterior] = "..."
            if contPermitirCapturaAlPaso == 1:
                permitirCapturaAlPaso = False
            contPermitirCapturaAlPaso += 1
            return True, jaqueMate
        else:
            return False, False
    else:
        print("Movimiento invalido pieza amiga o muertaS")
        return False, False

def enroqueCorto(color):
    print("enroqueCorto")
    rey = lista.getPieza("R1" + color)
    torre = lista.getPieza("T2" + color)
    posicion1 = [keyToCoordenadas(rey.getPosicion())[0], 5]
    posicion2 = [keyToCoordenadas(rey.getPosicion())[0], 6]
    auxR = rey.getPosicion()
    auxT = torre.getPosicion()
    if not rey.getPrimerMovimiento():
        print("rey ya se habia movido")
        return False
    if not torre.getPrimerMovimiento():
        print("torre ya se habia movido")
        return False
    if bloqueado(*posicion1) or bloqueado(*posicion2):
        print("bloqueado")
        return False
    if noJaque(posicion1, color):
        print(coordenadasToKey(*posicion1), " esta en jaque")
        return False
    if noJaque(posicion2, color):
        print(coordenadasToKey(*posicion2), " esta en jaque")
        return False
    rey.setPrimerMovimiento()
    torre.setPrimerMovimiento()
    rey.setPosicion(coordenadasToKey(*posicion2))
    torre.setPosicion(coordenadasToKey(*posicion1))
    tablero[coordenadasToKey(*posicion2)] = rey.getPieza()
    tablero[coordenadasToKey(*posicion1)] = torre.getPieza()
    tablero[auxR] = "..."
    tablero[auxT] = "..."
    return True

def enroqueLargo(color):
    print("enroqueLargo")
    rey = lista.getPieza("R1" + color)
    torre = lista.getPieza("T1" + color)
    posicion1 = [keyToCoordenadas(rey.getPosicion())[0], 3]
    posicion2 = [keyToCoordenadas(rey.getPosicion())[0], 2]
    posicion3 = [keyToCoordenadas(rey.getPosicion())[0], 1]
    auxR = keyToCoordenadas(rey.getPosicion())
    auxT = keyToCoordenadas(torre.getPosicion())
    if not rey.getPrimerMovimiento():
        print("rey ya se habia movido")
        return False
    if not torre.getPrimerMovimiento():
        print("torre ya se habia movido")
        return False
    if bloqueado(*posicion1) or bloqueado(*posicion2) or bloqueado(*posicion3):
        print("bloqueado")
        return False
    if noJaque(posicion1, color):
        print(coordenadasToKey(*posicion1), " esta en jaque")
        return False
    if noJaque(posicion2, color):
        print(coordenadasToKey(*posicion2), " esta en jaque")
        return False
    rey.setPrimerMovimiento()
    torre.setPrimerMovimiento()
    rey.setPosicion(coordenadasToKey(*posicion2))
    torre.setPosicion(coordenadasToKey(*posicion1))
    tablero[coordenadasToKey(*posicion2)] = rey.getPieza()
    tablero[coordenadasToKey(*posicion1)] = torre.getPieza()
    tablero[auxR] = "..."
    tablero[auxT] = "..."
    return True

def controller(pieza, posicion_color):
    if pieza == "O-O":
        return enroqueCorto(posicion_color)
    if pieza == "O-O-O":
        return enroqueLargo(posicion_color)
    return movimiento(pieza, posicion_color)
        
