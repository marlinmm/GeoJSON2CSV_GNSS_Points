import fiona
from xml.etree.ElementTree import ElementTree
from shapely.geometry import Point, mapping
import geopandas as gpd
import pyproj
from functools import partial
from shapely.ops import transform


def input_dtype_selection(input_file):
    # Get coordinates to variable
    if input_file[-3:len(input_file)] == "shp":
        poi_coordinates = extract_points_from_shape(input_file)
    if input_file[-3:len(input_file)] == "kml":
        poi_coordinates = extract_points_from_kml(input_file)
    else:
        print("File format nor supported")

    poi_geoseries = gpd.GeoSeries([Point(poi_coordinates)])
    poi_coord = mapping(poi_geoseries)["features"][0]["geometry"]["coordinates"]
    return poi_coord


# Function extract points (coordinates) from shapefile
def extract_points_from_shape(path_to_file):
    with fiona.open(path_to_file) as source:
        # Iterate the features of the original shapefile
        for elem in source:
            # Extract the geometries in one element (split the MultiLineString)
            point_coordinates = elem["geometry"]["coordinates"]
            return point_coordinates[0:2]


def extract_points_from_kml(path_to_file):
    tree = ElementTree()
    tree.parse(path_to_file)
    point_coordinates = tree.find(".//{http://www.opengis.net/kml/2.2}coordinates").text
    point_coordinates = point_coordinates.split(",")[0:2]
    point_coordinates = tuple(map(float, point_coordinates))
    return point_coordinates


# Convert coordinates to Azimuthal equidistant projection to generate round buffer around POI
def geodesic_point_buffer(lat, lon, m):
    # Set initial projection
    proj_wgs84 = pyproj.Proj('+proj=longlat +datum=WGS84')
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
