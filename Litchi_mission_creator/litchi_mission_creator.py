import os
import numpy as np
import pandas as pd
from Litchi_grid_mission import shape_to_grid_mission
from POI_mission import *

# Set path to POI (point) file (.shp or .kml)
input_file = "C:/Users/muel_m31/Desktop/UCEA/Litchi/Shapes/jena_forst_polygon.shp"  # grid
# input_file = "C:/Users/muel_m31/Desktop/UCEA/Litchi/Shapes/jena_forst_poi.shp"  # poi

# Set output path and output filename:
out_path = "C:/Users/muel_m31/Desktop/UCEA/Litchi/Missions"
out_filename = "jena_forst_test_grid"

# Set other flight parameters:
altitude = 100  # meters
photo_timeinterval = 3  # seconds
poi_radius = 100  # meters
front_overlap = 80  # percent
side_overlap = 80  # percent
gimbal_angle = -90  # degrees (0 to -90)

# EPSG code for correct calculateions of flight pattern (Jena: 32632, Aklavik:32608)
projected_crs_epsg_code = 32632

# Mission bool sets type of mission (POI mission: "poi", Grid mission: "grid")
mission_bool = "grid"


def mission_creator():
    final_out_filename = out_filename + "_" + str(altitude) + "m_" + str(photo_timeinterval) + "s_" + str(poi_radius) + \
                         "m.csv"

    # Load default Litchi mission file
    litchi_default_mission = "empty_litchi_mission.csv"
    litchi_mission = pd.read_csv(litchi_default_mission)

    # Extract column names of the default mission to list
    column_titles_list = litchi_mission.columns.tolist()
    column_titles = str(column_titles_list)[1:len(str(column_titles_list)) - 1] + str("\n")

    # Extract default values of the default mission to list
    default_mission_values = litchi_mission.values.tolist()[0]

    if mission_bool == "poi":
        poi_coord = input_dtype_selection(input_file)
        mission_coordinates = geodesic_point_buffer(poi_coord[1], poi_coord[0], poi_radius)

    if mission_bool == "grid":
        mission_coordinates = shape_to_grid_mission(input_file, altitude, side_overlap)

    # Initialize Litchi default dictionary
    litchi_dict = dict(zip(column_titles_list, default_mission_values))
    mission_values_array = []

    # Get datatpye for each parameter and set correct one for POI parameters
    dataTypeDict = dict(litchi_mission.dtypes)
    dataTypeDict["poi_latitude"] = np.dtype(float)
    dataTypeDict["poi_longitude"] = np.dtype(float)

    # Append coordinate of each waypoint to the output dataset
    for coordinate in mission_coordinates:
        # Set wanted values for each parameter iterating through all waypoints
        if mission_bool == "poi":
            litchi_dict["latitude"] = coordinate[1]
            litchi_dict["longitude"] = coordinate[0]
            litchi_dict["altitude(m)"] = altitude
            litchi_dict["poi_latitude"] = poi_coord[1]
            litchi_dict["poi_longitude"] = poi_coord[0]
            litchi_dict["photo_timeinterval"] = photo_timeinterval

        if mission_bool == "grid":
            litchi_dict["latitude"] = coordinate[1]
            litchi_dict["longitude"] = coordinate[0]
            litchi_dict["altitude(m)"] = altitude
            litchi_dict["gimbalmode"] = 2
            litchi_dict["gimbalpitchangle"] = gimbal_angle
            litchi_dict["speed(m/s)"] = 1.2
            litchi_dict["photo_timeinterval"] = -1
            litchi_dict["photo_distinterval"] = altitude - altitude / 100 * front_overlap

        # Set all values to float and append to list for output:
        litchi_mission_values = np.fromiter(litchi_dict.values(), dtype=float)
        mission_values_array.append(litchi_mission_values)

    # Change dataset to array and pandas dataframe with correct column names from default file
    mission_values_array = np.asarray(mission_values_array)
    df = pd.DataFrame(mission_values_array, columns=column_titles_list)

    # Change datatype for each column to the correct dtype
    df = df.astype(dataTypeDict)

    # Export to csv
    df.to_csv(os.path.join(out_path, final_out_filename), index=False)


mission_creator()
