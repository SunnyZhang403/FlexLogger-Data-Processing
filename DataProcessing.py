# Importing necessary libraries - please see technical overview for requirements for Python package
# installation if errors are arising from these
import pandas
import numpy as np
from matplotlib import pyplot as plt

# Insert calibration matrix values (each contained array represents a row)
# Adjust according to the serial number (currently calibrated for the sensor in MB077)
calarray = np.array([[0.00493, 0.02599,-0.01086,-0.76808, 0.03722,0.80085],[0.01620,0.99863, -0.00321,-0.43869, -0.01199, -0.48143],[0.90761,0.01884,0.9370, 0.02694,0.9553, -0.01468],[-0.17770, 6.6783, 5.14830, -2.55385, -5.28149, -2.84374],[-6.07294, -0.31815, 3.10343, 4.80038, 2.99016, -4.85802],[-0.04396, 3.93140, 0.06107,3.31785, 0.12418, 4.02453]])

# Read in data file - adjust filename according to the filename (follow the same formatting)
datacsv = pandas.read_csv(r"D:\\Laptop Archive\\Sunny\\School Work\\UofT 2022-2023\\Research\\No Force Data.csv")

# Process time data so it starts from 0 seconds
tdata = datacsv["Time"]
dataarray = np.array(datacsv)

def timedataprocessing(tdataarray):
    processedtdata =[]
    for j in range(len(tdataarray)):
        stime = 60*int(tdataarray[j][0:2])+int(tdataarray[j][3:5])+0.1*int(tdataarray[j][6])-(60*int(tdataarray[0][0:2])+int(tdataarray[0][3:5])+0.1*int(tdataarray[0][6]))
        processedtdata.append(stime)
    return processedtdata

tdatafinal = np.array(timedataprocessing(tdata))

# Extract only the 6 useful data points
def processdata(array, caldata):
    processeddata = []
    for i in range(len(array)):
        processeddata.append([np.dot(caldata[0], dataarray[i][1:7]),np.dot(caldata[1], dataarray[i][1:7]),np.dot(caldata[2], dataarray[i][1:7]),np.dot(caldata[3], dataarray[i][1:7]),np.dot(caldata[4], dataarray[i][1:7]),np.dot(caldata[5], dataarray[i][1:7])])
    return processeddata

finisheddata = np.array(processdata(dataarray, calarray))

#Plot data
FTplot = plt.plot(tdatafinal,finisheddata)
plt.xticks(range(int(min(tdatafinal)),int(max(tdatafinal)), 1))
plt.xlabel("Time (s)")

plt.legend(["Fx","Fy", "Fz","Tx","Ty","Tz"])
plt.show()

# Construct final array to write to file
finishedarray = []
for i in range(len(tdatafinal)):
    finishedarray.append([tdatafinal[i], finisheddata[i][0],finisheddata[i][1],finisheddata[i][2],finisheddata[i][3],finisheddata[i][4],finisheddata[i][5]])

# Write to file
finisheddataframe = pandas.DataFrame(finishedarray, None, ["Time [s]", "Fx [N]","Fy [N]", "Fz [N]","Tx [Nmm]","Ty[Nmm]","Tz[Nmm]"])
pandas.DataFrame.to_csv(finisheddataframe,r"D:\\Laptop Archive\\Sunny\\School Work\\UofT 2022-2023\\Research\\No Force Data [PROCESSED].csv")