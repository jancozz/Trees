from src.model.node import Node

class BinaryNode(Node):
    """Nodo para árboles binarios (ABB y AVL)"""
    def __init__(self, valor):
        super().__init__(valor)
        self.izquierdo = None
        self.derecho = None
        self.altura = 1