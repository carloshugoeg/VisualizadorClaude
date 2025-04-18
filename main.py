import tkinter as tk
from tkinter import ttk, messagebox
from ui_components import StackFrame, QueueFrame
from ui_components_linked_lists import SinglyLinkedListFrame, CircularLinkedListFrame
from ui_components_double_linked_list import DoublyLinkedListFrame
from ui_components_trees import BinaryTreeFrame, BinarySearchTreeFrame
from file_manager import FileManager


class DataStructureVisualizer(tk.Tk):
    """Main application for visualizing data structures."""

    def __init__(self):
        super().__init__()

        self.title("Data Structure Visualizer")
        self.geometry("1000x700")
        self.minsize(800, 600)

        # Create menu
        self.create_menu()

        # Create main content
        self.content_frame = ttk.Frame(self)
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create structure selection
        self.create_structure_selector()

        # Current active frame
        self.current_frame = None

        # Welcome message
        self.show_welcome()

    def create_menu(self):
        """Create the application menu."""
        menu_bar = tk.Menu(self)

        # File menu
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="New", command=self.new_structure)
        file_menu.add_command(label="Open", command=self.load_structure)
        file_menu.add_command(label="Save", command=self.save_structure)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)

        menu_bar.add_cascade(label="File", menu=file_menu)

        # Help menu
        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)

        menu_bar.add_cascade(label="Help", menu=help_menu)

        self.config(menu=menu_bar)

    def create_structure_selector(self):
        """Create dropdown for selecting data structure type."""
        selector_frame = ttk.Frame(self.content_frame)
        selector_frame.pack(fill=tk.X, pady=10)

        ttk.Label(selector_frame, text="Select Data Structure:").pack(side=tk.LEFT, padx=5)

        self.structure_var = tk.StringVar()
        structures = [
            "Stack",
            "Queue",
            "Singly Linked List",
            "Circular Linked List",
            "Doubly Linked List",
            "Binary Tree",
            "Binary Search Tree"
        ]

        structure_combo = ttk.Combobox(selector_frame, textvariable=self.structure_var,
                                       values=structures, state="readonly", width=20)
        structure_combo.pack(side=tk.LEFT, padx=5)
        structure_combo.bind("<<ComboboxSelected>>", self.on_structure_selected)

    def on_structure_selected(self, event):
        """Handle selection of a data structure type."""
        structure_type = self.structure_var.get()

        # Clear current frame if exists
        if self.current_frame:
            # Unbind any existing events before destroying
            self.unbind("<Configure>")
            self.current_frame.destroy()

        # Create new frame based on selection
        if structure_type == "Stack":
            self.current_frame = StackFrame(self.content_frame)
        elif structure_type == "Queue":
            self.current_frame = QueueFrame(self.content_frame)
        elif structure_type == "Singly Linked List":
            self.current_frame = SinglyLinkedListFrame(self.content_frame)
        elif structure_type == "Circular Linked List":
            self.current_frame = CircularLinkedListFrame(self.content_frame)
        elif structure_type == "Doubly Linked List":
            self.current_frame = DoublyLinkedListFrame(self.content_frame)
        elif structure_type == "Binary Tree":
            self.current_frame = BinaryTreeFrame(self.content_frame)
        elif structure_type == "Binary Search Tree":
            self.current_frame = BinarySearchTreeFrame(self.content_frame)

        # Display the frame
        if self.current_frame:
            self.current_frame.pack(fill=tk.BOTH, expand=True)

            # Create a safe resize handler
            def safe_resize_handler(event):
                if self.current_frame and self.current_frame.winfo_exists():
                    try:
                        self.current_frame.update_visualization()
                    except (tk.TclError, AttributeError):
                        # Silently ignore errors if the widget no longer exists
                        pass

            # Bind resize event to update visualization
            self.bind("<Configure>", safe_resize_handler)

    def new_structure(self):
        """Create a new data structure."""
        if self.current_frame:
            if messagebox.askyesno("New Structure",
                                   "This will clear the current structure. Continue?"):
                # Unbind events before destroying
                self.unbind("<Configure>")
                self.current_frame.destroy()
                self.current_frame = None
                self.structure_var.set("")

    def save_structure(self):
        """Save current structure to a file."""
        if not self.current_frame:
            messagebox.showinfo("Save", "No structure to save.")
            return

        success = FileManager.save_structure(
            self.current_frame.structure,
            self.structure_var.get()
        )

        if success:
            messagebox.showinfo("Save", "Structure saved successfully.")

    def load_structure(self):
        """Load a structure from a file."""
        structure_type, structure = FileManager.load_structure()

        if not structure_type or not structure:
            return

        # Clear current frame if exists
        if self.current_frame:
            # Unbind any existing events before destroying
            self.unbind("<Configure>")
            self.current_frame.destroy()

        # Set the combobox to the loaded structure type
        self.structure_var.set(structure_type)

        # Create new frame based on the loaded structure type
        if structure_type == "Stack":
            self.current_frame = StackFrame(self.content_frame)
        elif structure_type == "Queue":
            self.current_frame = QueueFrame(self.content_frame)
        elif structure_type == "Singly Linked List":
            self.current_frame = SinglyLinkedListFrame(self.content_frame)
        elif structure_type == "Circular Linked List":
            self.current_frame = CircularLinkedListFrame(self.content_frame)
        elif structure_type == "Doubly Linked List":
            self.current_frame = DoublyLinkedListFrame(self.content_frame)
        elif structure_type == "Binary Tree":
            self.current_frame = BinaryTreeFrame(self.content_frame)
        elif structure_type == "Binary Search Tree":
            self.current_frame = BinarySearchTreeFrame(self.content_frame)

        # Replace the structure with the loaded one
        if self.current_frame:
            self.current_frame.structure = structure
            self.current_frame.update_info()
            self.current_frame.pack(fill=tk.BOTH, expand=True)
            self.current_frame.update_visualization()

            # Create a safe resize handler
            def safe_resize_handler(event):
                if self.current_frame and self.current_frame.winfo_exists():
                    try:
                        self.current_frame.update_visualization()
                    except (tk.TclError, AttributeError):
                        # Silently ignore errors if the widget no longer exists
                        pass

            # Bind resize event to update visualization
            self.bind("<Configure>", safe_resize_handler)

            messagebox.showinfo("Load", "Structure loaded successfully.")

    def show_welcome(self):
        """Show welcome message frame."""
        welcome_frame = ttk.Frame(self.content_frame)
        welcome_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(welcome_frame,
                  text="Data Structure Visualizer",
                  font=("TkDefaultFont", 24, "bold")).pack(pady=(100, 20))

        ttk.Label(welcome_frame,
                  text="Select a data structure type from the dropdown menu to begin.",
                  font=("TkDefaultFont", 12)).pack(pady=10)

        ttk.Label(welcome_frame,
                  text="This tool allows you to visualize and interact with various data structures,\n"
                       "helping you understand how they work.",
                  font=("TkDefaultFont", 10)).pack(pady=10)

        self.current_frame = welcome_frame

    def show_about(self):
        """Show about dialog."""
        about_text = "Data Structure Visualizer\n\n" \
                     "Created for the Data Structures course.\n" \
                     "This application helps students understand\n" \
                     "different data structures through visualization.\n\n" \
                     "© 2025 - All rights reserved"

        messagebox.showinfo("About", about_text)


if __name__ == "__main__":
    app = DataStructureVisualizer()
    app.mainloop()