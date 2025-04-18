import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from ui_components import StructureFrame


class DoublyLinkedListFrame(StructureFrame):
    """Frame for Doubly Linked List operations and visualization."""

    def __init__(self, parent):
        super().__init__(parent, "Doubly Linked List")
        from structures import DoublyLinkedList
        self.structure = DoublyLinkedList()
        self.update_info()

    def _create_info_widgets(self):
        self.size_var = tk.StringVar(value="Size: 0")
        self.head_var = tk.StringVar(value="Head: None")
        self.tail_var = tk.StringVar(value="Tail: None")

        ttk.Label(self.info_frame, textvariable=self.size_var).pack(anchor=tk.W, padx=5, pady=2)
        ttk.Label(self.info_frame, textvariable=self.head_var).pack(anchor=tk.W, padx=5, pady=2)
        ttk.Label(self.info_frame, textvariable=self.tail_var).pack(anchor=tk.W, padx=5, pady=2)

    def _create_action_widgets(self, parent_frame):
        # Input frame
        input_frame = ttk.Frame(parent_frame)
        input_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(input_frame, text="Value:").pack(side=tk.LEFT, padx=5)
        self.value_entry = ttk.Entry(input_frame, width=15)
        self.value_entry.pack(side=tk.LEFT, padx=5)

        # Action buttons for insertion
        insert_frame = ttk.LabelFrame(parent_frame, text="Insert Operations")
        insert_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Button(insert_frame, text="Insert at Beginning",
                   command=self.insert_at_beginning).pack(side=tk.LEFT, padx=5)
        ttk.Button(insert_frame, text="Insert at End",
                   command=self.insert_at_end).pack(side=tk.LEFT, padx=5)
        ttk.Button(insert_frame, text="Insert at Position",
                   command=self.insert_at_position).pack(side=tk.LEFT, padx=5)

        # Action buttons for deletion
        delete_frame = ttk.LabelFrame(parent_frame, text="Delete Operations")
        delete_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Button(delete_frame, text="Delete from Beginning",
                   command=self.delete_from_beginning).pack(side=tk.LEFT, padx=5)
        ttk.Button(delete_frame, text="Delete from End",
                   command=self.delete_from_end).pack(side=tk.LEFT, padx=5)
        ttk.Button(delete_frame, text="Delete at Position",
                   command=self.delete_at_position).pack(side=tk.LEFT, padx=5)

        # Search button
        search_frame = ttk.Frame(parent_frame)
        search_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Button(search_frame, text="Search",
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
            self.update_visualization()
            self.value_entry.delete(0, tk.END)

    def insert_at_end(self):
        value = self.value_entry.get()
        if not value:
            messagebox.showerror("Input Error", "Please enter a value")
            return

        converted_value = self.convert_input_value(value)
        if converted_value is not None:
            self.structure.insert_at_end(converted_value)
            self.update_info()
            self.update_visualization()
            self.value_entry.delete(0, tk.END)

    def insert_at_position(self):
        value = self.value_entry.get()
        if not value:
            messagebox.showerror("Input Error", "Please enter a value")
            return

        position = simpledialog.askinteger("Position",
                                           f"Enter position (0-{self.structure.size}):",
                                           minvalue=0, maxvalue=self.structure.size)
        if position is None:  # User cancelled
            return

        converted_value = self.convert_input_value(value)
        if converted_value is not None:
            if self.structure.insert_at_position(position, converted_value):
                self.update_info()
                self.update_visualization()
                self.value_entry.delete(0, tk.END)
            else:
                messagebox.showerror("Insert Error", "Failed to insert at position")

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

    def delete_at_position(self):
        if not self.structure.head:
            messagebox.showinfo("List Empty", "The list is empty")
            return

        position = simpledialog.askinteger("Position",
                                           f"Enter position (0-{self.structure.size - 1}):",
                                           minvalue=0, maxvalue=self.structure.size - 1)
        if position is None:  # User cancelled
            return

        value = self.structure.delete_at_position(position)
        if value is not None:
            messagebox.showinfo("Delete Result", f"Deleted value: {value}")
            self.update_info()
            self.update_visualization()
        else:
            messagebox.showerror("Delete Error", "Failed to delete at position")

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
        tail_value = self.structure.tail.data if self.structure.tail else "None"
        self.tail_var.set(f"Tail: {tail_value}")

    def update_visualization(self):
        # Clear the canvas
        self.canvas.delete("all")

        nodes = self.structure.get_nodes()
        if not nodes:
            return

        # Draw the doubly linked list from left to right
        box_width = 80
        box_height = 40
        x_left = 30
        y_center = self.canvas.winfo_height() // 2

        for i, node in enumerate(nodes):
            # Calculate position
            x = x_left + i * (box_width + 80)
            y = y_center - box_height // 2

            # Draw node box
            self.canvas.create_rectangle(x, y, x + box_width, y + box_height,
                                         fill="lightblue", outline="black")

            # Draw value
            self.canvas.create_text(x + box_width // 2, y + box_height // 2,
                                    text=str(node.data))

            # Draw memory address
            self.canvas.create_text(x + box_width // 2, y - 15,
                                    text=f"Mem: {hex(node.memory_address)}",
                                    font=("Arial", 8))

            # Draw next pointer (except for the last node)
            if i < len(nodes) - 1:
                self.canvas.create_line(x + box_width, y + box_height // 3,
                                        x + box_width + 80, y + box_height // 3,
                                        arrow=tk.LAST, fill="black")

                # Add next pointer text
                next_text_x = x + box_width + 40
                self.canvas.create_text(next_text_x, y + box_height // 3 - 10,
                                        text="next", font=("Arial", 8))

            # Draw prev pointer (except for the first node)
            if i > 0:
                self.canvas.create_line(x, y + 2 * box_height // 3,
                                        x - 80, y + 2 * box_height // 3,
                                        arrow=tk.LAST, fill="blue")

                # Add prev pointer text
                prev_text_x = x - 40
                self.canvas.create_text(prev_text_x, y + 2 * box_height // 3 - 10,
                                        text="prev", font=("Arial", 8))

        # Mark the "head" pointer
        if nodes:
            self.canvas.create_text(x_left - 15, y_center - 10, text="head",
                                    anchor=tk.E, font=("Arial", 10, "bold"))
            self.canvas.create_line(x_left - 10, y_center - 10,
                                    x_left, y_center - 10, arrow=tk.LAST)

            # Mark the "tail" pointer
            last_x = x_left + (len(nodes) - 1) * (box_width + 80)
            self.canvas.create_text(last_x + box_width + 15, y_center - 10,
                                    text="tail", anchor=tk.W, font=("Arial", 10, "bold"))
            self.canvas.create_line(last_x + box_width + 10, y_center - 10,
                                    last_x + box_width, y_center - 10, arrow=tk.LAST)