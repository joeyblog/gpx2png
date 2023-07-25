import requests
import gpxpy
from utils import *
from geopy.geocoders import Nominatim

#made my own class just because it is easier to manage the data I needed
class GPX:
    coordinates = []
    lats = []
    lons = []

    def load_from_filepath(self, gpx_filepath):
        print("Loading GPX file...")
        with open(gpx_filepath, 'r') as gpx_file:
            self.parse_gpx(gpx_file.read())

    def load_from_url(self, url):
        print("Downloading: " + url)
        try:
            response = requests.get(url)
            response.raise_for_status()
            print("Download completed")
            self.parse_gpx(response.content)
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")

    def parse_gpx(self, data):
        self.coordinates = []
        self.lats = []
        self.lons = []
        gpx = gpxpy.parse(xml_or_file=data)
        cnt_tp = 0
        cnt_wp = 0
        cnt_rp = 0
        for track in gpx.tracks:
            for segment in track.segments:
                for point in segment.points:
                    cnt_tp += 1
                    lat = float(point.latitude)
                    lon = float(point.longitude)
                    data = (lat,lon)
                    #print(data)
                    self.coordinates.append(data)
                    self.lats.append(lat)
                    self.lons.append(lon)

        for waypoint in gpx.waypoints:
            cnt_wp += 1
            lat = float(waypoint.latitude)
            lon = float(waypoint.longitude)
            data = (lat,lon)
            #print(data)
            self.coordinates.append(data)
            self.lats.append(lat)
            self.lons.append(lon)

        for route in gpx.routes:
            for point in route.points:
                cnt_rp += 1
                lat = float(point.latitude)
                lon = float(point.longitude)
                data = (lat,lon)
                #print(data)
                self.coordinates.append(data)
                self.lats.append(lat)
                self.lons.append(lon)
        print(str(cnt_tp)+' Points from tracks')
        print(str(cnt_wp)+' Waypoints')
        print(str(cnt_rp)+' Points from routes')
    
    def get_coordinates(self):
        return self.coordinates

    def get_min_point(self):
        lat_min = min(self.lats)
        lon_min = min(self.lons)
        return lat_min, lon_min
    
    def get_max_point(self):
        lat_max= max(self.lats)
        lon_max = max(self.lons)
        return lat_max, lon_max
    
    def get_total_distance(self):
        return total_distance(self.coordinates)

    def getLocationInfo(self):
        geolocator = Nominatim(user_agent="geoapiExercises")
        location = geolocator.reverse(str(self.lats[0])+","+str(self.lons[0]))
        address = location.raw['address']

        # traverse the data
        data = {
            "city" : address.get('city', ''),
            "flag": get_country_flag(address.get('country_code'))
        }
        return data
