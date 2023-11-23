from shapely.geometry import Polygon
from pyproj import Proj, transform

def polygon_to_metres(polygon, center): 
    in_crs = Proj(init='epsg:4326')
    out_crs = Proj(init='epsg:32648')
    polygon_meters = transform(in_crs, out_crs, *polygon.exterior.xy)
    polygon = Polygon(list(zip(polygon_meters[0], polygon_meters[1])))
    centroid_x, centroid_y = polygon.centroid.x, polygon.centroid.y 
    xs = [x - centroid_x + center[0] for x in polygon_meters[0]]
    ys = [y - centroid_y + center[1] for y in polygon_meters[1]]
    polygon_meters_shapely = Polygon(list(zip(xs, ys)))
    return polygon_meters_shapely

def resize_polygon(site, desired_scale=50, center=None):
    X, Y = site.exterior.xy
    current_width = max(X) - min(X)
    current_height = max(Y) - min(Y)
    longest_axis = max(current_width, current_height)
    scale_factor = desired_scale / longest_axis

    if center is None:
        center_x = current_width / 2
        center_y = current_height / 2
    else:
        center_x, center_y = center

    scaled_polygon_x = [(x - min(X)) * scale_factor for x in X]
    scaled_polygon_y = [(y - min(Y)) * scale_factor for y in Y]
      
    scaled_polygon = Polygon(list(zip(scaled_polygon_x,scaled_polygon_y)))

    x_off = scaled_polygon.centroid.x - center[0]
    y_off = scaled_polygon.centroid.y - center[1]
    centered_polygon_x = [x - x_off for x in scaled_polygon_x]
    centered_polygon_y = [y - y_off for y in scaled_polygon_y]
    
    scaled_polygon = Polygon(list(zip(centered_polygon_x,centered_polygon_y)))

    return scaled_polygon

