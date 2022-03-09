# import os
# import fiona
# import pyproj
# import numpy as np
# import pandas as pd
# import geopandas as gpd
# from functools import partial
# from shapely.ops import transform
# from shapely.geometry import Point, mapping
# from xml.etree.ElementTree import ElementTree
# from Litchi_grid_mission import shape_to_grid_mission
#
# # Set path to POI (point) file (.shp or .kml)
# poi_file = "C:/Users/muel_m31/Desktop/UCEA/Litchi/Shapes/jena_forst_polygon.shp"
#
# # Set output path and output filename:
# out_path = "C:/Users/muel_m31/Desktop/UCEA/Litchi/Missions"
# out_filename = "jena_forst_test_v4"
#
# # Set other flight parameters:
# altitude = 150  # meters
# photo_timeinterval = 3  # seconds
# poi_radius = 100  # meters
#
# final_out_filename = out_filename + "_" + str(altitude) + "m_" + str(photo_timeinterval) + "s_" + str(poi_radius) + \
#                      "m.csv"
#
# # Load default Litchi mission file
# litchi_default_mission = "empty_litchi_mission.csv"
# litchi_mission = pd.read_csv(litchi_default_mission)
#
# # Extract column names of the default mission to list
# column_titles_list = litchi_mission.columns.tolist()
# column_titles = str(column_titles_list)[1:len(str(column_titles_list)) - 1] + str("\n")
#
# # Extract default values of the default mission to list
# default_mission_values = litchi_mission.values.tolist()[0]
#
#
# # Function extract points (coordinates) from shapefile
# def extract_points_from_shape(path_to_file):
#     with fiona.open(path_to_file) as source:
#         # Iterate the features of the original shapefile
#         for elem in source:
#             # Extract the geometries in one element (split the MultiLineString)
#             point_coordinates = elem["geometry"]["coordinates"]
#             return point_coordinates[0:2]
#
#
# def extract_points_from_kml(path_to_file):
#     tree = ElementTree()
#     tree.parse(path_to_file)
#     point_coordinates = tree.find(".//{http://www.opengis.net/kml/2.2}coordinates").text
#     point_coordinates = point_coordinates.split(",")[0:2]
#     point_coordinates = tuple(map(float, point_coordinates))
#     return point_coordinates
#
#
# # Get coordinates to variable
# if poi_file[-3:len(poi_file)] == "shp":
#     poi_coordinates = extract_points_from_shape(poi_file)
# if poi_file[-3:len(poi_file)] == "kml":
#     poi_coordinates = extract_points_from_kml(poi_file)
# else:
#     print("File format nor supported")
# poi_geoseries = gpd.GeoSeries([Point(poi_coordinates)])
# poi_coord = mapping(poi_geoseries)["features"][0]["geometry"]["coordinates"]
#
# # Set initial projection
# proj_wgs84 = pyproj.Proj('+proj=longlat +datum=WGS84')
#
#
# # Convert coordinates to Azimuthal equidistant projection to generate round buffer around POI
# def geodesic_point_buffer(lat, lon, m):
#     # Thanks to: https://gis.stackexchange.com/a/289923
#     # Azimuthal equidistant projection
#     aeqd_proj = '+proj=aeqd +lat_0={lat} +lon_0={lon} +x_0=0 +y_0=0'
#     project = partial(
#         pyproj.transform,
#         pyproj.Proj(aeqd_proj.format(lat=lat, lon=lon)),
#         proj_wgs84)
#     print(project)
#     # Create buffer
#     buf = Point(0, 0).buffer(m)  # distance in metres
#     print(buf)
#     test = transform(project, buf).exterior.coords[:]
#     print(test)
#     # print(buf)
#     return transform(project, buf).exterior.coords[:]
#
#
# #  Call function to generate round buffer with WGS84 coordinates
# buffer_coordinates = geodesic_point_buffer(poi_coord[1], poi_coord[0], poi_radius)
#
# buffer_coordinates = shape_to_grid_mission(path_to_file=poi_file)
#
# # Initialize Litchi default dictionary
# litchi_dict = dict(zip(column_titles_list, default_mission_values))
# mission_values_array = []
#
# # Get datatpye for each parameter and set correct one for POI parameters
# dataTypeDict = dict(litchi_mission.dtypes)
# dataTypeDict["poi_latitude"] = np.dtype(float)
# dataTypeDict["poi_longitude"] = np.dtype(float)
#
# # Append coordinate of each waypoint to the output dataset
# for coordinate in buffer_coordinates:
#     # Set wanted values for each parameter iterating through all waypoints
#     litchi_dict["latitude"] = coordinate[1]
#     litchi_dict["longitude"] = coordinate[0]
#     litchi_dict["altitude(m)"] = altitude
#     litchi_dict["poi_latitude"] = poi_coordinates[1]
#     litchi_dict["poi_longitude"] = poi_coordinates[0]
#     # litchi_dict["photo_timeinterval"] = photo_timeinterval
#
#     # # test parameters
#     litchi_dict["gimbalmode"] = 2
#     litchi_dict["gimbalpitchangle"] = -90
#     litchi_dict["speed(m/s)"] = 1.2
#     litchi_dict["photo_timeinterval"] = -1
#     litchi_dict["photo_distinterval"] = 20
#
#
#
#     # Set all values to float and append to list for output:
#     litchi_mission_values = np.fromiter(litchi_dict.values(), dtype=float)
#     mission_values_array.append(litchi_mission_values)
#
# # Change dataset to array and pandas dataframe with correct column names from default file
# mission_values_array = np.asarray(mission_values_array)
# df = pd.DataFrame(mission_values_array, columns=column_titles_list)
#
# # Change datatype for each column to the correct dtype
# df = df.astype(dataTypeDict)
#
# # Export to csv
# df.to_csv(os.path.join(out_path, final_out_filename), index=False)
