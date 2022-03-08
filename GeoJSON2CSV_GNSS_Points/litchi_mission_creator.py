import os
from functools import partial
import pyproj
from shapely.ops import transform
import fiona
import pandas as pd
import geopandas as gpd
import numpy as np


# Set path to POI (point) shapefile
poi_shapefile = "C:/Users/muel_m31/Desktop/UCEA/Litchi/Shapes/litchi_test_file_centerpoint.shp"

# Set output path and output filename:
out_path = "C:/Users/muel_m31/Desktop/UCEA/Litchi/Missions"
out_filename = "jena_forst_test3.csv"

# Set other flight parameters:
altitude = 120  # meters
photo_timeinterval = 3  # seconds
poi_radius = 150  # meters

# Load default Litchi mission file
litchi_default_mission = "empty_litchi_mission.csv"
litchi_mission = pd.read_csv(litchi_default_mission)

# Extract column names of the default mission to list
column_titles_list = litchi_mission.columns.tolist()
column_titles = str(column_titles_list)[1:len(str(column_titles_list)) - 1] + str("\n")

# Extract default values of the default mission to list
default_mission_values = litchi_mission.values.tolist()[0]


# Function extract points (coordinates) from shapefile
def extract_points_from_shape(path_to_file):
    with fiona.open(path_to_file) as source:
        # Iterate the features of the original shapefile
        for elem in source:
            # Extract the geometries in one element (split the MultiLineString)
            point_coordinates = elem["geometry"]["coordinates"]
            return point_coordinates


from shapely.geometry import Point, mapping

# Get coordinates to variable
poi_coordinates = extract_points_from_shape(poi_shapefile)[0:2]
poi_geoseries = gpd.GeoSeries([Point(poi_coordinates)])
poi_coord = mapping(poi_geoseries)["features"][0]["geometry"]["coordinates"]

# Set initial projection
proj_wgs84 = pyproj.Proj('+proj=longlat +datum=WGS84')


# Convert coordinates to Azimuthal equidistant projection to generate round buffer around POI
def geodesic_point_buffer(lat, lon, m):
    # Thanks to: https://gis.stackexchange.com/a/289923
    # Azimuthal equidistant projection
    aeqd_proj = '+proj=aeqd +lat_0={lat} +lon_0={lon} +x_0=0 +y_0=0'
    project = partial(
        pyproj.transform,
        pyproj.Proj(aeqd_proj.format(lat=lat, lon=lon)),
        proj_wgs84)
    # Create buffer
    buf = Point(0, 0).buffer(m)  # distance in metres
    return transform(project, buf).exterior.coords[:]


# Call function to generate round buffer with WGS84 coordinates
buffer_coordinates = geodesic_point_buffer(poi_coord[1], poi_coord[0], poi_radius)

# Initialize Litchi default dictionary
litchi_dict = dict(zip(column_titles_list, default_mission_values))
mission_values_array = []

# Get datatpye for each parameter and set correct one for POI parameters
dataTypeDict = dict(litchi_mission.dtypes)
dataTypeDict["poi_latitude"] = np.dtype(float)
dataTypeDict["poi_longitude"] = np.dtype(float)

# Append coordinate of each waypoint to the output dataset
# for coordinate in shapefile_coordinates:
for coordinate in buffer_coordinates:
    # print(coordinate)
    # output_string = column_titles + litchi_dict["latitude"]

    # Set wanted values for each parameter iterating through all waypoints
    litchi_dict["latitude"] = coordinate[1]
    litchi_dict["longitude"] = coordinate[0]
    litchi_dict["altitude(m)"] = altitude
    # litchi_dict["heading(deg)"] = 250
    # litchi_dict["gimbalpitchangle"] = -65
    litchi_dict["poi_latitude"] = poi_coordinates[1]
    litchi_dict["poi_longitude"] = poi_coordinates[0]
    # litchi_dict["poi_altitude(m)"] = 0
    litchi_dict["photo_timeinterval"] = photo_timeinterval

    # Set all values to float and append to list for output:
    litchi_mission_values = np.fromiter(litchi_dict.values(), dtype=float)
    mission_values_array.append(litchi_mission_values)

# Change dataset to array and pandas dataframe with correct column names from default file
mission_values_array = np.asarray(mission_values_array)
df = pd.DataFrame(mission_values_array, columns=column_titles_list)

# Change datatype for each column to the correct dtype
df = df.astype(dataTypeDict)

# Export to csv
df.to_csv(os.path.join(out_path, out_filename), index=False)
