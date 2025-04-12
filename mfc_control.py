import csv
from datetime import datetime
import os
import time
import tkinter as tk
from tkinter import ttk, PhotoImage, Canvas, Scrollbar
from labjack import ljm
import yaml
import threading
import random
import traceback
from PIL import Image, ImageTk


# Abstract LabJack functions into a class
class LabJackInterface:
    def __init__(self, use_mock=False):
        self.use_mock = use_mock
        if not use_mock:
            self.handle = ljm.openS("ANY", "ANY", "ANY")

    def write_name(self, name, value):
        if self.use_mock:
            print(f"Mock write: {name} = {value}")
        else:
            ljm.eWriteName(self.handle, name, value)

    def read_name(self, name):
        if self.use_mock:
            return random.uniform(0, 100)  # Mock random flowrate
        else:
            return ljm.eReadName(self.handle, name)

    def close(self):
        if not self.use_mock:
            ljm.close(self.handle)


# Load config file
program_path = os.path.dirname(os.path.realpath(__file__))
with open("mfc_config.yml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

num_mfc = config["num_mfc"]

# Create file
start_time = datetime.now()
current_date = start_time.strftime("%Y-%m-%d")
subfolder_path = os.path.join(os.getcwd(), current_date)
os.makedirs(subfolder_path, exist_ok=True)

# Create CSV file and writer
file_datetime = start_time.strftime("%Y%m%d_%H%M%S")
csv_filename = "MFC_" + file_datetime + ".csv"
csv_filepath = os.path.join(subfolder_path, csv_filename)

# Create file header
header = ["datetime"]
for i in range(num_mfc):
    header.append(config[f"mfc{i+1}"]["name"] + "_setpoint")
    header.append(config[f"mfc{i+1}"]["name"] + "_flowrate")

# Write CSV header
with open(csv_filepath, mode="w", newline="") as data_file:
    data_writer = csv.writer(data_file, delimiter=",")
    data_writer.writerow(header)

# Initialize LabJack interface
labjack = LabJackInterface(use_mock=True)  # Set to False for real LabJack

# Set the MFCs
for i in range(num_mfc):
    mfc = config[f"mfc{i+1}"]
    setpoint = mfc["setpoint"]
    scale = mfc["scale"]
    offset = mfc["offset"]
    labjack.write_name(mfc["flow_set"], (setpoint - offset) / scale)


def set_all_setpoints():
    for i in range(num_mfc):
        mfc_name = config[f"mfc{i+1}"]["name"]
        new_setpoint = float(setpoint_entries[mfc_name].get())
        config[f"mfc{i+1}"]["setpoint"] = new_setpoint
        labjack.write_name(
            config[f"mfc{i+1}"]["flow_set"],
            (new_setpoint - config[f"mfc{i+1}"]["offset"])
            / config[f"mfc{i+1}"]["scale"],
        )
        mfc_setpoints[mfc_name].config(text=f"Setpoint: {new_setpoint}")


# Tkinter GUI setup
root = tk.Tk()
root.title("MFC Controller")

# Adjust layout to create two frames on the left and one on the right
mfc_info_frame = ttk.Frame(root, padding=10)
mfc_info_frame.grid(row=0, column=0, sticky="n")

button_frame = ttk.Frame(root, padding=10)
button_frame.grid(row=1, column=0, sticky="n")

image_frame = ttk.Frame(root, padding=10)
image_frame.grid(row=0, column=1, rowspan=2, sticky="n")

# Load and resize the image for MFC layout
image_path = os.path.join(program_path, config["mfc_layout_image"])
try:
    original_image = Image.open(image_path)
    resized_image = original_image.resize((400, 400), Image.Resampling.LANCZOS)
    mfc_image = ImageTk.PhotoImage(resized_image)
    image_label = ttk.Label(image_frame, image=mfc_image)
    image_label.grid(row=0, column=0, padx=20, pady=10, sticky="n")
    # Ensure the image is displayed correctly by attaching it to the image_label
    image_label.image = mfc_image
except Exception as e:
    print(f"Error loading image: {e}")

# Configure grid weights to ensure proper layout
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(0, weight=1)

# Move MFC settings to the mfc_info_frame
mfc_frame = ttk.Frame(mfc_info_frame, padding=10)
mfc_frame.grid(row=0, column=0, sticky="n")

# Create MFC frames
mfc_labels = {}
mfc_setpoints = {}
mfc_flows = {}
setpoint_entries = {}

# Adjust layout to split MFCs into multiple columns if there are more than 4
max_mfc_per_column = 4
for i in range(num_mfc):
    mfc = config[f"mfc{i+1}"]
    column = i // max_mfc_per_column
    row = i % max_mfc_per_column

    frame = ttk.Frame(mfc_info_frame, padding=10)
    frame.grid(row=row, column=column, sticky="w")

    ttk.Label(frame, text=f"{mfc['name']}:", font=("Arial", 12, "bold")).grid(
        row=0, column=0, sticky="w"
    )
    setpoint_label = ttk.Label(frame, text=f"Setpoint: {mfc['setpoint']}")
    setpoint_label.grid(row=1, column=0, sticky="w")
    mfc_setpoints[mfc["name"]] = setpoint_label

    setpoint_entry = ttk.Spinbox(
        frame, from_=0, to=100000, increment=100, width=10
    )
    setpoint_entry.insert(0, mfc["setpoint"])
    setpoint_entry.grid(row=1, column=1, sticky="w")
    setpoint_entries[mfc["name"]] = setpoint_entry

    flow_label = ttk.Label(frame, text="Flowrate: 0")
    flow_label.grid(row=2, column=0, sticky="w")
    mfc_flows[mfc["name"]] = flow_label

# Move the "Set All" button to the button_frame
set_button = ttk.Button(button_frame, text="Set All", command=set_all_setpoints)
set_button.grid(row=0, column=0, pady=10, sticky="ew")

# Reset the button style
set_button_style = ttk.Style()
set_button_style.configure("TButton")

# Add a label to display errors in the GUI
error_label = ttk.Label(root, text="", foreground="red")
error_label.grid(row=max_mfc_per_column + 1, column=0, pady=10)

# Adjust the window width to fit contents naturally
root.geometry("")
root.minsize(1, 500)
root.maxsize(root.winfo_screenwidth(), 500)

# Update the root window to fit its contents
root.update()


# Update flow rate readout to round to the nearest integer
def update_mfc_data():
    while True:
        try:
            data = [datetime.now()]
            for i in range(num_mfc):
                mfc = config[f"mfc{i+1}"]
                flowrate = round(
                    labjack.read_name(mfc["flow_read"]) * mfc["scale"]
                    + mfc["offset"]
                )
                mfc_flows[mfc["name"]].config(text=f"Flowrate: {flowrate}")
                data.extend([mfc["setpoint"], flowrate])

            with open(csv_filepath, mode="a", newline="") as data_file:
                csv.writer(data_file).writerow(data)

            time.sleep(config["read_interval"])
        except Exception as e:
            # Log the error and display it in the GUI
            error_message = f"Error: {str(e)}\n{traceback.format_exc()}"
            print(error_message)
            error_label.config(text=f"Error: {str(e)}")
            time.sleep(1)  # Prevent rapid error looping


# Run data update in a separate thread to keep GUI responsive
data_thread = threading.Thread(target=update_mfc_data, daemon=True)
data_thread.start()

# Run the Tkinter event loop
root.mainloop()
