#!/usr/bin/env python3

class GeoPoint:
    def __init__(self, lat=0, lon=0):
        self._latitude = lat
        self._longitude = lon

    def latitude(self):
        return self._latitude

    def longitude(self):
        return self._longitude

    def get(self):
        return self._latitude, self._longitude

    def from_tuple(self, tup):
        gp = GeoPoint(tup[0], tup[1])
        return gp

    def min(self, points):
        min_lat = points[0].latitude()
        min_lon = points[0].longitude()
        for i in range(1, len(points)):
            if points[i].latitude() < min_lat:
                min_lat = points[i].latitude()
            if points[i].longitude() < min_lon:
                min_lon = points[i].longitude()
        return GeoPoint(min_lat, min_lon)

    def max(self, points):
        max_lat = points[0].latitude()
        max_lon = points[0].longitude()
        for i in range(1, len(points)):
            if points[i].latitude() > max_lat:
                max_lat = points[i].latitude()
            if points[i].longitude() > max_lon:
                max_lon = points[i].longitude()
        return GeoPoint(max_lat, max_lon)

    def __str__(self):
        return f'[{self._latitude},{self._longitude}]'
