import math
import pvlib as pv


def distance_btwn_loc(loc_a: pv.location.Location, loc_b: pv.location.Location):
    return distance_btwn_lat_lon(loc_a.latitude, loc_a.longitude, loc_b.latitude, loc_b.longitude)


def distance_btwn_lat_lon(lat1,lon1,lat2,lon2):
    # Operates on assumption of spherical globe. Could be improved using spheroid.

    earth_r = 6371e3  # Radius of the earth in m
    d_lat = to_radians(lat2-lat1)
    d_lon = to_radians(lon2-lon1)
    a = math.sin(d_lat/2) * math.sin(d_lat/2) + math.cos(to_radians(lat1)) * math.cos(to_radians(lat2)) * math.sin(d_lon/2) * math.sin(d_lon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = earth_r * c  # Distance in m
    return d


def to_radians(degrees: float):
    return degrees * (math.pi/180)
