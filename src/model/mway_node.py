class MWayNode:
    """Nodo para árbol M-vías"""

    def __init__(self, m):
        self.m = m  # Orden del árbol
        self.valores = []  # Lista de valores (máximo m-1)
        self.hijos = []  # Lista de hijos (máximo m)

    def esta_lleno(self):
        return len(self.valores) >= self.m - 1

    def es_hoja(self):
        return len(self.hijos) == 0