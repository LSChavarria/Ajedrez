# AJEDREZ
# Primero ingresa la pieza que quieres mover con mayusculas como aparece en el tablero (por ejemplo A1B)
# Si deseas hacer enroque corto en lugar de la pieza ingresa O-O (es la letra o no cero)
# Si deseas hacer enroque largo en lugar de la pieza ingresa O-O-O (es la letra O en mayuscula no cero)
# En caso de no ser enroque se te pedira la posicion a la que debes mover la pieza (por ejemplo 1A)

from tablero import inicializarTablero, tablero
from movimientos import controller
from imprimir import imprimirTablero, imprimitEstados
from clases.Piezas import lista

jugada = []
inicializarTablero()
imprimirTablero()
cont = 0
while True:
    if cont % 2 == 0:
        color = "B"
    else: 
        color = "N"
    print("Ingresa tu pieza: ")
    pieza = input()
    if pieza == "R":
        if color == "B":
            print("Blancas se rinden")
        else:
            print("Negras se rinden")
        imprimirTablero()
        imprimitEstados()
        break
    if pieza == "O-O" or pieza == "O-O-O":
        if controller(pieza, color):
            imprimirTablero()
            imprimitEstados()
            jugada.append([pieza, color])
            cont += 1
        else:
            print("Enroque invalido")
        continue
    try:
        lista.getPieza(pieza)
    except:
        print("Pieza invalida")
        continue
    if pieza[2] != color:
        print("Pieza invalida")
        continue
    print("Ingresa la casilla donde la moveras: ")
    posicion = input()
    try:
        tablero[posicion]
    except:
        print("Posicion invalida")
        continue
    movimientoValido, jaqueMate = controller(pieza, posicion)
    if movimientoValido:
        imprimirTablero()
        imprimitEstados()
        jugada.append([pieza, posicion])
        cont += 1
        if jaqueMate:
            for i in jugada:
                print(i)
            break

# Partida de ejemplo
"""
['P4N', '5D']
['P3B', '4C']
['P5N', '6E']
['C1B', '3C']
['A2N', '7E']
['C2B', '3F']
['C2N', '6F']
['A1B', '5G']
['P8N', '6H']
['A1B', '4H']
['O-O', 'N']
['P5B', '3E']
['P2N', '6B']
['A1B', '6F']
['A2N', '6F']
['P3B', '5D']
['P5N', '5D']
['D1B', '2D']
['A1N', '6E']
['T1B', '1D']
['D1N', '7E']
['P7B', '3G']
['P3N', '5C']
['P4B', '5C']
['T2N', '8D']
['P4B', '6B']
['P5N', '4D']
['A2B', '2G']
['C1N', '6C']
['C2B', '4D']
['C1N', '4D']
['P5B', '4D']
['A1N', '3H']
['R1B', '1F']
['T2N', '4D']
['D1B', '3E']
['D1N', '7B']
['P6B', '3F']
['T2N', '1D']
['C1B', '1D']
['D1N', '6A']
['R1B', '1G']
['T1N', '8D']
['C1B', '2F']
['A2N', '4D']
['D1B', '1E']
['A2N', '2F']
['D1B', '2F']
['T1N', '1D']
['A2B', '1F']
['D1N', '1F']
['D1B', '1F']
['T1N', '1F']
['P1B', '3A']
['T1N', '1G']
"""