# MFC Controller User Guide

## Overview
The MFC Controller application allows you to control and monitor Mass Flow Controllers (MFCs) using a graphical user interface (GUI). It supports real-time flow rate monitoring, dynamic setpoint adjustments, and data logging.

## Features
- Control multiple MFCs.
- Real-time flow rate monitoring.
- Adjustable setpoints via the GUI.
- Data logging in CSV format.
- User-replaceable layout image.

## Getting Started

### Running the Application
1. Double-click the executable file (`mfc_control.exe`) to start the application.
2. The GUI will open, displaying the MFCs and their current setpoints and flow rates.

### Adjusting Setpoints
1. Use the spinboxes next to each MFC to set the desired flow rate.
2. Click the "Set All" button to apply the changes.

### Monitoring Flow Rates
- The flow rates for each MFC are displayed in real-time under the "Flowrate" label.

### Data Logging
- Data is automatically logged in CSV format in a `data` directory, organized by date.

## Configuration

### Editing the Configuration File
1. Locate the `mfc_config.yml` file in the same directory as the executable.
2. Open the file in a text editor to modify settings such as the number of MFCs, read intervals, and MFC parameters.

Example configuration:
```yaml
mfc_layout_image: mfc_layout.png
num_mfc: 8
read_interval: 1
mfc1:
  name: "MFC 1"
  flow_set: "TDAC0"
  flow_read: "AIN0"
  scale: 10000
  offset: 0
  setpoint: 0
```

### MFC Naming Convention
Each MFC must be named sequentially in the configuration file, starting with `mfc1`, `mfc2`, and so on. This ensures proper identification and mapping in the application.

### Configuration Variables Explained
- `mfc_layout_image`: The filename of the layout image to display in the GUI.
- `num_mfc`: The number of MFCs to control.
- `read_interval`: The time interval (in seconds) between flow rate readings.
- `name`: A descriptive name for the MFC (e.g., "Dilution Flow").
- `flow_set`: The LabJack analong output for setting the flow rate.
- `flow_read`: The LabJack analog input for reading the flow rate.
- `scale`: Conversion factor for flow rate reading (e.g., maximum flow in SCCM / full scale voltage)
- `offset`: An offset to apply to the scaled reading.
- `setpoint`: The initial setpoint for the MFC in SCCM.

### Replacing the Layout Image
1. Replace the `mfc_layout.png` file in the same directory as the executable with your custom image.
2. Update the `mfc_layout_image` field in the `mfc_config.yml` file to match the new image filename.

## Troubleshooting

### Common Issues
- **Image Not Found**: Ensure the image file specified in `mfc_config.yml` exists in the same directory as the executable.
- **Flow Rates Not Updating**: Check the connection to the LabJack device.

## Support
For further assistance, contact the developer or refer to the GitHub repository for updates.