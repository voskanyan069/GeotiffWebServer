#!/usr/bin/env python3

import math

class GeoFile:
    def __init__(self, path='./'):
        self.path = path

    def filename(self, point):
        lat = point.latitude()
        lon = point.longitude()
        vertical = 'N'
        horizontal = 'E'
        if (lat < 0):
            vertical = 'S'
        if (lon < 0):
            horizontal = 'W'
    
        return self.path + '%s%02.0f%s%03.0f.tif' % (vertical,
                math.floor(abs(lat)), horizontal, math.floor(abs(lon)))
