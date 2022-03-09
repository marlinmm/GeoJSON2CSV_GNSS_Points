from os.path import join
import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from sklearn.metrics import mean_squared_error

path = "C:/Users/muel_m31/Desktop/Shadow/Daten_lokal/"
file_name = "tree_circumference_cleaned_nan.csv"

file = join(path, file_name)

diameter_in_situ = []
diameter_UAV = []

with open(file ) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        girth_in_situ_measurement = row["girth_meas"]
        # if girth_in_situ_measurement == '':
        #     girth_in_situ_measurement = np.nan
        diameter_in_situ.append(float(girth_in_situ_measurement) / np.pi)
        diameter_UAV_measurement = row["diam_OM"]
        # if diameter_UAV_measurement == '':
        #     diameter_UAV_measurement = np.nan
        # circumference_UAV_measurement = 2 * np.pi * (float(diameter_UAV_measurement) / 2)
        diameter_UAV.append(float(diameter_UAV_measurement))
        # print(row['id'], row['circ_calc'])

    slope, intercept, r, p, se = stats.linregress(diameter_in_situ, diameter_UAV)
    r_squared = r**2

    rmse = mean_squared_error(diameter_in_situ, diameter_UAV, squared=False)

    fig = plt.figure()
    ax = fig.add_subplot()
    ax.text(60, 35, r'$R^2$: ' + str(round(r_squared, 3)), fontsize=15)
    ax.text(60, 30, r'RMSE: ' + str(round(rmse, 3)), fontsize=15)
    ax.scatter(diameter_in_situ, diameter_UAV)
    ax.set_xlabel('Diameter (in-situ)')
    ax.set_ylabel('Diameter (UAV-measured) ')
    plt.show()