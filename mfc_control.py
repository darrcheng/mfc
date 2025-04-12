# Main program to initialize and run the MFC application
import os
import csv
import time
import threading
from datetime import datetime
import tkinter as tk
from mfc_core import LabJackInterface, MassFlowController
from mfc_ui import MFCUI
import yaml

# Load configuration
with open("mfc_config.yml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

num_mfc = config["num_mfc"]
read_interval = config["read_interval"]
image_path = config["mfc_layout_image"]

# Initialize LabJack interface
labjack = LabJackInterface(use_mock=True)

# Initialize MFCs
mfc_list = []
for i in range(num_mfc):
    mfc_config = config[f"mfc{i+1}"]
    mfc = MassFlowController(
        name=mfc_config["name"],
        flow_set=mfc_config["flow_set"],
        flow_read=mfc_config["flow_read"],
        scale=mfc_config["scale"],
        offset=mfc_config["offset"],
        setpoint=mfc_config["setpoint"],
        labjack=labjack,
    )
    mfc_list.append(mfc)

# Create CSV file
start_time = datetime.now()
csv_filepath = os.path.join(
    os.getcwd(),
    start_time.strftime("%Y-%m-%d"),
    f"MFC_{start_time.strftime('%Y%m%d_%H%M%S')}.csv",
)
os.makedirs(os.path.dirname(csv_filepath), exist_ok=True)
header = (
    ["datetime"]
    + [f"{mfc.name}_setpoint" for mfc in mfc_list]
    + [f"{mfc.name}_flowrate" for mfc in mfc_list]
)
with open(csv_filepath, mode="w", newline="") as data_file:
    csv.writer(data_file).writerow(header)

# Tkinter GUI setup
root = tk.Tk()
root.title("MFC Controller")


# Callback to set all setpoints
def set_all_setpoints():
    setpoints = ui.get_setpoints()
    for mfc in mfc_list:
        mfc.set_flow(setpoints[mfc.name])


# Initialize UI
ui = MFCUI(root, mfc_list, image_path, set_all_setpoints)


# Update MFC data
def update_mfc_data():
    while True:
        try:
            data = [datetime.now()]
            flow_data = {}
            for mfc in mfc_list:
                flow = mfc.get_flow()
                flow_data[mfc.name] = flow
                data.extend([mfc.setpoint, flow])

            # Update GUI
            ui.update_flow_labels(flow_data)

            # Write to CSV
            with open(csv_filepath, mode="a", newline="") as data_file:
                csv.writer(data_file).writerow(data)

            time.sleep(read_interval)
        except Exception as e:
            print(f"Error: {e}")


# Run data update in a separate thread
data_thread = threading.Thread(target=update_mfc_data, daemon=True)
data_thread.start()

# Run the Tkinter event loop
root.mainloop()
