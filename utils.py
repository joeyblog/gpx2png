import math
import emoji

#calculate the tile numbeers from coords
#https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames
def deg2num(lat_deg, lon_deg, zoom):
  lat_rad = math.radians(lat_deg)
  n = 1 << zoom
  xtile = int((lon_deg + 180.0) / 360.0 * n)
  ytile = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
  return xtile, ytile

#calculate the corner loctaions from tile numbers
def tile_corners_to_latlon(zoom, xtile, ytile):
    n = 2.0 ** zoom
    lon_deg = xtile / n * 360.0 - 180.0
    lat_rad_nw = math.atan(math.sinh(math.pi * (1 - 2 * (ytile / n))))
    lat_deg_nw = math.degrees(lat_rad_nw)

    lat_rad_se = math.atan(math.sinh(math.pi * (1 - 2 * ((ytile + 1) / n))))
    lat_deg_se = math.degrees(lat_rad_se)

    lat_deg_nw = max(min(lat_deg_nw, 85.0511), -85.0511)
    lat_deg_se = max(min(lat_deg_se, 85.0511), -85.0511)

    top_left = (lat_deg_nw, lon_deg)
    #top_right = (lat_deg_nw, lon_deg + (360.0 / n))
    bottom_right = (lat_deg_se, lon_deg + (360.0 / n))
    #bottom_left = (lat_deg_se, lon_deg)

    #I just need top_left and bottom_right
    #return top_left, top_right, bottom_left, bottom_right
    return top_left, bottom_right

EARTH_RADIUS = 6371000

def haversine_distance(lat1, lon1, lat2, lon2):
    #convert to rad
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    d_lat = lat2_rad - lat1_rad
    d_lon = lon2_rad - lon1_rad
    a = math.sin(d_lat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(d_lon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = EARTH_RADIUS * c

    return distance

#calculate the total distance in meters
def total_distance(coords):
    total_distance = 0
    for i in range(len(coords) - 1):
        lat1, lon1 = coords[i]
        lat2, lon2 = coords[i + 1]
        total_distance += haversine_distance(lat1, lon1, lat2, lon2)
    return total_distance


#assuming that the walking speed is 10km/h (works good for hatching eggs)
#calculation might be slightly off in some locations
def convert_to_time(length_in_meters):
    walking_speed = 10 #km/h

    speed_m_per_sec = walking_speed * 1000 / 3600

    time_in_seconds = length_in_meters / speed_m_per_sec

    hours = int(time_in_seconds // 3600)
    minutes = int((time_in_seconds % 3600) // 60)
    seconds = int(time_in_seconds % 60)

    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    else:
        return f"{minutes:02d}:{seconds:02d}"


def calculate_rectangle_dimensions(min_lat, min_lon, max_lat, max_lon):
    width = haversine_distance(min_lat, min_lon, min_lat, max_lon)
    height = haversine_distance(min_lat, min_lon, max_lat, min_lon)

    return width, height

#calculate a new coord with offsets in meters
def add_meters_to_coordinate(lat, lon, meter_x, meter_y):
    lat_per_meter = 1 / (EARTH_RADIUS * math.pi / 180)
    lon_per_meter = 1 / (EARTH_RADIUS * math.pi / 180 * math.cos(math.radians(lat)))

    delta_lat = meter_y * lat_per_meter
    delta_lon = meter_x * lon_per_meter

    new_lat = lat + delta_lat
    new_lon = lon + delta_lon

    return new_lat, new_lon

# get emoji for country flag just because it looks nicer with it
def get_country_flag(country_code):
    try:        
        flag = emoji.emojize(f":flag_{country_code}:")
        return flag
    except emoji.EmojiNotFoundError:
        return ""