import json
import pickle
import os
from tkinter import filedialog, messagebox


class FileManager:
    """Class for handling file operations (save and load data structures)."""

    @staticmethod
    def save_structure(structure, structure_type):
        """Save a data structure to a file."""
        # Ask user for file path
        file_path = filedialog.asksaveasfilename(
            defaultextension=".dsv",
            filetypes=[("Data Structure Visualizer", "*.dsv"), ("All Files", "*.*")],
            title="Save Structure"
        )

        if not file_path:
            return False  # User cancelled

        try:
            # Create a dictionary with structure info
            data = {
                "type": structure_type,
                "data": pickle.dumps(structure)
            }

            # Save as JSON file with pickle-serialized data
            with open(file_path, 'wb') as file:
                pickle.dump(data, file)

            return True

        except Exception as e:
            messagebox.showerror("Save Error", f"Error saving file: {str(e)}")
            return False

    @staticmethod
    def load_structure():
        """Load a data structure from a file."""
        # Ask user for file path
        file_path = filedialog.askopenfilename(
            defaultextension=".dsv",
            filetypes=[("Data Structure Visualizer", "*.dsv"), ("All Files", "*.*")],
            title="Load Structure"
        )

        if not file_path:
            return None, None  # User cancelled

        try:
            # Load from pickle file
            with open(file_path, 'rb') as file:
                data = pickle.load(file)

            structure_type = data.get("type")
            structure = pickle.loads(data.get("data"))

            return structure_type, structure

        except Exception as e:
            messagebox.showerror("Load Error", f"Error loading file: {str(e)}")
            return None, None