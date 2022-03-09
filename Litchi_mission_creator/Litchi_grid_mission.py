import os
import numpy as np
import geopandas as gpd
from shapely.geometry import Point


# # Function extract points (coordinates) from shapefile
# def extract_points_from_shape(path_to_file):
#     with fiona.open(path_to_file) as source:
#         # Iterate the features of the original shapefile
#         for elem in source:
#             # Extract the geometries in one element (split the MultiLineString)
#             point_coordinates = elem["geometry"]["coordinates"]
#             return point_coordinates[0:2]


def shape_to_grid_mission(path_to_file):
    # path_to_file = "C:/Users/muel_m31/Desktop/UCEA/Litchi/Shapes/jena_forst_polygon.shp"

    jena_forst_polygon = gpd.read_file(path_to_file)
    print(jena_forst_polygon["geometry"])
    print(jena_forst_polygon.crs)
    print(jena_forst_polygon.total_bounds)

    jena_forst_32632 = jena_forst_polygon.to_crs(epsg=32632)

    print(jena_forst_32632.crs)
    jena_forst_bouds_32632 = jena_forst_32632.total_bounds
    print(jena_forst_32632.total_bounds)

    altitude = 150

    front_overlap = 60
    side_overlap = 60
    side_multiplicator = 1.333

    side_distance = altitude * side_multiplicator - (altitude * side_multiplicator / 100 * side_overlap)
    print(side_distance)

    coordinate_list = []
    counter = 1

    for i in range(int(jena_forst_bouds_32632[1]), int(jena_forst_bouds_32632[3]), int(side_distance)):
        if counter % 2 == 0:
            coordinate_list.append(Point(jena_forst_bouds_32632[0], i))
            coordinate_list.append(Point(jena_forst_bouds_32632[2], i))
        if counter % 2 != 0:
            coordinate_list.append(Point(jena_forst_bouds_32632[2], i))
            coordinate_list.append(Point(jena_forst_bouds_32632[0], i))
        counter += 1
        print(counter)
    geopandas_coord_list = gpd.GeoSeries(coordinate_list, crs="EPSG:32632").to_crs(epsg=4326)
    coordinate_list = [(x, y) for x, y in zip(geopandas_coord_list.x, geopandas_coord_list.y)]
    return coordinate_list

    # print(coordinate_list)
    # for elem in geopandas_coord_list:
    #     print(elem.geometry)

    # print(geopandas_coord_list)
    # coordinates = extract_points_from_shape(path_to_file)
    # print(coordinates)
