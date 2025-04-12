# mfc
Repository containing code to control MKS mass flow controllers

## Features
- Dynamic setpoint control for multiple MFCs using a Tkinter GUI.
- Supports up to 8 MFCs with automatic column layout adjustment for better visualization.
- Real-time flow rate monitoring with rounded integer values.
- CSV logging of setpoints and flow rates for data analysis.
- Mock mode for testing without a LabJack device.

## Requirements
- Python 3.7+
- LabJack LJM library
- Pillow (for image handling)
- PyYAML (for configuration file parsing)

## Installation
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

## Testing Without a LabJack
Enable mock mode by setting `use_mock=True` in the `LabJackInterface` initialization in `mfc_control.py`.

## License
This project is licensed under the MIT License.
