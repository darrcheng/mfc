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
import shutil
from version import VERSION

# Ensure configuration file exists in the working directory
config_filename = "mfc_config.yml"
default_config_path = os.path.join(os.path.dirname(__file__), config_filename)
user_config_path = os.path.join(os.getcwd(), config_filename)

if not os.path.exists(user_config_path):
    shutil.copy(default_config_path, user_config_path)
    print(f"Default configuration file copied to {user_config_path}")

# Check for README_USER.txt and copy it to the working directory if it doesn't exist
readme_filename = f"README_USER_v{VERSION}.txt"
readme_path = os.path.join(os.getcwd(), readme_filename)
if not os.path.exists(readme_path):
    bundled_readme_path = os.path.join(
        os.path.dirname(__file__), "README_USER.txt"
    )
    shutil.copy(bundled_readme_path, readme_path)
    print(f"README file copied to {readme_path}")

# Load configuration
with open(user_config_path, "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

num_mfc = config["num_mfc"]
read_interval = config["read_interval"]

# Update the image path to dynamically locate the file in the same directory as the script
image_path = os.path.join(os.path.dirname(__file__), config["mfc_layout_image"])

# Initialize LabJack interface
labjack = LabJackInterface(use_mock=False)

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
data_dir = os.path.join(os.getcwd(), "data", start_time.strftime("%Y-%m-%d"))
os.makedirs(data_dir, exist_ok=True)
csv_filepath = os.path.join(
    data_dir,
    f"MFC_{start_time.strftime('%Y%m%d_%H%M%S')}.csv",
)
header = ["datetime"]
for mfc in mfc_list:
    header.append(f"{mfc.name}_setpoint")
    header.append(f"{mfc.name}_flowrate")
with open(csv_filepath, mode="w", newline="") as data_file:
    csv.writer(data_file).writerow(header)

# Tkinter GUI setup
root = tk.Tk()

# Update the title of the GUI window to include the version number
root.title(f"MFC Controller v{VERSION}")


# Callback to set all setpoints
def set_all_setpoints():
    setpoints = ui.get_setpoints()
    for mfc in mfc_list:
        mfc.set_flow(setpoints[mfc.name])
    # Update the setpoint labels dynamically after setting all setpoints
    for mfc in mfc_list:
        ui.update_setpoint_label(mfc.name, setpoints[mfc.name])


# Initialize UI
ui = MFCUI(root, mfc_list, config, set_all_setpoints)


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
