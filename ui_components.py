import tkinter as tk
from tkinter import ttk, messagebox


class StructureFrame(ttk.Frame):
    """Base frame for displaying and interacting with a data structure."""

    def __init__(self, parent, structure_type):
        super().__init__(parent)
        self.parent = parent
        self.structure_type = structure_type
        self.structure = None
        self.data_type = tk.StringVar(value="int")  # Default data type

        self._create_widgets()

    def _create_widgets(self):
        # Top control frame
        control_frame = ttk.Frame(self)
        control_frame.pack(fill=tk.X, padx=10, pady=5)

        # Data type selection
        ttk.Label(control_frame, text="Data Type:").pack(side=tk.LEFT, padx=5)
        data_types = ["int", "float", "str", "bool"]
        data_type_combo = ttk.Combobox(control_frame, textvariable=self.data_type,
                                       values=data_types, state="readonly", width=10)
        data_type_combo.pack(side=tk.LEFT, padx=5)

        # Structure info frame
        self.info_frame = ttk.LabelFrame(self, text=f"{self.structure_type} Information")
        self.info_frame.pack(fill=tk.X, padx=10, pady=5)

        # Create the specific info widgets based on structure type
        self._create_info_widgets()

        # Actions frame
        actions_frame = ttk.LabelFrame(self, text="Actions")
        actions_frame.pack(fill=tk.X, padx=10, pady=5)

        # Create action buttons based on structure type
        self._create_action_widgets(actions_frame)

        # Visualization frame
        self.viz_frame = ttk.LabelFrame(self, text="Visualization")
        self.viz_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Canvas for drawing the structure
        self.canvas = tk.Canvas(self.viz_frame, bg="white", bd=2, relief=tk.SUNKEN)
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def _create_info_widgets(self):
        """Create widgets to display structure information.
        Override in subclasses."""
        ttk.Label(self.info_frame, text="Size: 0").pack(anchor=tk.W, padx=5, pady=2)

    def _create_action_widgets(self, parent_frame):
        """Create action buttons specific to the structure.
        Override in subclasses."""
        pass

    def convert_input_value(self, value_str):
        """Convert input string to the selected data type."""
        try:
            if self.data_type.get() == "int":
                return int(value_str)
            elif self.data_type.get() == "float":
                return float(value_str)
            elif self.data_type.get() == "bool":
                return value_str.lower() in ['true', 'yes', '1', 't', 'y']
            else:  # Default to string
                return value_str
        except (ValueError, TypeError):
            messagebox.showerror("Type Error",
                                 f"Cannot convert '{value_str}' to {self.data_type.get()}")
            return None

    def update_visualization(self):
        """Update the visualization of the structure. Override in subclasses."""
        pass


class StackFrame(StructureFrame):
    """Frame for Stack operations and visualization."""

    def __init__(self, parent):
        super().__init__(parent, "Stack")
        from structures import Stack
        self.structure = Stack()
        self.update_info()

    def _create_info_widgets(self):
        self.size_var = tk.StringVar(value="Size: 0")
        self.top_var = tk.StringVar(value="Top: None")

        ttk.Label(self.info_frame, textvariable=self.size_var).pack(anchor=tk.W, padx=5, pady=2)
        ttk.Label(self.info_frame, textvariable=self.top_var).pack(anchor=tk.W, padx=5, pady=2)

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

        ttk.Button(button_frame, text="Push", command=self.push).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Pop", command=self.pop).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Peek", command=self.peek).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Search", command=self.search).pack(side=tk.LEFT, padx=5)

    def push(self):
        value = self.value_entry.get()
        if not value:
            messagebox.showerror("Input Error", "Please enter a value")
            return

        converted_value = self.convert_input_value(value)
        if converted_value is not None:
            self.structure.push(converted_value)
            self.update_info()
            self.update_visualization()
            self.value_entry.delete(0, tk.END)

    def pop(self):
        if self.structure.is_empty():
            messagebox.showinfo("Stack Empty", "The stack is empty")
            return

        value = self.structure.pop()
        messagebox.showinfo("Pop Result", f"Popped value: {value}")
        self.update_info()
        self.update_visualization()

    def peek(self):
        if self.structure.is_empty():
            messagebox.showinfo("Stack Empty", "The stack is empty")
            return

        value = self.structure.peek()
        messagebox.showinfo("Peek Result", f"Top value: {value}")

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
        top_value = self.structure.peek() if not self.structure.is_empty() else "None"
        self.top_var.set(f"Top: {top_value}")

    def update_visualization(self):
        # Clear the canvas
        self.canvas.delete("all")

        nodes = self.structure.get_nodes()
        if not nodes:
            return

        # Draw the stack from bottom to top
        box_width = 100
        box_height = 40
        x_center = self.canvas.winfo_width() // 2
        y_bottom = self.canvas.winfo_height() - 30

        for i, node in enumerate(reversed(nodes)):
            # Calculate position
            x = x_center - box_width // 2
            y = y_bottom - i * (box_height + 10)

            # Draw node box
            self.canvas.create_rectangle(x, y, x + box_width, y - box_height,
                                         fill="lightblue", outline="black")

            # Draw value
            self.canvas.create_text(x + box_width // 2, y - box_height // 2,
                                    text=str(node.data))

            # Draw memory address
            self.canvas.create_text(x + box_width // 2, y - box_height - 5,
                                    text=f"Mem: {hex(node.memory_address)}",
                                    font=("Arial", 8))

            # Draw pointer (except for the top node)
            if i < len(nodes) - 1:
                self.canvas.create_line(x_center, y - box_height - 5,
                                        x_center, y - box_height - 10,
                                        arrow=tk.LAST, fill="black")


class QueueFrame(StructureFrame):
    """Frame for Queue operations and visualization."""

    def __init__(self, parent):
        super().__init__(parent, "Queue")
        from structures import Queue
        self.structure = Queue()
        self.update_info()

    def _create_info_widgets(self):
        self.size_var = tk.StringVar(value="Size: 0")
        self.front_var = tk.StringVar(value="Front: None")
        self.rear_var = tk.StringVar(value="Rear: None")

        ttk.Label(self.info_frame, textvariable=self.size_var).pack(anchor=tk.W, padx=5, pady=2)
        ttk.Label(self.info_frame, textvariable=self.front_var).pack(anchor=tk.W, padx=5, pady=2)
        ttk.Label(self.info_frame, textvariable=self.rear_var).pack(anchor=tk.W, padx=5, pady=2)

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

        ttk.Button(button_frame, text="Enqueue", command=self.enqueue).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Dequeue", command=self.dequeue).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Peek", command=self.peek).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Search", command=self.search).pack(side=tk.LEFT, padx=5)

    def enqueue(self):
        value = self.value_entry.get()
        if not value:
            messagebox.showerror("Input Error", "Please enter a value")
            return

        converted_value = self.convert_input_value(value)
        if converted_value is not None:
            self.structure.enqueue(converted_value)
            self.update_info()
            self.update_visualization()
            self.value_entry.delete(0, tk.END)

    def dequeue(self):
        if self.structure.is_empty():
            messagebox.showinfo("Queue Empty", "The queue is empty")
            return

        value = self.structure.dequeue()
        messagebox.showinfo("Dequeue Result", f"Dequeued value: {value}")
        self.update_info()
        self.update_visualization()

    def peek(self):
        if self.structure.is_empty():
            messagebox.showinfo("Queue Empty", "The queue is empty")
            return

        value = self.structure.peek()
        messagebox.showinfo("Peek Result", f"Front value: {value}")

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
        front_value = self.structure.peek() if not self.structure.is_empty() else "None"
        self.front_var.set(f"Front: {front_value}")

        # For the rear value, we need to find the last node if it exists
        if self.structure.rear:
            self.rear_var.set(f"Rear: {self.structure.rear.data}")
        else:
            self.rear_var.set("Rear: None")

    def update_visualization(self):
        # Clear the canvas
        self.canvas.delete("all")

        nodes = self.structure.get_nodes()
        if not nodes:
            return

        # Draw the queue from left to right
        box_width = 80
        box_height = 40
        x_left = 30
        y_center = self.canvas.winfo_height() // 2

        for i, node in enumerate(nodes):
            # Calculate position
            x = x_left + i * (box_width + 20)
            y = y_center - box_height // 2

            # Draw node box
            self.canvas.create_rectangle(x, y, x + box_width, y + box_height,
                                         fill="lightgreen", outline="black")

            # Draw value
            self.canvas.create_text(x + box_width // 2, y + box_height // 2,
                                    text=str(node.data))

            # Draw memory address
            self.canvas.create_text(x + box_width // 2, y - 15,
                                    text=f"Mem: {hex(node.memory_address)}",
                                    font=("Arial", 8))

            # Draw pointer (except for the last node)
            if i < len(nodes) - 1:
                self.canvas.create_line(x + box_width, y + box_height // 2,
                                        x + box_width + 20, y + box_height // 2,
                                        arrow=tk.LAST, fill="black")

        # Label front and rear
        if nodes:
            self.canvas.create_text(x_left + box_width // 2, y_center + box_height // 2 + 25,
                                    text="Front", font=("Arial", 10, "bold"))

            last_x = x_left + (len(nodes) - 1) * (box_width + 20)
            self.canvas.create_text(last_x + box_width // 2, y_center + box_height // 2 + 25,
                                    text="Rear", font=("Arial", 10, "bold"))

# More UI components for other data structures will follow the same pattern
# They will be implemented in subsequent code artifacts