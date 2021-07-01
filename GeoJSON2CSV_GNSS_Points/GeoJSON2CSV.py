import os
from os.path import join
import glob
import json
import csv

print("Specify desired accuracy in m (e.g. 0.02): ")
acc = float(input())
print("Specify height of RTK stick in m (e.g. 2): ")
rtk_stick = float(input())

# Get list of files in current folder
path = "D:/Aktuelles/DLR/Befliegung_JenaForst/GPS_Stab_Juni"
extension = '*.geojson'
list_json = glob.glob(join(path, extension))
names = [w[:-8] for w in list_json]
print(list_json)
print(names)

# inititate lists for later use
accuracy_average_list = []
x_coord_average_list = []
y_coord_average_list = []
altitude_average_list = []
alt_string_avg_list = []
time_list = []
counter_list = []
all_data_points_list = []
min_accuracy_list = []
max_accuracy_list = []

# loop to iterate through all geojson-files
for j,file in enumerate(list_json):
    with open(list_json[j]) as file:
        data = json.load(file)
    #print(data)

    # add start time to list
    time = data["features"][0]["properties"]["time"]
    time_list.append(time)
    counter = 0

    # values-lists to be reset for every new file
    accuracy_list = []
    x_coord_list = []
    y_coord_list = []
    altitude_list = []
    all_accuracy_list = []

    # loop to iterate through all features
    for i,features in enumerate(data["features"]):

        # get all accuracy values to determine min and max values
        all_accuracy = float(data["features"][i]["properties"]["accuracy"])
        all_accuracy_list.append(all_accuracy)

        # loop to check if the accuracy is below specified value
        if float((data["features"][i]["properties"]["accuracy"])) <= acc:
            counter += 1

            # Accuracy
            accuracy = float(data["features"][i]["properties"]["accuracy"])
            accuracy_list.append(accuracy)
            accuracy_average = sum(accuracy_list)/len(accuracy_list)

            # X_coordinates
            x_coord = float(data["features"][i]["geometry"]["coordinates"][0])
            x_coord_list.append(x_coord)
            x_coord_average = sum(x_coord_list)/len(x_coord_list)

            # Y_coordinates
            y_coord = float(data["features"][i]["geometry"]["coordinates"][1])
            y_coord_list.append(y_coord)
            y_coord_average = sum(y_coord_list)/len(y_coord_list)

            # Altitude
            altitude = float(data["features"][i]["properties"]["altitude"])
            altitude_list.append(altitude)
            altitude_average = sum(altitude_list)/len(altitude_list) - rtk_stick

            # parse to strings
            acc_string = str(accuracy_average)
            x_coord_string = str(x_coord_average)
            y_coord_string = str(y_coord_average)
            alti_string = str(altitude_average)

    # Count number of all data points:
    all_data_points = str(i+1)
    all_data_points_list.append(all_data_points)

    #Counting of used points
    counter_string = str(counter)
    counter_list.append(counter_string)

    # worst accuracy value per point
    min_accuracy = str(max(all_accuracy_list))
    min_accuracy_list.append(min_accuracy)

    # best accuracy value per point
    max_accuracy = str(min(all_accuracy_list))
    max_accuracy_list.append(max_accuracy)


    # Collection of average values
    accuracy_average_list.append(acc_string)
    x_coord_average_list.append(x_coord_string)
    y_coord_average_list.append(y_coord_string)
    altitude_average_list.append(alti_string)

rows = zip(names,time_list, accuracy_average_list, x_coord_average_list, y_coord_average_list, altitude_average_list, max_accuracy_list, min_accuracy_list, counter_list, all_data_points_list)

with open("D:/Aktuelles/DLR/Befliegung_JenaForst/GPS_Stab_Juni/GNSS_Points_Juni_corrected.csv", "w") as csvFile:
    writer = csv.writer(csvFile)
    writer.writerow(["Point", "Time", "Accuracy", "X_Coord", "Y_Coord", "Altitude", "Best_Accuracy", "Worst_Accuracy", "No. Of Used Points", "No. Of All Points"])
    for row in rows:
        writer.writerow(row)
