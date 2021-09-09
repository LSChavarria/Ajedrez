class pieza:

    def __init__(self, pieza, color, posicion):
        self.vive = True
        self.pieza = pieza
        self.color = color
        self.posicion = posicion
        self.primerMovimiento = True

    def getPieza(self):
        return self.pieza

    def getEstado(self):
        return self.vive
    
    def getColor(self):
        return self.color
    
    def getPosicion(self):
        return self.posicion
    
    def getPrimerMovimiento(self):
        return self.primerMovimiento
    
    def setEstado(self, estado = False):
        self.vive = estado

    def setPosicion(self, posicion):
        self.posicion = posicion
    
    def setPrimerMovimiento(self, primerMovimiento = False):
        self.primerMovimiento = primerMovimiento

class listPiezas:
    piezas = {}
    
    def nuevaPiezaCoronacion(self, nombre, color, posicion):
        self.agregarPieza(pieza(nombre, color, posicion))
        
    def agregarPieza(self, pieza):
        self.piezas[pieza.getPieza()] = pieza
    
    def getPieza(self, pieza):
        return self.piezas[pieza]
    
    def getListaPiezas(self):
        return self.piezas

lista = listPiezas()
lista.agregarPieza(pieza("R1B", "B", "1E"))
lista.agregarPieza(pieza("D1B", "B", "1D"))
lista.agregarPieza(pieza("T1B", "B", "1A"))
lista.agregarPieza(pieza("T2B", "B", "1H"))
lista.agregarPieza(pieza("A1B", "B", "1C"))
lista.agregarPieza(pieza("A2B", "B", "1F"))
lista.agregarPieza(pieza("C1B", "B", "1B"))
lista.agregarPieza(pieza("C2B", "B", "1G"))
lista.agregarPieza(pieza("P1B", "B", "2A"))
lista.agregarPieza(pieza("P2B", "B", "2B"))
lista.agregarPieza(pieza("P3B", "B", "2C"))
lista.agregarPieza(pieza("P4B", "B", "2D"))
lista.agregarPieza(pieza("P5B", "B", "2E"))
lista.agregarPieza(pieza("P6B", "B", "2F"))
lista.agregarPieza(pieza("P7B", "B", "2G"))
lista.agregarPieza(pieza("P8B", "B", "2H"))
lista.agregarPieza(pieza("R1N", "N", "8E"))
lista.agregarPieza(pieza("D1N", "N", "8D"))
lista.agregarPieza(pieza("T1N", "N", "8A"))
lista.agregarPieza(pieza("T2N", "N", "8H"))
lista.agregarPieza(pieza("A1N", "N", "8C"))
lista.agregarPieza(pieza("A2N", "N", "8F"))
lista.agregarPieza(pieza("C1N", "N", "8B"))
lista.agregarPieza(pieza("C2N", "N", "8G"))
lista.agregarPieza(pieza("P1N", "N", "7A"))
lista.agregarPieza(pieza("P2N", "N", "7B"))
lista.agregarPieza(pieza("P3N", "N", "7C"))
lista.agregarPieza(pieza("P4N", "N", "7D"))
lista.agregarPieza(pieza("P5N", "N", "7E"))
lista.agregarPieza(pieza("P6N", "N", "7F"))
lista.agregarPieza(pieza("P7N", "N", "7G"))
lista.agregarPieza(pieza("P8N", "N", "7H"))