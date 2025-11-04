from src.model import ABBTree
from src.model import AVLTree
from src.model import MWayTree

class TreeController:
    """Controlador para gestionar las operaciones de los árboles"""

    def __init__(self):
        self.arbol_actual = None
        self.tipo_arbol = None

    def crear_arbol(self, tipo, orden=None):
        """
        Crea un nuevo árbol según el tipo especificado
        tipo: 'ABB', 'AVL', 'MVIAS'
        orden: requerido solo para M-VIAS
        """
        self.tipo_arbol = tipo

        if tipo == 'ABB':
            self.arbol_actual = ABBTree()
        elif tipo == 'AVL':
            self.arbol_actual = AVLTree()
        elif tipo == 'MVIAS':
            if orden is None or orden < 3:
                raise ValueError("Para árbol M-vías se requiere un orden >= 3")
            self.arbol_actual = MWayTree(orden)
        else:
            raise ValueError(f"Tipo de árbol no reconocido: {tipo}")

        return True

    def insertar_valor(self, valor):
        """Inserta un valor en el árbol actual"""
        if self.arbol_actual is None:
            raise Exception("Primero debe crear un árbol")

        try:
            valor_numerico = int(valor)
            self.arbol_actual.insertar(valor_numerico)
            return True
        except ValueError:
            raise ValueError("El valor debe ser un número entero")

    def insertar_multiples(self, valores_texto):
        """Inserta múltiples valores separados por comas"""
        if self.arbol_actual is None:
            raise Exception("Primero debe crear un árbol")

        valores = [v.strip() for v in valores_texto.split(',')]
        insertados = []
        errores = []

        for valor in valores:
            try:
                valor_numerico = int(valor)
                self.arbol_actual.insertar(valor_numerico)
                insertados.append(valor_numerico)
            except ValueError:
                errores.append(f"'{valor}' no es un número válido")

        return insertados, errores

    def obtener_niveles_y_nodos_espejo(self):
        if self.arbol_actual is None:
            return set(), 0
        return self.arbol_actual.obtener_niveles_espejo()

    def buscar_valor(self, valor):
        """Busca un valor en el árbol actual"""
        if self.arbol_actual is None:
            raise Exception("Primero debe crear un árbol")

        try:
            valor_numerico = int(valor)

            if self.tipo_arbol in ['ABB', 'AVL']:
                resultado = self.arbol_actual.buscar(valor_numerico)
                return resultado is not None
            else:  # MVIAS
                return self.arbol_actual.buscar(valor_numerico)
        except ValueError:
            raise ValueError("El valor debe ser un número entero")

    def obtener_recorrido_inorden(self):
        """Obtiene el recorrido inorden del árbol"""
        if self.arbol_actual is None:
            return []

        return self.arbol_actual.recorrido_inorden()

    def obtener_arbol(self):
        """Retorna el árbol actual para visualización"""
        return self.arbol_actual

    def limpiar_arbol(self):
        """Limpia el árbol actual"""
        if self.arbol_actual and self.tipo_arbol:
            if self.tipo_arbol == 'MVIAS':
                orden = self.arbol_actual.m
                self.crear_arbol(self.tipo_arbol, orden)
            else:
                self.crear_arbol(self.tipo_arbol)
        else:
            self.arbol_actual = None
            self.tipo_arbol = None

    def obtener_tipo_arbol(self):
        """Retorna el tipo de árbol actual"""
        return self.tipo_arbol

    def obtener_info_arbol(self):
        """Obtiene información del árbol actual"""
        if self.arbol_actual is None:
            return {
                'tipo': None,
                'elementos': 0,
                'raiz': None
            }

        recorrido = self.obtener_recorrido_inorden()
        info = {
            'tipo': self.tipo_arbol,
            'elementos': len(recorrido),
            'raiz': None
        }

        if self.arbol_actual.raiz:
            if self.tipo_arbol == 'MVIAS':
                info['raiz'] = self.arbol_actual.raiz.valores[0] if self.arbol_actual.raiz.valores else None
            else:
                info['raiz'] = self.arbol_actual.raiz.valor
        return info