# BlueRobotics_Bar100sensor
For correcting pressure measurements collected with the Bar100 sensor from Blue Robotics


For correcting pressure measurements collected with the Bar100 sensor from Blue Robotics by calculating a baseline at sealevel from the first few measurements obtained and calculating the correct depth based on the corrected values

**Inputs**
- A .txt file with comma-separated data values where the first column contains timestamps (assumes ms but can be anything), the second has temperature (assumes degrees C), and third column has pressure values (must be in mbar)
(e.g. the file obtained by running the "DepthDataToSD.ino" Arduino sketch found in the "Arduino_code" repository)
- The path to that file

**Outputs**
- A .csv file containing corrected measurements (Timestamp in ms, Degrees C, Original mbar, Corrected mbar, Depth in m)
- A .png file of a plot showing the temperature across time
- A .png file of a plot showing the corrected pressure measurements across time
- A .png file of a plot showing the corrected depth measurements across time
