import customtkinter as ctk
from tkinter import messagebox
from controller.tree_controller import TreeController
from view.tree_canvas import TreeCanvas
from model import ABBTree

class MainWindow:
    """Ventana principal de la aplicación"""

    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Gestor de Árboles - ABB, AVL y M-VÍAS")
        self.root.geometry("1200x700")

        self.controller = TreeController()
        self.canvas_arbol = None

        self._crear_interfaz()

    def _crear_interfaz(self):
        """Crea todos los elementos de la interfaz"""

        # Frame principal dividido en dos columnas
        main_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Columna izquierda - Controles
        left_frame = ctk.CTkFrame(main_frame, width=350, corner_radius=10)
        left_frame.pack(side="left", fill="both", padx=(0, 10))
        left_frame.pack_propagate(False)

        # Columna derecha - Visualización
        right_frame = ctk.CTkFrame(main_frame, corner_radius=10)
        right_frame.pack(side="right", fill="both", expand=True)

        self._crear_panel_controles(left_frame)
        self._crear_panel_visualizacion(right_frame)

    def _crear_panel_controles(self, parent):
        """Crea el panel de controles"""

        # Sección: Crear Árbol
        frame_crear = ctk.CTkFrame(parent, corner_radius=8)
        frame_crear.pack(fill="x", padx=15, pady=(0, 15))

        label_crear = ctk.CTkLabel(frame_crear, text="Crear Árbol",
                                   font=ctk.CTkFont(size=14, weight="bold"))
        label_crear.pack(pady=(10, 10), padx=10, anchor="w")

        ctk.CTkLabel(frame_crear, text="Tipo de árbol:").pack(anchor='w', padx=10)

        self.tipo_var = ctk.StringVar(value='ABB')

        radio_abb = ctk.CTkRadioButton(frame_crear, text="Árbol Binario de Búsqueda (ABB)",
                                       variable=self.tipo_var, value='ABB',
                                       command=self._toggle_orden)
        radio_abb.pack(anchor='w', padx=20, pady=2)

        radio_avl = ctk.CTkRadioButton(frame_crear, text="Árbol AVL",
                                       variable=self.tipo_var, value='AVL',
                                       command=self._toggle_orden)
        radio_avl.pack(anchor='w', padx=20, pady=2)

        radio_mvias = ctk.CTkRadioButton(frame_crear, text="Árbol M-VÍAS",
                                         variable=self.tipo_var, value='MVIAS',
                                         command=self._toggle_orden)
        radio_mvias.pack(anchor='w', padx=20, pady=2)

        # Orden para M-VÍAS
        self.frame_orden = ctk.CTkFrame(frame_crear, fg_color="transparent")
        self.frame_orden.pack(fill="x", padx=10, pady=(5, 0))

        ctk.CTkLabel(self.frame_orden, text="Orden (M):").pack(side="left", padx=(10, 5))
        self.orden_var = ctk.StringVar(value='3')
        self.entry_orden = ctk.CTkEntry(self.frame_orden, width=60,
                                        textvariable=self.orden_var)
        self.entry_orden.pack(side="left")

        self.frame_orden.pack_forget()  # Ocultar inicialmente

        btn_crear = ctk.CTkButton(frame_crear, text="Crear Árbol",
                                  command=self._crear_arbol,
                                  fg_color="#2E7D32", hover_color="#1B5E20",
                                  font=ctk.CTkFont(size=13, weight="bold"),
                                  height=35, corner_radius=8)
        btn_crear.pack(pady=(15, 15), padx=10, fill="x")

        # Sección: Insertar Valores
        frame_insertar = ctk.CTkFrame(parent, corner_radius=8)
        frame_insertar.pack(fill="x", padx=15, pady=(0, 15))

        label_insertar = ctk.CTkLabel(frame_insertar, text="Insertar Valores",
                                      font=ctk.CTkFont(size=14, weight="bold"))
        label_insertar.pack(pady=(10, 10), padx=10, anchor="w")

        ctk.CTkLabel(frame_insertar, text="Valor único:").pack(anchor='w', padx=10)
        self.entry_valor = ctk.CTkEntry(frame_insertar, placeholder_text="Ingrese un número")
        self.entry_valor.pack(fill="x", padx=10, pady=(0, 5))
        self.entry_valor.bind('<Return>', lambda e: self._insertar_valor())

        btn_insertar = ctk.CTkButton(frame_insertar, text="Insertar",
                                     command=self._insertar_valor,
                                     fg_color="#1565C0", hover_color="#0D47A1",
                                     font=ctk.CTkFont(size=13, weight="bold"),
                                     height=32, corner_radius=8)
        btn_insertar.pack(fill="x", padx=10, pady=(0, 10))

        ctk.CTkLabel(frame_insertar, text="Múltiples valores (separados por comas):").pack(
            anchor='w', padx=10, pady=(5, 0))
        self.entry_multiples = ctk.CTkEntry(frame_insertar,
                                            placeholder_text="ej: 50,30,70,20,40")
        self.entry_multiples.pack(fill="x", padx=10, pady=(0, 5))
        self.entry_multiples.bind('<Return>', lambda e: self._insertar_multiples())

        btn_insertar_mult = ctk.CTkButton(frame_insertar, text="Insertar Múltiples",
                                          command=self._insertar_multiples,
                                          fg_color="#1565C0", hover_color="#0D47A1",
                                          font=ctk.CTkFont(size=13, weight="bold"),
                                          height=32, corner_radius=8)
        btn_insertar_mult.pack(fill="x", padx=10, pady=(0, 15))

        # Sección: Buscar
        frame_buscar = ctk.CTkFrame(parent, corner_radius=8)
        frame_buscar.pack(fill="x", padx=15, pady=(0, 15))

        label_buscar = ctk.CTkLabel(frame_buscar, text="Buscar Valor",
                                    font=ctk.CTkFont(size=14, weight="bold"))
        label_buscar.pack(pady=(10, 10), padx=10, anchor="w")

        ctk.CTkLabel(frame_buscar, text="Valor a buscar:").pack(anchor='w', padx=10)
        self.entry_buscar = ctk.CTkEntry(frame_buscar, placeholder_text="Ingrese un número")
        self.entry_buscar.pack(fill="x", padx=10, pady=(0, 5))
        self.entry_buscar.bind('<Return>', lambda e: self._buscar_valor())

        btn_buscar = ctk.CTkButton(frame_buscar, text="Buscar",
                                   command=self._buscar_valor,
                                   fg_color="#F57C00", hover_color="#E65100",
                                   font=ctk.CTkFont(size=13, weight="bold"),
                                   height=32, corner_radius=8)
        btn_buscar.pack(fill="x", padx=10, pady=(0, 15))

        # Sección: Información
        frame_info = ctk.CTkFrame(parent, corner_radius=8)
        frame_info.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        label_info = ctk.CTkLabel(frame_info, text="Información del Árbol",
                                  font=ctk.CTkFont(size=14, weight="bold"))
        label_info.pack(pady=(10, 10), padx=10, anchor="w")

        # Usar CTkTextbox en lugar de scrolledtext
        self.texto_info = ctk.CTkTextbox(frame_info, height=150,
                                         font=ctk.CTkFont(family="Courier", size=11),
                                         corner_radius=5)
        self.texto_info.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # Botón Limpiar
        btn_limpiar = ctk.CTkButton(parent, text="Limpiar Árbol",
                                    command=self._limpiar_arbol,
                                    fg_color="#C62828", hover_color="#B71C1C",
                                    font=ctk.CTkFont(size=13, weight="bold"),
                                    height=35, corner_radius=8)
        btn_limpiar.pack(fill="x", padx=15, pady=(0, 15))

    def _crear_panel_visualizacion(self, parent):
        """Crea el panel de visualización del árbol"""

        titulo = ctk.CTkLabel(parent, text="Visualización del Árbol",
                              font=ctk.CTkFont(size=18, weight="bold"))
        titulo.pack(pady=15)

        # Frame para el canvas
        canvas_frame = ctk.CTkFrame(parent, corner_radius=8, fg_color="#1a1a1a")
        canvas_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        # Canvas para dibujar el árbol
        self.canvas_arbol = TreeCanvas(canvas_frame, width=850, height=600)
        self.canvas_arbol.pack(fill="both", expand=True, padx=5, pady=5)

    def _toggle_orden(self):
        """Muestra u oculta el campo de orden según el tipo de árbol"""
        if self.tipo_var.get() == 'MVIAS':
            self.frame_orden.pack(fill="x", padx=10, pady=(5, 0))
        else:
            self.frame_orden.pack_forget()

    def _crear_arbol(self):
        """Crea un nuevo árbol"""
        tipo = self.tipo_var.get()

        try:
            if tipo == 'MVIAS':
                orden = int(self.orden_var.get())
                self.controller.crear_arbol(tipo, orden)
            else:
                self.controller.crear_arbol(tipo)

            self.canvas_arbol.limpiar()
            self._actualizar_info()
            messagebox.showinfo("Éxito", f"Árbol {tipo} creado correctamente")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _insertar_valor(self):
        """Inserta un valor único"""
        valor = self.entry_valor.get().strip()

        if not valor:
            messagebox.showwarning("Advertencia", "Ingrese un valor")
            return

        try:
            self.controller.insertar_valor(valor)
            self.entry_valor.delete(0, 'end')
            self._actualizar_visualizacion()
            self._actualizar_info()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _insertar_multiples(self):
        """Inserta múltiples valores"""
        valores = self.entry_multiples.get().strip()

        if not valores:
            messagebox.showwarning("Advertencia", "Ingrese valores")
            return

        try:
            insertados, errores = self.controller.insertar_multiples(valores)
            self.entry_multiples.delete(0, 'end')
            self._actualizar_visualizacion()
            self._actualizar_info()

            mensaje = f"Insertados: {len(insertados)} valores"
            if errores:
                mensaje += f"\nErrores: {len(errores)}"
                for error in errores[:3]:  # Mostrar máximo 3 errores
                    mensaje += f"\n- {error}"

            messagebox.showinfo("Resultado", mensaje)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _buscar_valor(self):
        """Busca un valor en el árbol"""
        valor = self.entry_buscar.get().strip()

        if not valor:
            messagebox.showwarning("Advertencia", "Ingrese un valor a buscar")
            return

        try:
            encontrado = self.controller.buscar_valor(valor)

            if encontrado:
                messagebox.showinfo("Resultado", f"✓ El valor {valor} SÍ está en el árbol")
            else:
                messagebox.showinfo("Resultado", f"✗ El valor {valor} NO está en el árbol")

            self.entry_buscar.delete(0, 'end')
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _limpiar_arbol(self):
        """Limpia el árbol actual"""
        if messagebox.askyesno("Confirmar", "¿Desea limpiar el árbol?"):
            self.controller.limpiar_arbol()
            self.canvas_arbol.limpiar()
            self._actualizar_info()

    def _actualizar_visualizacion(self):
        """Actualiza la visualización del árbol"""
        arbol = self.controller.obtener_arbol()
        tipo = self.controller.obtener_tipo_arbol()
        self.canvas_arbol.dibujar_arbol(arbol, tipo)

    def _actualizar_info(self):
        """Actualiza la información del árbol"""
        info = self.controller.obtener_info_arbol()
        recorrido = self.controller.obtener_recorrido_inorden()
        niveles_lista, cantidad_nodos = self.controller.obtener_niveles_y_nodos_espejo()

        texto = f"Tipo: {info['tipo'] or 'Ninguno'}\n"
        texto += f"Elementos: {info['elementos']}\n"
        texto += f"Raíz: {info['raiz'] or 'Vacío'}\n"
        texto += f"\nRecorrido Inorden:\n"
        texto += str(recorrido) if recorrido else "[]"
        texto += f"\nCantidad de niveles espejo: {len(niveles_lista)}\n"
        texto += f"Niveles espejo: {niveles_lista if niveles_lista else 'Ninguno'}\n"
        texto += f"Cantidad de nodos simétricos: {cantidad_nodos}"

        self.texto_info.delete('1.0', 'end')
        self.texto_info.insert('1.0', texto)

    # def _verificar_y_actualizar(self):
    #     """Verifica si el árbol es espejo y actualiza la información"""
    #     self.controller.verificar_espejo()
    #     self._actualizar_info()

    def ejecutar(self):
        """Inicia la aplicación"""
        self.root.mainloop()