from src.model import BinaryNode

class AVLTree:
    """Árbol AVL auto-balanceado"""

    def __init__(self):
        self.raiz = None

    def altura(self, nodo):
        if not nodo:
            return 0
        return nodo.altura

    def factor_balance(self, nodo):
        if not nodo:
            return 0
        return self.altura(nodo.izquierdo) - self.altura(nodo.derecho)

    def actualizar_altura(self, nodo):
        if nodo:
            nodo.altura = 1 + max(self.altura(nodo.izquierdo),
                                  self.altura(nodo.derecho))

    def rotar_derecha(self, z):
        y = z.izquierdo
        T3 = y.derecho

        y.derecho = z
        z.izquierdo = T3

        self.actualizar_altura(z)
        self.actualizar_altura(y)

        return y

    def rotar_izquierda(self, z):
        y = z.derecho
        T2 = y.izquierdo

        y.izquierdo = z
        z.derecho = T2

        self.actualizar_altura(z)
        self.actualizar_altura(y)

        return y

    def insertar(self, valor):
        self.raiz = self._insertar_recursivo(self.raiz, valor)

    def _insertar_recursivo(self, nodo, valor):
        if not nodo:
            return BinaryNode(valor)

        if valor < nodo.valor:
            nodo.izquierdo = self._insertar_recursivo(nodo.izquierdo, valor)
        elif valor > nodo.valor:
            nodo.derecho = self._insertar_recursivo(nodo.derecho, valor)
        else:
            return nodo

        self.actualizar_altura(nodo)
        balance = self.factor_balance(nodo)

        # Rotaciones
        if balance > 1 and valor < nodo.izquierdo.valor:
            return self.rotar_derecha(nodo)

        if balance < -1 and valor > nodo.derecho.valor:
            return self.rotar_izquierda(nodo)

        if balance > 1 and valor > nodo.izquierdo.valor:
            nodo.izquierdo = self.rotar_izquierda(nodo.izquierdo)
            return self.rotar_derecha(nodo)

        if balance < -1 and valor < nodo.derecho.valor:
            nodo.derecho = self.rotar_derecha(nodo.derecho)
            return self.rotar_izquierda(nodo)

        return nodo

    def recorrido_inorden(self):
        resultado = []
        self._inorden_recursivo(self.raiz, resultado)
        return resultado

    def _inorden_recursivo(self, nodo, resultado):
        if nodo:
            self._inorden_recursivo(nodo.izquierdo, resultado)
            resultado.append(nodo.valor)
            self._inorden_recursivo(nodo.derecho, resultado)