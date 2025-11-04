from src.model import MWayNode

class MWayTree:
    """Árbol M-vías"""

    def __init__(self, m):
        if m < 3:
            raise ValueError("El orden debe ser al menos 3")
        self.m = m
        self.raiz = None

    def insertar(self, valor):
        if self.raiz is None:
            self.raiz = MWayNode(self.m)
            self.raiz.valores.append(valor)
        else:
            self._insertar_recursivo(self.raiz, valor)

    def _insertar_recursivo(self, nodo, valor):
        # Buscar posición de inserción
        i = 0
        while i < len(nodo.valores) and valor > nodo.valores[i]:
            i += 1

        # Si el valor ya existe
        if i < len(nodo.valores) and valor == nodo.valores[i]:
            return

        # Si es hoja, insertar directamente
        if nodo.es_hoja():
            nodo.valores.insert(i, valor)
        else:
            # Insertar en el hijo correspondiente
            if i < len(nodo.hijos):
                self._insertar_recursivo(nodo.hijos[i], valor)

    def buscar(self, valor):
        return self._buscar_recursivo(self.raiz, valor)

    def _buscar_recursivo(self, nodo, valor):
        if nodo is None:
            return False

        i = 0
        while i < len(nodo.valores) and valor > nodo.valores[i]:
            i += 1

        if i < len(nodo.valores) and valor == nodo.valores[i]:
            return True

        if nodo.es_hoja():
            return False

        if i < len(nodo.hijos):
            return self._buscar_recursivo(nodo.hijos[i], valor)

        return False

    def recorrido_inorden(self):
        resultado = []
        self._inorden_recursivo(self.raiz, resultado)
        return resultado

    def _inorden_recursivo(self, nodo, resultado):
        if nodo is None:
            return

        for i in range(len(nodo.valores)):
            if i < len(nodo.hijos):
                self._inorden_recursivo(nodo.hijos[i], resultado)
            resultado.append(nodo.valores[i])

        if len(nodo.hijos) > len(nodo.valores):
            self._inorden_recursivo(nodo.hijos[-1], resultado)