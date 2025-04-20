# mfc
Repository containing code to control MKS mass flow controllers

## Features
- Dynamic setpoint control for multiple MFCs using a Tkinter GUI.
- Supports up to 8 MFCs with automatic column layout adjustment for better visualization.
- Real-time flow rate monitoring with rounded integer values.
- CSV logging of setpoints and flow rates for data analysis.
- Mock mode for testing without a LabJack device.
- Centralized version management for consistency across the project.
- Automatically organizes data files into date-based subdirectories.

## Requirements
- Python 3.7+
- LabJack LJM library
- Pillow (for image handling)
- PyYAML (for configuration file parsing)

## Installation
### Option 1
1. Download latest release:
   1. In right hand column, under Releases, navigate to latest release
   2. Download `mfc_control_vX.X.X.exe`
   3. Run `mfc_control_vX.X.X.exe` to create `mfc_config.yml` and `README_USER.txt`
### Option 2
1. Clone this repository:
   ```bash
   git clone https://github.com/your-repo/mfc.git
   cd mfc
   ```
2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration
Edit the `mfc_config.yml` file to define the MFCs and their parameters. Example:
```yaml
num_mfc: 8
read_interval: 1
mfc_layout_image: "mfc_layout.png"
mfc1:
  name: "SADR Extractor"
  flow_set: "TDAC0"
  flow_read: "AIN0"
  scale: 2000
  offset: 0
  setpoint: 4000
# Add more MFCs as needed
```

## Usage
1. Run the `mfc_control.py` script:
   ```bash
   python mfc_control.py
   ```
2. Use the GUI to adjust setpoints and monitor flow rates.

## Packaging as an Executable
To package the project as a standalone executable:
1. Ensure `PyInstaller` is installed:
   ```bash
   pip install pyinstaller
   ```
2. Run the following command to build the executable:
   ```bash
   pyinstaller mfc_control.spec
   ```
3. The executable will be available in the `dist` directory.

## Testing Without a LabJack
Enable mock mode by setting `use_mock=True` in the `LabJackInterface` initialization in `mfc_control.py`.

## License
This project is licensed under the MIT License.
