from src.model import BinaryNode
from collections import deque

class ABBTree:
    """Árbol Binario de Búsqueda"""

    def __init__(self):
        self.raiz = None

    def insertar(self, valor):
        if self.raiz is None:
            self.raiz = BinaryNode(valor)
        else:
            self._insertar_recursivo(self.raiz, valor)

    def _insertar_recursivo(self, nodo, valor):
        if valor < nodo.valor:
            if nodo.izquierdo is None:
                nodo.izquierdo = BinaryNode(valor)
            else:
                self._insertar_recursivo(nodo.izquierdo, valor)
        elif valor > nodo.valor:
            if nodo.derecho is None:
                nodo.derecho = BinaryNode(valor)
            else:
                self._insertar_recursivo(nodo.derecho, valor)

    # def cant_niveles_espejo(self):
    #     if self.raiz is None:
    #         return 0
    #
    #     niveles = set()
    #     self._verificar_niveles_espejo(self.raiz.izquierdo, self.raiz.derecho, 1, niveles)
    #     return len(niveles)
    #
    # def cantidad_nodos_espejo(self):
    #     if self.raiz is None:
    #         return 0
    #
    #     niveles = set()
    #     contador = [0]  # Usamos lista para que sea mutable
    #     self._verificar_niveles_espejo(self.raiz.izquierdo, self.raiz.derecho, 1, niveles, contador)
    #     return contador[0]
    #
    # def niveles_espejo(self):
    #     if self.raiz is None:
    #         return []
    #
    #     niveles = set()
    #     self._verificar_niveles_espejo(self.raiz.izquierdo, self.raiz.derecho, 1, niveles)
    #     return niveles
    #
    # def _verificar_niveles_espejo(self, nodo1, nodo2, nivel, niveles, contador=None):
    #     if nodo1 is None and nodo2 is None:
    #         return True
    #     if nodo1 is not None and nodo2 is not None:
    #         izq = self._verificar_niveles_espejo(nodo1.izquierdo, nodo2.derecho, nivel + 1, niveles, contador)
    #         der = self._verificar_niveles_espejo(nodo1.derecho, nodo2.izquierdo, nivel + 1, niveles, contador)
    #
    #         if izq and der:
    #             niveles.add(nivel)
    #             if contador is not None:
    #                 contador[0] += 2  # nodo1 y nodo2 son simétricos
    #             return True
    #     return False

    def _estructura_espejo(self, nodo1, nodo2):
        if nodo1 is None and nodo2 is None:
            return True
        if nodo1 is None or nodo2 is None:
            return False

        return (
                self._estructura_espejo(nodo1.izquierdo, nodo2.derecho) and
                self._estructura_espejo(nodo1.derecho, nodo2.izquierdo)
        )

    def obtener_niveles_espejo(self):
        if self.raiz is None:
            return set(), 0

        niveles_simetricos = set()
        cantidad_nodos_simetricos = 0

        cola1 = deque([self.raiz.izquierdo])
        cola2 = deque([self.raiz.derecho])
        nivel = 1

        while cola1 and cola2:
            nivel_nodos1 = list(cola1)
            nivel_nodos2 = list(cola2)

            if len(nivel_nodos1) != len(nivel_nodos2):
                break

            espejo = True
            hay_nodos = False

            for i in range(len(nivel_nodos1)):
                n1 = nivel_nodos1[i]
                n2 = nivel_nodos2[-(i + 1)]

                if (n1 is None) != (n2 is None):
                    espejo = False
                    break
                if n1 and n2:
                    cantidad_nodos_simetricos += 2
                    hay_nodos = True

            if espejo and hay_nodos:
                niveles_simetricos.add(nivel)
            else:
                break

            siguiente1 = deque()
            siguiente2 = deque()
            for n1 in cola1:
                if n1:
                    siguiente1.append(n1.izquierdo)
                    siguiente1.append(n1.derecho)
            for n2 in cola2:
                if n2:
                    siguiente2.append(n2.derecho)
                    siguiente2.append(n2.izquierdo)

            cola1 = siguiente1
            cola2 = siguiente2
            nivel += 1

        return niveles_simetricos, cantidad_nodos_simetricos

    def buscar(self, valor):
        return self._buscar_recursivo(self.raiz, valor)

    def _buscar_recursivo(self, nodo, valor):
        if nodo is None or nodo.valor == valor:
            return nodo
        if valor < nodo.valor:
            return self._buscar_recursivo(nodo.izquierdo, valor)
        return self._buscar_recursivo(nodo.derecho, valor)

    def recorrido_inorden(self):
        resultado = []
        self._inorden_recursivo(self.raiz, resultado)
        return resultado

    def _inorden_recursivo(self, nodo, resultado):
        if nodo:
            self._inorden_recursivo(nodo.izquierdo, resultado)
            resultado.append(nodo.valor)
            self._inorden_recursivo(nodo.derecho, resultado)
