class nodo:
    def __init__(self, valor):
        self.valor = valor
        self.hijos = []

    def agregar_hijo(self, hijo):
        self.hijos.append(hijo)

    def agregar_hijos(self, hijos):
        self.hijos.extend(hijos)

    def imprimir(self, nivel=0):
        texto = "  "*nivel + str(self.valor) + "\n"
        for hijo in self.hijos:
            texto += hijo.imprimir(nivel+1)
        return texto
    
    

class arbol:
    def __init__(self, raiz = None):
        self.raiz = raiz
    
    def establecer_raiz(self, raiz):
        self.raiz = raiz
    
    def imprimir_arbol(self):
        if self.raiz != None:
            print(self.raiz.imprimir())
        else:
            print("El arbol esta vacio")
        

if __name__ == '__main__':
    And = nodo("AND")
    Or = nodo("OR")
    Or.agregar_hijos([And, nodo("E")])
    And.agregar_hijos([nodo("A"), nodo("B"), nodo("C"), nodo("D")])
    Arbol = arbol(Or)
    Arbol.imprimir_arbol()
