import geopandas as gpd
from shapely.geometry import Point


def shape_to_grid_mission(path_to_file, altitude, side_overlap):
    jena_forst_polygon = gpd.read_file(path_to_file)
    jena_forst_32632 = jena_forst_polygon.to_crs(epsg=32632)
    jena_forst_bouds_32632 = jena_forst_32632.total_bounds

    side_multiplicator = 1.333

    side_distance = altitude * side_multiplicator - (altitude * side_multiplicator / 100 * side_overlap)

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
    geopandas_coord_list = gpd.GeoSeries(coordinate_list, crs="EPSG:32632").to_crs(epsg=4326)
    coordinate_list = [(x, y) for x, y in zip(geopandas_coord_list.x, geopandas_coord_list.y)]
    return coordinate_list
