from shapely.geometry import Polygon
from pyproj import Proj, transform, Transformer
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

def polygon_to_metres(polygon, center=(0,0)): 
    in_crs = Proj('epsg:4326')
    out_crs = Proj('epsg:32648')
    # polygon_meters = transform(in_crs, out_crs, *polygon.exterior.xy)
    
    transformer = Transformer.from_crs("epsg:4326", "epsg:32648", always_xy=True)
    polygon_meters = transformer.transform(*polygon.exterior.xy)
    polygon = Polygon(list(zip(polygon_meters[0], polygon_meters[1])))
    # centroid_x=  polygon.centroid.x
    # centroid_y = polygon.centroid.y 
    # print(polygon.centroid)
    # print(polygon.centroid.x)
    # xs = [x - centroid_x + center[0] for x in polygon_meters[0]]
    # ys = [y - centroid_y + center[1] for y in polygon_meters[1]]
    
    xs = [x - float(polygon.centroid.x)  for x in polygon_meters[0]]
    ys = [y - float(polygon.centroid.y)   for y in polygon_meters[1]]
    polygon_meters_shapely = Polygon(list(zip(xs, ys)))
    return polygon_meters_shapely

def resize_polygon(site, multiplier=False, desired_scale=1, center=None):
    X, Y = site.exterior.xy
    current_width = max(X) - min(X)
    current_height = max(Y) - min(Y)
    longest_axis = max(current_width, current_height)
    scale_factor = desired_scale / longest_axis

    if not center:
        center_x = current_width / 2
        center_y = current_height / 2

    else:
        center_x, center_y = center

    if multiplier: 
        scale_factor = multiplier

    scaled_polygon_x = [(x - min(X)) * scale_factor for x in X]
    scaled_polygon_y = [(y - min(Y)) * scale_factor for y in Y]
      
    scaled_polygon = Polygon(list(zip(scaled_polygon_x,scaled_polygon_y)))

    x_off = scaled_polygon.centroid.x - center_x
    y_off = scaled_polygon.centroid.y - center_y
    centered_polygon_x = [x - x_off for x in scaled_polygon_x]
    centered_polygon_y = [y - y_off for y in scaled_polygon_y]
    
    scaled_polygon = Polygon(list(zip(centered_polygon_x,centered_polygon_y)))

    return scaled_polygon
    # return centered_polygon_x,centered_polygon_y

def polygon_to_Poly3DCollection(polygon, height, config={"facecolors":"cyan", "linewidths":1, "edgecolors":"r", "alpha":0.5}): 
    """
    Returns a Poly3DCollection object for a given polygon and height
    input: 
        polygon: shapely.geometry.Polygon
        height: int 
        config: dict (Optional) 
    output:
        A 3D Poly3DCollection object representing the input polygon extruded to the specified height: mpl_toolkits.mplot3d.art3d.Poly3DCollection
    """
    polygon_coords_2d = polygon.exterior.xy
    polygon_coords_2d = list(zip(polygon_coords_2d[0], polygon_coords_2d[1]))            
    polygon_coords_3d = [(x, y, 0) for x, y in polygon_coords_2d]  # Bottom face
    polygon_coords_3d_top = [(x, y, height) for x, y in polygon_coords_2d]  # Top face
    verts = [polygon_coords_3d, polygon_coords_3d_top]
    poly3d = [[verts[0][i], verts[0][i + 1], verts[1][i + 1], verts[1][i]] for i in range(len(verts[0]) - 1)]
    return Poly3DCollection(poly3d, **config)

