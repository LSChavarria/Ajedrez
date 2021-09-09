from clases.Piezas import lista
from tablero import tablero

def imprimitEstados():
    piezas = lista.getListaPiezas()
    vivosBlancos = []
    vivosNegros = []
    muertosBlancos = []
    muertosNegros = []
    for x in piezas.values():
        if x.getEstado():
            if x.getColor() == "B":
                vivosBlancos.append(x.getPieza())
            else:
                vivosNegros.append(x.getPieza())
        else:
            if x.getColor() == "B":
                muertosBlancos.append(x.getPieza())
            else:
                muertosNegros.append(x.getPieza())
    print("\nVivos blancos: ", vivosBlancos)
    print("Vivos negors: ", vivosNegros)
    print("\nMuertos blancos: ", muertosBlancos)
    print("Muertos negros: ", muertosNegros)
    print("\n")

def imprimirTablero():
    i = 0
    j = 8
    salida = "  -------------------------------------------------\n8 | "
    for x in tablero.values():
        i += 1
        salida = salida + x + " | "
        if i == 8:
            j -= 1
            salida = salida + "\n  -------------------------------------------------\n" + str(j) + " | "
            i = 0
    salida = salida[:-4]
    salida += "     A     B     C     D     E     F     G     H\n"
    print(salida)