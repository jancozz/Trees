import customtkinter as ctk
from tkinter import Canvas

class TreeCanvas(ctk.CTkFrame):
    """Canvas personalizado para dibujar árboles (compatible con CustomTkinter)"""

    def __init__(self, parent, width=850, height=600, **kwargs):
        super().__init__(parent, fg_color='#1a1a1a', **kwargs)

        # Configuración de dimensiones
        self.canvas_width = width
        self.canvas_height = height
        self.radio_nodo = 20
        self.separacion_horizontal = 60
        self.separacion_vertical = 80

        # Colores para tema oscuro
        self.color_fondo = '#1a1a1a'
        self.color_texto = '#ffffff'
        self.color_linea = '#666666'
        self.color_nodo_binario = '#2E7D32'
        self.color_nodo_binario_borde = '#1B5E20'
        self.color_nodo_mvias = '#1565C0'
        self.color_nodo_mvias_borde = '#0D47A1'

        # Crear scrollbars
        self.scrollbar_v = ctk.CTkScrollbar(self, orientation="vertical", bg_color='#2b2b2b')
        self.scrollbar_h = ctk.CTkScrollbar(self, orientation="horizontal", bg_color='#2b2b2b')

        # Crear canvas con scrollbars
        self.canvas = ctk.CTkCanvas(
            self,
            bg=self.color_fondo,
            highlightthickness=0,
            yscrollcommand=self.scrollbar_v.set,
            xscrollcommand=self.scrollbar_h.set,
            width=width,
            height=height
        )

        # Configurar scrollbars
        self.scrollbar_v.configure(command=self.canvas.yview)
        self.scrollbar_h.configure(command=self.canvas.xview)

        # Layout con grid
        self.canvas.grid(row=0, column=0, sticky='nsew')
        self.scrollbar_v.grid(row=0, column=1, sticky='ns')
        self.scrollbar_h.grid(row=1, column=0, sticky='ew')

        # Configurar peso de filas y columnas
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Bind para zoom con rueda del mouse (opcional)
        self.canvas.bind('<Control-MouseWheel>', self._zoom)

        # Variables para el árbol actual
        self.arbol_actual = None
        self.tipo_actual = None

    def _zoom(self, event):
        """Zoom con Ctrl + rueda del mouse"""
        if event.delta > 0:
            # Zoom in
            self.canvas.scale("all", event.x, event.y, 1.1, 1.1)
        else:
            # Zoom out
            self.canvas.scale("all", event.x, event.y, 0.9, 0.9)

        # Actualizar región de scroll
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def limpiar(self):
        """Limpia el canvas"""
        self.canvas.delete('all')
        self.arbol_actual = None
        self.tipo_actual = None

    def dibujar_arbol(self, arbol, tipo):
        """Dibuja el árbol según su tipo"""
        self.limpiar()
        self.arbol_actual = arbol
        self.tipo_actual = tipo

        if arbol is None or arbol.raiz is None:
            self.canvas.create_text(self.canvas_width // 2, self.canvas_height // 2,
                                    text="Árbol vacío", font=('Arial', 14),
                                    fill='#888888')
            return

        if tipo in ['ABB', 'AVL']:
            self._dibujar_arbol_binario(arbol.raiz)
        elif tipo == 'MVIAS':
            self._dibujar_arbol_mvias(arbol.raiz, arbol.m)

        # Actualizar región de scroll para incluir todo el contenido
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

        # Añadir padding a la región de scroll
        bbox = self.canvas.bbox("all")
        if bbox:
            padding = 50
            self.canvas.configure(scrollregion=(
                bbox[0] - padding,
                bbox[1] - padding,
                bbox[2] + padding,
                bbox[3] + padding
            ))

    def _dibujar_arbol_binario(self, raiz):
        """Dibuja un árbol binario (ABB o AVL)"""
        if raiz is None:
            return

        # Calcular profundidad del árbol
        profundidad = self._calcular_profundidad_binario(raiz)

        # Ancho inicial basado en la profundidad (más espacio para árboles grandes)
        ancho_inicial = max((2 ** profundidad) * self.separacion_horizontal, 800)

        # Dibujar desde la raíz en el centro horizontal del espacio calculado
        x_inicial = ancho_inicial // 2 + 100  # Offset adicional
        y_inicial = 40

        self._dibujar_nodo_binario(raiz, x_inicial, y_inicial,
                                   ancho_inicial // 2, 1, profundidad)

    def _dibujar_nodo_binario(self, nodo, x, y, offset, nivel, max_nivel):
        """Dibuja un nodo binario y sus hijos recursivamente"""
        if nodo is None:
            return

        # Dibujar hijos primero (para que las líneas queden detrás)
        nuevo_offset = max(offset // 2, self.separacion_horizontal // 2)

        if nodo.izquierdo:
            x_izq = x - offset
            y_hijo = y + self.separacion_vertical
            # Línea al hijo izquierdo
            self.canvas.create_line(x, y, x_izq, y_hijo,
                                    fill=self.color_linea, width=2, tags="line")
            self._dibujar_nodo_binario(nodo.izquierdo, x_izq, y_hijo,
                                       nuevo_offset, nivel + 1, max_nivel)

        if nodo.derecho:
            x_der = x + offset
            y_hijo = y + self.separacion_vertical
            # Línea al hijo derecho
            self.canvas.create_line(x, y, x_der, y_hijo,
                                    fill=self.color_linea, width=2, tags="line")
            self._dibujar_nodo_binario(nodo.derecho, x_der, y_hijo,
                                       nuevo_offset, nivel + 1, max_nivel)

        # Dibujar el nodo actual
        self.canvas.create_oval(x - self.radio_nodo, y - self.radio_nodo,
                                x + self.radio_nodo, y + self.radio_nodo,
                                fill=self.color_nodo_binario,
                                outline=self.color_nodo_binario_borde, width=2,
                                tags="node")

        self.canvas.create_text(x, y, text=str(nodo.valor),
                                font=('Arial', 12, 'bold'), fill=self.color_texto,
                                tags="text")

    def _calcular_profundidad_binario(self, nodo):
        """Calcula la profundidad de un árbol binario"""
        if nodo is None:
            return 0

        izq = self._calcular_profundidad_binario(nodo.izquierdo)
        der = self._calcular_profundidad_binario(nodo.derecho)

        return 1 + max(izq, der)

    def _dibujar_arbol_mvias(self, raiz, m):
        """Dibuja un árbol M-vías"""
        if raiz is None:
            return

        # Calcular profundidad y ancho necesario
        profundidad = self._calcular_profundidad_mvias(raiz)
        ancho_necesario = self._calcular_ancho_mvias(raiz, m)

        # Posición inicial con más espacio
        x_inicial = max(ancho_necesario // 2, 400)
        y_inicial = 40

        ancho_nivel = max(ancho_necesario, 800)

        self._dibujar_nodo_mvias(raiz, x_inicial, y_inicial,
                                 ancho_nivel, 1, profundidad, m)

    def _calcular_ancho_mvias(self, nodo, m):
        """Calcula el ancho necesario para el árbol M-vías"""
        if nodo is None or nodo.es_hoja():
            return len(nodo.valores) * self.radio_nodo * 2 if nodo else 0

        ancho_hijos = sum(self._calcular_ancho_mvias(hijo, m) for hijo in nodo.hijos)
        return max(ancho_hijos, len(nodo.valores) * self.radio_nodo * 2)

    def _dibujar_nodo_mvias(self, nodo, x, y, ancho, nivel, max_nivel, m):
        """Dibuja un nodo M-vías y sus hijos"""
        if nodo is None:
            return

        # Calcular ancho del nodo basado en cantidad de valores
        num_valores = len(nodo.valores)
        ancho_nodo = (num_valores + 1) * self.radio_nodo * 2

        # Dibujar hijos primero
        if not nodo.es_hoja():
            num_hijos = len(nodo.hijos)
            espacio_entre_hijos = max(ancho / max(num_hijos, 1), 100)

            for i, hijo in enumerate(nodo.hijos):
                x_hijo = x - ancho / 2 + espacio_entre_hijos * (i + 0.5)
                y_hijo = y + self.separacion_vertical

                # Línea al hijo
                self.canvas.create_line(x, y + self.radio_nodo,
                                        x_hijo, y_hijo - self.radio_nodo,
                                        fill=self.color_linea, width=2, tags="line")

                nuevo_ancho = espacio_entre_hijos * 0.8
                self._dibujar_nodo_mvias(hijo, x_hijo, y_hijo,
                                         nuevo_ancho, nivel + 1, max_nivel, m)

        # Dibujar el nodo (rectángulo con compartimentos)
        x_inicio = x - ancho_nodo // 2

        for i, valor in enumerate(nodo.valores):
            x_compartimento = x_inicio + i * self.radio_nodo * 2

            # Rectángulo del compartimento
            self.canvas.create_rectangle(x_compartimento, y - self.radio_nodo,
                                         x_compartimento + self.radio_nodo * 2,
                                         y + self.radio_nodo,
                                         fill=self.color_nodo_mvias,
                                         outline=self.color_nodo_mvias_borde, width=2,
                                         tags="node")

            # Valor
            self.canvas.create_text(x_compartimento + self.radio_nodo, y,
                                    text=str(valor), font=('Arial', 10, 'bold'),
                                    fill=self.color_texto, tags="text")

    def _calcular_profundidad_mvias(self, nodo):
        """Calcula la profundidad de un árbol M-vías"""
        if nodo is None or nodo.es_hoja():
            return 1

        max_prof = 0
        for hijo in nodo.hijos:
            prof = self._calcular_profundidad_mvias(hijo)
            max_prof = max(max_prof, prof)

        return 1 + max_prof

    def pack(self, **kwargs):
        """Override pack para el frame"""
        super().pack(**kwargs)

    def grid(self, **kwargs):
        """Override grid para el frame"""
        super().grid(**kwargs)