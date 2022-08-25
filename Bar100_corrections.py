"""
For correcting pressure measurements collected with the Bar100 sensor from Blue Robotics 
by calculating a baseline at sealevel from the first few measurements obtained
and calculating the correct depth based on the corrected values

Inputs
- A .txt file with comma-separated data values where the first column contains timestamps (assumes ms but can be anything), the second has temperature (assumes degrees C), and third column has pressure values (must be in mbar)
(e.g. the file obtained by running the "DepthDataToSD.ino" Arduino sketch found in the "Arduino_code" repository)
- The path to that file

Outputs
- A .csv file containing corrected measurements (Timestamp in ms, Degrees C, Original mbar, Corrected mbar, Depth in m)
- A .png file of a plot showing the temperature across time
- A .png file of a plot showing the corrected pressure measurements across time
- A .png file of a plot showing the corrected depth measurements across time
"""

#############################################################
# INPUT - Define the path to where the DEPTH.txt file is
file_path = r"D:"
datafile = "DEPTH.txt" # if the file has a different name, change that here
#############################################################

# Import necessities
import csv
import numpy as np
import matplotlib.pyplot as plt

print(f"Opening {datafile} in {file_path}")

# Specify lists to save values in
tp=[]
degreesC=[]
mbar=[]

with open(f"{file_path}\\{datafile}") as csv_file: #Open the DEPTH.txt file as a csv file
    content = csv.reader(csv_file, delimiter=',') #Read the file
    rows=list(content) #Create a list of the content in the file
    
    for i in range(0,len(rows),1): #Loop through the rows
        current_row=rows[i]
        tp.append(int(current_row[0])) #Save the time point (in ms after Arduino sketch was uploaded)
        degreesC.append(float(current_row[1])) #Save the temperature (in degrees C)
        mbar.append(float(current_row[2])) #Save the pressure reading (in mbar)

# Correct the original pressure measurements by taking an average of the first few measurements, 
# subtracting this from the average known pressure at sealevel (1013.25 mbar), 
# and adding that to the original measurements
baseline = np.average(mbar[0:19]) #Average across e.g. 20 measurements to get baseline
mbar_corrected = mbar+(1013.25-baseline)

# Calculate depth by converting the mbar measurement to Pa (= mbar * 100),
# subtracting the pressure at sealevel in Pa (= 1013.25 mbar * 100) to get the change in pressure from sealevel,
# and dividing this by [the density of seawater (1029 kg/m2) multiplied with the acceleration of gravity (9.80665 m/s2)]
# I.e. (mbar*100-101325)/(1029*9.80665)
depth = ((mbar_corrected*100)-101325)/(1029*9.80665)

# Create a header for the new datafile
header = ['Timestamp in ms','Degrees C','Original mbar','Corrected mbar','Depth in m']

with open(f"{file_path}\\DEPTH_corrected.csv", 'w', newline='') as csv_file2: #Create/open a csv file to save the corrected data in
    writer = csv.writer(csv_file2) #Prepare to write to the newfile
    writer.writerow(header) #Add the header to the file

    for i in range(0,len(tp),1): #Loop through each row in the data/lists
        current_row=[tp[i], degreesC[i], mbar[i], round(mbar_corrected[i],2),round(depth[i],2)]
        writer.writerow(current_row)



####### Create plots (with x-axis in seconds) #######
tp_sec=np.divide(tp,1000)

# Temperature ###########################################
figure = plt.figure()
ax = figure.add_subplot(111)
plt.grid() #Show gridlines

ax.plot(tp_sec,degreesC) #Plot the data
ax.plot(tp_sec,np.ones(len(tp_sec))*5,color='k') #Plot a line at 5 degrees C
ax.plot(tp_sec,np.ones(len(tp_sec))*10,color='k') #Plot a line at 10 degrees C
ax.plot(tp_sec,np.ones(len(tp_sec))*15,color='k') #Plot a line at 15 degrees C
ax.plot(tp_sec,np.ones(len(tp_sec))*20,color='k') #Plot a line at 20 degrees C

plt.xticks(np.arange(0, len(tp), 60))
plt.yticks(np.arange(round(min(degreesC))-1,max(degreesC)+2, 1))

ax.spines['top'].set_visible(True)

plt.axis([-20,len(tp)+20,min(degreesC)-2,max(degreesC)+2])
plt.xlabel('Timestamp (s)')
plt.ylabel('Temperature (degrees Celsius)')

#Save the figure
plt.savefig(f"{file_path}\\{datafile[0:-4]}_temperature.png",dpi=300)


# Corrected pressure ###########################################
figure = plt.figure()
ax = figure.add_subplot(111)
plt.grid() #Show gridlines

ax.plot(tp_sec,mbar_corrected) #Plot the data

plt.xticks(np.arange(0, len(mbar_corrected), 60))
plt.yticks(np.arange(1000,max(mbar_corrected)+10, 100))

plt.axis([-20,len(tp)+20,min(mbar_corrected)-10,max(mbar_corrected)+50])
plt.xlabel('Timestamp (s)')
plt.ylabel('Corrected pressure (mbar)')

#Save the figure
plt.savefig(f"{file_path}\\{datafile[0:-4]}_correctedPressure.png",dpi=300)


# Calculated depth ###########################################
figure = plt.figure()
ax = figure.add_subplot(111)
plt.grid() #Show gridlines

ax.plot(tp_sec,depth) #Plot the data

plt.xticks(np.arange(0, len(depth), 60))
plt.yticks(np.arange(0,max(depth)+10, 10))

plt.axis([-20,len(tp)+20,min(depth)-2,max(depth)+2])
plt.xlabel('Timestamp (s)')
plt.ylabel('Calculated depth (m)')

#Save the figure
plt.savefig(f"{file_path}\\{datafile[0:-4]}_calculatedDepth.png",dpi=300)


print(f"New file DEPTH_corrected.csv and three figures saved in {file_path}")