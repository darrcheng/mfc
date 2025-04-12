# Contains the GUI logic
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk


class MFCUI:
    def __init__(self, root, mfc_list, image_path, set_all_callback):
        self.root = root
        self.mfc_list = mfc_list
        self.set_all_callback = set_all_callback
        self.mfc_frames = {}
        self.setpoint_entries = {}
        self.setpoint_labels = {}
        self.flow_labels = {}

        # Layout setup
        self.mfc_info_frame = ttk.Frame(root, padding=10)
        self.mfc_info_frame.grid(row=0, column=0, sticky="n")

        self.button_frame = ttk.Frame(root, padding=10)
        self.button_frame.grid(row=1, column=0, sticky="n")

        self.image_frame = ttk.Frame(root, padding=10)
        self.image_frame.grid(row=0, column=1, rowspan=2, sticky="n")

        # Load and display image
        try:
            original_image = Image.open(image_path)
            original_width, original_height = original_image.size
            max_size = 400

            # Calculate new dimensions while maintaining aspect ratio
            if original_width > original_height:
                new_width = max_size
                new_height = int((original_height / original_width) * max_size)
            else:
                new_height = max_size
                new_width = int((original_width / original_height) * max_size)

            resized_image = original_image.resize(
                (new_width, new_height), Image.Resampling.LANCZOS
            )
            mfc_image = ImageTk.PhotoImage(resized_image)
            image_label = ttk.Label(self.image_frame, image=mfc_image)
            image_label.grid(row=0, column=0, padx=20, pady=10, sticky="n")
            image_label.image = mfc_image
        except Exception as e:
            print(f"Error loading image: {e}")

        # Create MFC frames
        self.create_mfc_frames()

        # Add "Set All" button
        set_button = ttk.Button(
            self.button_frame, text="Set All", command=self.set_all_callback
        )
        set_button.grid(row=0, column=0, pady=10, sticky="ew")

    def create_mfc_frames(self):
        max_mfc_per_column = 4
        for i, mfc in enumerate(self.mfc_list):
            column = i // max_mfc_per_column
            row = i % max_mfc_per_column

            frame = ttk.Frame(self.mfc_info_frame, padding=10)
            frame.grid(row=row, column=column, sticky="w")

            # Store the frame in the mfc_frames dictionary
            self.mfc_frames[mfc.name] = frame

            ttk.Label(
                frame, text=f"{mfc.name}:", font=("Arial", 12, "bold")
            ).grid(row=0, column=0, sticky="w")

            # Store the setpoint_label in a dictionary for dynamic updates
            setpoint_label = ttk.Label(frame, text=f"Setpoint: {mfc.setpoint}")
            setpoint_label.grid(row=1, column=0, sticky="w")
            self.setpoint_labels[mfc.name] = setpoint_label

            setpoint_entry = ttk.Spinbox(
                frame, from_=0, to=100000, increment=100, width=10
            )
            setpoint_entry.insert(0, mfc.setpoint)
            setpoint_entry.grid(row=1, column=1, sticky="w")
            self.setpoint_entries[mfc.name] = setpoint_entry

            flow_label = ttk.Label(frame, text="Flowrate: 0")
            flow_label.grid(row=2, column=0, sticky="w")
            self.flow_labels[mfc.name] = flow_label

    def update_flow_labels(self, flow_data):
        for name, flow in flow_data.items():
            self.flow_labels[name].config(text=f"Flowrate: {flow}")

    def get_setpoints(self):
        return {
            name: float(entry.get())
            for name, entry in self.setpoint_entries.items()
        }

    # Add a method to update the setpoint label dynamically
    def update_setpoint_label(self, name, setpoint):
        self.setpoint_labels[name].config(text=f"Setpoint: {int(setpoint)}")
