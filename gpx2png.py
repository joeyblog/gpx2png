from PIL import Image, ImageDraw
import requests
from xml.dom.minidom import parseString
from io import BytesIO
from utils import *
from gpx import GPX

#draw point with any size you like
def draw_point(draw, x, y, color, size):
    left_top = (x - size, y - size)
    right_bottom = (x + size, y + size)
    bounding_box = [left_top, right_bottom]
    draw.ellipse(bounding_box, fill=color)

def draw_lines(image, coordinates, left_top, right_bottom):
    print("Drawing the route...")
    draw = ImageDraw.Draw(image)

    width, height = image.size

    #calculate the best line width depending on the size of the image
    rate = max(width, height) / 256
    line_width_base = 1
    line_width = int(line_width_base * rate)
    print("line width: ", line_width)
    dot_size = line_width

    #colors in RGBA
    line_col = (26,133,255,255) #1A85FF
    point_col = (0,255,17,255) #00FF11
    point_outline_col = (255,255,255,255)
    point_start_col = (255,0,35,255)

    point_list = []
    for lat, lon in coordinates:
        # Calculate the pixel positions of the left-top and right-bottom coordinates
        left_top_lat, left_top_lon = left_top
        right_bottom_lat, right_bottom_lon = right_bottom

        # Calculate the latitude and longitude range of the image
        lat_range = left_top_lat - right_bottom_lat
        lon_range = right_bottom_lon - left_top_lon

        # Calculate the pixel position of the given coordinate
        x = int((lon - left_top_lon) / lon_range * width)
        y = int((left_top_lat - lat) / lat_range * height)
        point_list.append((x, y))
    
    draw.line(point_list, fill=line_col, width=line_width)
    for i, (x, y) in enumerate(point_list):
        if i == 0 or i == len(point_list) - 1:
            draw_point(draw, x, y, point_outline_col, dot_size)
            draw_point(draw, x, y, point_start_col, dot_size-1)
        else:
            draw_point(draw, x, y, point_outline_col, dot_size)
            draw_point(draw, x, y, point_col, dot_size-1)


def calc_min_max(points):
    lat_min = min(points['lat'])
    lon_min = min(points['lon'])
    lat_max= max(points['lat'])
    lon_max = max(points['lon'])
    return lat_min, lon_min, lat_max, lon_max

def convert(url):
    gpx = GPX()
    gpx.load_from_url(url)

    #gpx.load_from_filepath(url) #if you want to load a local file

    if(len(gpx.get_coordinates()) == 0):
        print("no point data found")
        return
    lat_min, lon_min = gpx.get_min_point()
    lat_max, lon_max = gpx.get_max_point()

    #calculate the rectangle size
    width, height = calculate_rectangle_dimensions(lat_min, lon_min, lat_max, lon_max)
    print("x: %dm, y: %dm" % (width, height))

    #distance of the longer side
    max_dist = max(width, height)

    #roughly decides the zoom depending on the distance
    zoom = 17
    if(max_dist > 1024):
        zoom = 16
    if(max_dist > 2048):
        zoom = 15
    if(max_dist > 4096):
        zoom = 14
    if(max_dist > 8192):
        zoom = 13
    print("Zoom: ", zoom)

    #add offset so it has some margin
    #prevent any point to be on the very edge of the picture
    #also try to make width and height as close as possible so it looks like a square
    offset = True
    if(offset):
        offset_x = 100 #meters
        if(height > width): 
            offset_x += int((height-width)/2) #adjust width to the length of height
        offset_y = 100 #meters
        if(width > height):
            offset_y += int((width-height)/2) #adjust height to the length of width

        lat_min, lon_min = add_meters_to_coordinate(lat_min, lon_min, -offset_x, -offset_y)
        lat_max, lon_max = add_meters_to_coordinate(lat_max, lon_max, offset_x, offset_y)

    delta_lat = lat_max- lat_min
    delta_long = lon_max- lon_min

    headers = {"User-Agent":"thisCanBeAnything"} #any UA is file

    smurl = r"https://tile.openstreetmap.org/{0}/{1}/{2}.png"
    xmin, ymax =deg2num(lat_min, lon_min, zoom)
    xmax, ymin =deg2num(lat_min + delta_lat, lon_min + delta_long, zoom)
    top_left = 0
    bottom_right = 0
    image = Image.new('RGB',((xmax-xmin+1)*256,(ymax-ymin+1)*256) ) 
    coordinates = []
    x_cnt = xmax+1 - xmin
    y_cnt = ymax+1 - ymin

    print(x_cnt*y_cnt) #number of tiles to be downloaded
    for xtile in range(xmin, xmax+1):
        for ytile in range(ymin,  ymax+1):
            try:
                imgurl = smurl.format(zoom, xtile, ytile)
                print("Downloading: " + imgurl)
                imgstr = requests.get(imgurl, headers=headers)
                tile = Image.open(BytesIO(imgstr.content))
                image.paste(tile, box = ((xtile-xmin)*256 ,  (ytile-ymin)*255))
                top_left, bottom_right = tile_corners_to_latlon(zoom, xtile, ytile)
                coordinates.append(top_left)
                coordinates.append(bottom_right)

            except: 
                print("Couldn't download image")
                tile = None
    
    min_lat, min_lon = coordinates[0]
    max_lat, max_lon = coordinates[0]

    # Find min/max latitude and longitude
    for lat, lon in coordinates:
        min_lat = min(min_lat, lat)
        min_lon = min(min_lon, lon)
        max_lat = max(max_lat, lat)
        max_lon = max(max_lon, lon)

    left_top = (max_lat, min_lon)
    right_bottom = (min_lat, max_lon)

    draw_lines(image, gpx.get_coordinates(), left_top, right_bottom)

    byte_io = BytesIO()
    image.save(byte_io, 'PNG')
    byte_io.seek(0)
    dist_m = gpx.get_total_distance()

    #get some more info
    result = {
        "data":byte_io,
        "total":dist_m,
        "walk": convert_to_time(dist_m),
        "location": gpx.getLocationInfo()
    }
    return result

    #save a png file locally
    #image.save(output_file_path, "PNG")
    #print("Overlay saved as:", output_file_path)
    
