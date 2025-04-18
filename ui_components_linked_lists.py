import tkinter as tk
from tkinter import ttk, messagebox
from ui_components import StructureFrame


class SinglyLinkedListFrame(StructureFrame):
    """Frame for Singly Linked List operations and visualization."""

    def __init__(self, parent):
        super().__init__(parent, "Singly Linked List")
        from structures import SinglyLinkedList
        self.structure = SinglyLinkedList()
        self.update_info()

        # Configurar el canvas con un fondo blanco
        self.canvas.configure(bg="white")

        # Forzar un redibujado inicial después de configuración
        self.canvas.update_idletasks()
        self.after(100, self.update_visualization)

    def _create_info_widgets(self):
        self.size_var = tk.StringVar(value="Size: 0")
        self.head_var = tk.StringVar(value="Head: None")

        ttk.Label(self.info_frame, textvariable=self.size_var).pack(anchor=tk.W, padx=5, pady=2)
        ttk.Label(self.info_frame, textvariable=self.head_var).pack(anchor=tk.W, padx=5, pady=2)

    def _create_action_widgets(self, parent_frame):
        # Input frame
        input_frame = ttk.Frame(parent_frame)
        input_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(input_frame, text="Value:").pack(side=tk.LEFT, padx=5)
        self.value_entry = ttk.Entry(input_frame, width=15)
        self.value_entry.pack(side=tk.LEFT, padx=5)

        # Action buttons
        button_frame = ttk.Frame(parent_frame)
        button_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Button(button_frame, text="Insert at Beginning",
                   command=self.insert_at_beginning).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Insert at End",
                   command=self.insert_at_end).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Delete from Beginning",
                   command=self.delete_from_beginning).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Delete from End",
                   command=self.delete_from_end).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Search",
                   command=self.search).pack(side=tk.LEFT, padx=5)

    def insert_at_beginning(self):
        value = self.value_entry.get()
        if not value:
            messagebox.showerror("Input Error", "Please enter a value")
            return

        converted_value = self.convert_input_value(value)
        if converted_value is not None:
            self.structure.insert_at_beginning(converted_value)
            self.update_info()

            # Esperar a que la interfaz se actualice
            self.canvas.update_idletasks()
            self.update_visualization()

            self.value_entry.delete(0, tk.END)
            messagebox.showinfo("Insert", f"Value {converted_value} inserted at beginning")

    def insert_at_end(self):
        value = self.value_entry.get()
        if not value:
            messagebox.showerror("Input Error", "Please enter a value")
            return

        converted_value = self.convert_input_value(value)
        if converted_value is not None:
            self.structure.insert_at_end(converted_value)
            self.update_info()

            # Esperar a que la interfaz se actualice
            self.canvas.update_idletasks()
            self.update_visualization()

            self.value_entry.delete(0, tk.END)
            messagebox.showinfo("Insert", f"Value {converted_value} inserted at end")

    def delete_from_beginning(self):
        if not self.structure.head:
            messagebox.showinfo("List Empty", "The list is empty")
            return

        value = self.structure.delete_from_beginning()
        messagebox.showinfo("Delete Result", f"Deleted value: {value}")
        self.update_info()
        self.update_visualization()

    def delete_from_end(self):
        if not self.structure.head:
            messagebox.showinfo("List Empty", "The list is empty")
            return

        value = self.structure.delete_from_end()
        messagebox.showinfo("Delete Result", f"Deleted value: {value}")
        self.update_info()
        self.update_visualization()

    def search(self):
        value = self.value_entry.get()
        if not value:
            messagebox.showerror("Input Error", "Please enter a value to search")
            return

        converted_value = self.convert_input_value(value)
        if converted_value is not None:
            position = self.structure.search(converted_value)
            if position >= 0:
                messagebox.showinfo("Search Result", f"Value found at position: {position}")
            else:
                messagebox.showinfo("Search Result", "Value not found")

    def update_info(self):
        self.size_var.set(f"Size: {self.structure.size}")
        head_value = self.structure.head.data if self.structure.head else "None"
        self.head_var.set(f"Head: {head_value}")

    def update_visualization(self):
        # Limpia el canvas
        self.canvas.delete("all")

        # Obtén los nodos
        nodes = self.structure.get_nodes()
        if not nodes:
            return

        # Asegúrate de que el canvas tiene un tamaño antes de calcular posiciones
        canvas_width = self.canvas.winfo_width() or 400  # Valor por defecto si el ancho es 0
        canvas_height = self.canvas.winfo_height() or 200  # Valor por defecto si la altura es 0

        # Dibuja la lista enlazada de izquierda a derecha
        box_width = 80
        box_height = 40
        x_left = 80  # Aumentado desde 30 para mover a la derecha
        y_center = canvas_height // 2

        # Imprime información de depuración
        print(f"Canvas size: {canvas_width}x{canvas_height}")
        print(f"Number of nodes: {len(nodes)}")
        print(f"Node data: {[str(node.data) for node in nodes]}")

        for i, node in enumerate(nodes):
            # Calcula la posición
            x = x_left + i * (box_width + 50)
            y = y_center - box_height // 2

            # Dibuja la caja del nodo
            node_id = self.canvas.create_rectangle(x, y, x + box_width, y + box_height,
                                                   fill="lightyellow", outline="black", width=2)

            # Dibuja el valor - asegúrate de que sea una cadena y use color negro
            try:
                node_text = str(node.data)
                text_id = self.canvas.create_text(x + box_width // 2, y + box_height // 2,
                                                  text=node_text, fill="black", font=("Arial", 12, "bold"))
                print(f"Created text '{node_text}' with ID {text_id} at ({x + box_width // 2}, {y + box_height // 2})")
            except Exception as e:
                print(f"Error creating text: {e}")
                # Intenta un texto genérico si falla la conversión
                self.canvas.create_text(x + box_width // 2, y + box_height // 2,
                                        text="[ERROR]", fill="red")

            # Dibuja el puntero (excepto para el último nodo)
            if i < len(nodes) - 1:
                self.canvas.create_line(x + box_width, y + box_height // 2,
                                        x + box_width + 50, y + box_height // 2,
                                        arrow=tk.LAST, fill="black", width=2)

                # Añade texto para el puntero "next"
                next_text_x = x + box_width + 25
                self.canvas.create_text(next_text_x, y + box_height // 2 - 15,
                                        text="next", fill="darkgreen", font=("Arial", 8))

        # Marca el puntero "head"
        if nodes:
            self.canvas.create_text(x_left - 25, y_center, text="head",
                                    anchor=tk.E, fill="red", font=("Arial", 10, "bold"))
            self.canvas.create_line(x_left - 20, y_center,
                                    x_left, y_center, arrow=tk.LAST, fill="red", width=2)

        # Forzar actualización del canvas
        self.canvas.update_idletasks()


class CircularLinkedListFrame(StructureFrame):
    """Frame for Circular Linked List operations and visualization."""

    def __init__(self, parent):
        super().__init__(parent, "Circular Linked List")
        from structures import CircularLinkedList
        self.structure = CircularLinkedList()
        self.update_info()

        # Configurar el canvas con un fondo blanco
        self.canvas.configure(bg="white")

        # Forzar un redibujado inicial después de configuración
        self.canvas.update_idletasks()
        self.after(100, self.update_visualization)

    def _create_info_widgets(self):
        self.size_var = tk.StringVar(value="Size: 0")
        self.head_var = tk.StringVar(value="Head: None")

        ttk.Label(self.info_frame, textvariable=self.size_var).pack(anchor=tk.W, padx=5, pady=2)
        ttk.Label(self.info_frame, textvariable=self.head_var).pack(anchor=tk.W, padx=5, pady=2)

    def _create_action_widgets(self, parent_frame):
        # Input frame
        input_frame = ttk.Frame(parent_frame)
        input_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(input_frame, text="Value:").pack(side=tk.LEFT, padx=5)
        self.value_entry = ttk.Entry(input_frame, width=15)
        self.value_entry.pack(side=tk.LEFT, padx=5)

        # Action buttons
        button_frame1 = ttk.Frame(parent_frame)
        button_frame1.pack(fill=tk.X, padx=5, pady=5)

        ttk.Button(button_frame1, text="Insert at Beginning",
                   command=self.insert_at_beginning).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame1, text="Insert at End",
                   command=self.insert_at_end).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame1, text="Delete from Beginning",
                   command=self.delete_from_beginning).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame1, text="Delete from End",
                   command=self.delete_from_end).pack(side=tk.LEFT, padx=5)

        button_frame2 = ttk.Frame(parent_frame)
        button_frame2.pack(fill=tk.X, padx=5, pady=5)

        ttk.Button(button_frame2, text="Search",
                   command=self.search).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame2, text="Rotate Left",
                   command=self.rotate_left).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame2, text="Rotate Right",
                   command=self.rotate_right).pack(side=tk.LEFT, padx=5)

    def insert_at_beginning(self):
        value = self.value_entry.get()
        if not value:
            messagebox.showerror("Input Error", "Please enter a value")
            return

        converted_value = self.convert_input_value(value)
        if converted_value is not None:
            self.structure.insert_at_beginning(converted_value)
            self.update_info()

            # Esperar a que la interfaz se actualice
            self.canvas.update_idletasks()
            self.update_visualization()

            self.value_entry.delete(0, tk.END)
            messagebox.showinfo("Insert", f"Value {converted_value} inserted at beginning")

    def insert_at_end(self):
        value = self.value_entry.get()
        if not value:
            messagebox.showerror("Input Error", "Please enter a value")
            return

        converted_value = self.convert_input_value(value)
        if converted_value is not None:
            self.structure.insert_at_end(converted_value)
            self.update_info()

            # Esperar a que la interfaz se actualice
            self.canvas.update_idletasks()
            self.update_visualization()

            self.value_entry.delete(0, tk.END)
            messagebox.showinfo("Insert", f"Value {converted_value} inserted at end")

    def delete_from_beginning(self):
        if not self.structure.head:
            messagebox.showinfo("List Empty", "The list is empty")
            return

        value = self.structure.delete_from_beginning()
        messagebox.showinfo("Delete Result", f"Deleted value: {value}")
        self.update_info()
        self.update_visualization()

    def delete_from_end(self):
        if not self.structure.head:
            messagebox.showinfo("List Empty", "The list is empty")
            return

        value = self.structure.delete_from_end()
        messagebox.showinfo("Delete Result", f"Deleted value: {value}")
        self.update_info()
        self.update_visualization()

    def search(self):
        value = self.value_entry.get()
        if not value:
            messagebox.showerror("Input Error", "Please enter a value to search")
            return

        converted_value = self.convert_input_value(value)
        if converted_value is not None:
            position = self.structure.search(converted_value)
            if position >= 0:
                messagebox.showinfo("Search Result", f"Value found at position: {position}")
            else:
                messagebox.showinfo("Search Result", "Value not found")

    def rotate_left(self):
        if not self.structure.head:
            messagebox.showinfo("List Empty", "The list is empty")
            return

        self.structure.rotate_left()
        self.update_info()
        self.update_visualization()
        messagebox.showinfo("Rotate Left", "The list has been rotated left")

    def rotate_right(self):
        if not self.structure.head:
            messagebox.showinfo("List Empty", "The list is empty")
            return

        self.structure.rotate_right()
        self.update_info()
        self.update_visualization()
        messagebox.showinfo("Rotate Right", "The list has been rotated right")

    def update_info(self):
        self.size_var.set(f"Size: {self.structure.size}")
        head_value = self.structure.head.data if self.structure.head else "None"
        self.head_var.set(f"Head: {head_value}")

    def update_visualization(self):
        # Clear the canvas
        self.canvas.delete("all")

        nodes = self.structure.get_nodes()
        if not nodes:
            return

        # Asegúrate de que el canvas tiene un tamaño antes de calcular posiciones
        canvas_width = self.canvas.winfo_width() or 400  # Valor por defecto si el ancho es 0
        canvas_height = self.canvas.winfo_height() or 200  # Valor por defecto si la altura es 0

        # Draw circular linked list in a circle
        center_x = canvas_width // 2
        center_y = canvas_height // 2
        radius = min(center_x, center_y) - 70  # Reducido para dejar más espacio

        # Print debug info
        print(f"Canvas size: {canvas_width}x{canvas_height}")
        print(f"Center: ({center_x}, {center_y}), Radius: {radius}")
        print(f"Number of nodes: {len(nodes)}")
        print(f"Node data: {[str(node.data) for node in nodes]}")

        # Calculate positions for nodes
        node_positions = []
        for i in range(len(nodes)):
            angle = 2 * 3.14159 * i / len(nodes)
            x = center_x + radius * (math_cos := [1, 0, -1, 0])[int(angle // (3.14159 / 2))]
            y = center_y + radius * (math_sin := [0, 1, 0, -1])[int(angle // (3.14159 / 2))]
            node_positions.append((x, y))

        # Draw nodes
        box_width = 60
        box_height = 40
        for i, node in enumerate(nodes):
            x, y = node_positions[i]

            # Draw node box
            x1 = x - box_width // 2
            y1 = y - box_height // 2
            x2 = x + box_width // 2
            y2 = y + box_height // 2

            self.canvas.create_rectangle(x1, y1, x2, y2,
                                         fill="lightpink", outline="black", width=2)

            # Draw value - asegúrate de que sea una cadena y use color negro
            try:
                node_text = str(node.data)
                text_id = self.canvas.create_text(x, y, text=node_text,
                                                  fill="black", font=("Arial", 12, "bold"))
                print(f"Created text '{node_text}' with ID {text_id} at ({x}, {y})")
            except Exception as e:
                print(f"Error creating text: {e}")
                # Intenta un texto genérico si falla la conversión
                self.canvas.create_text(x, y, text="[ERROR]", fill="red")

        # Draw connections between nodes
        for i in range(len(nodes)):
            start_x, start_y = node_positions[i]
            end_x, end_y = node_positions[(i + 1) % len(nodes)]

            # Calculate the direction from start to end
            dx = end_x - start_x
            dy = end_y - start_y
            dist = (dx ** 2 + dy ** 2) ** 0.5

            # Calculate start and end points for the arrow
            if dist > 0:
                nx = dx / dist
                ny = dy / dist
            else:
                nx, ny = 0, 0

            # Adjust start and end points to be on the box boundaries
            start_x = start_x + nx * (box_width // 2)
            start_y = start_y + ny * (box_height // 2)
            end_x = end_x - nx * (box_width // 2)
            end_y = end_y - ny * (box_height // 2)

            # Draw the arrow
            self.canvas.create_line(start_x, start_y, end_x, end_y,
                                    arrow=tk.LAST, fill="black", width=2)

            # Add "next" label midway
            mid_x = (start_x + end_x) / 2
            mid_y = (start_y + end_y) / 2
            offset_x = -ny * 10  # Perpendicular offset for the text
            offset_y = nx * 10
            self.canvas.create_text(mid_x + offset_x, mid_y + offset_y,
                                    text="next", fill="darkgreen", font=("Arial", 8))

        # Mark the head pointer
        if nodes:
            head_x, head_y = node_positions[0]
            # Move the head text to a better position
            head_text_x = center_x
            head_text_y = center_y - radius - 20  # Moved up to avoid overlap

            self.canvas.create_text(head_text_x, head_text_y, text="head",
                                    font=("Arial", 10, "bold"), fill="red")
            self.canvas.create_line(head_text_x, head_text_y + 10,
                                    head_x, head_y - box_height // 2,
                                    arrow=tk.LAST, dash=(4, 2), fill="red", width=2)

        # Forzar actualización del canvas
        self.canvas.update_idletasks()