class Node:
    """Clase base para nodos de árbol"""

    def __init__(self, valor):
        self.valor = valor

    def __str__(self):
        return str(self.valor)