import json

# imports added in Lab3 version
from math import cos, sqrt, pi
import os
from .graphs import WeightedGraph
from django.conf import settings


# path changed from Lab2 version
# TODO: copy your json file from Lab 1 here - DONE
TRAM_FILE = os.path.join(settings.BASE_DIR, 'static/tramnetwork.json')


class TramNetwork(WeightedGraph):
    def __init__(self, lines, stops, times):
        super().__init__(stops)
        self._linedict = lines
        self._stopdict = stops
        self._timedict = times

        for stop_name in self._stopdict.keys():
            WeightedGraph.add_vertex(self, stop_name)

        for tram_line, stops in self._linedict.items():
            for i in range(len(stops) - 1):
                stop1 = stops[i]
                stop2 = stops[i+1]
                WeightedGraph.add_edge(self, stop1, stop2)

    def all_lines(self):
        return self._linedict.keys()

    def all_stops(self):
        return self._stopdict.keys()

    def extreme_positions(self):
        # this returns just the coordinates, but it will be another for lines to
        # find corresponding stops
        lat = [location['lat'] for location in self._stopdict.values()]
        lon = [location['lon'] for location in self._stopdict.values()]
        min_lat = min(lat)
        min_lon = min(lon)
        max_lat = max(lat)
        max_lon = max(lon)
        return min_lat, min_lon, max_lat, max_lon

    def geo_distansce(self, a, b):
        r = 6371.0   # Radius of Earth km
        lat_1 = self._stopdict[a]['lat'] * pi/180
        lon_1 = self._stopdict[a]['lon'] * pi/180
        lat_2 = self._stopdict[b]['lat'] * pi/180
        lon_2 = self._stopdict[b]['lon'] * pi/180
        dlat = lat_2 - lat_1
        dlon = lon_2 - lon_1
        meanlat = (lat_1 + lat_2) / 2
        
        distance = r* sqrt(dlat **2 + (cos(meanlat) * dlon) **2 )
        
        return distance
    
    def line_stops(self, line):
        return self._linedict.get(line, [])

    def stop_lines(self, a):
        lines_v_stops = []
        for key, value in self._linedict.items():
            for station in value:
                if station == a:
                    lines_v_stops.append(key)

        sorted_lines = sorted(lines_v_stops, key=lambda x: int(x))
        return sorted_lines
    
    
    def stop_position(self, a):
        return self._stopdict[a]

    def transition_time(self, line, a, b):
        time = 0
        if a and b in self._linedict[line]:
            stops_on_line = self._linedict[line]
            start_index = stops_on_line.index(a)
            end_index = stops_on_line.index(b)
            if start_index == end_index:
                return time

            elif start_index < end_index:
                stops_between_values = stops_on_line[start_index: end_index + 1]
            else:
                stops_between_values = stops_on_line[end_index: start_index + 1]

            for indx in range(len(stops_between_values) - 1):
                if stops_between_values[indx] in self._timedict and stops_between_values[indx + 1] in self._timedict[stops_between_values[indx]]:

                    time += self._timedict[stops_between_values[indx]
                                           ][stops_between_values[indx + 1]]
                else:
                    time += self._timedict[stops_between_values[indx + 1]
                                           ][stops_between_values[indx]]
            return time

        else:
            False

    def lines_between_stops(self, stop1, stop2):
        lines_btw_stops = []
        for key in self._linedict.keys():
            if stop1 in self._linedict[key] and stop2 in self._linedict[key]:
                lines_btw_stops.append(key)

        sorted_stops = sorted(lines_btw_stops, key=lambda x: int(x))
        return sorted_stops

    def travel_time(self, a, b):

        time = 0
        common_line = self.lines_between_stops(a, b)[0]
        stops_on_line = self._linedict[common_line]
        start_index = stops_on_line.index(a)
        end_index = stops_on_line.index(b)
        if start_index == end_index:
            return time

        elif start_index < end_index:
            stops_between_values = stops_on_line[start_index: end_index + 1]
        else:
            stops_between_values = stops_on_line[end_index: start_index + 1]

        for indx in range(len(stops_between_values) - 1):
            if stops_between_values[indx] in self._timedict and stops_between_values[indx + 1] in self._timedict[stops_between_values[indx]]:

                time += self._timedict[stops_between_values[indx]
                                       ][stops_between_values[indx + 1]]
            else:
                time += self._timedict[stops_between_values[indx + 1]
                                       ][stops_between_values[indx]]
        return time

    
    
def readTramNetwork(tramfile=TRAM_FILE):
    with open(tramfile, 'r') as file:
        Network = json.load(file)
    return TramNetwork(Network["lines"], Network['stops'], Network['times'])










# Bonus task 1: take changes into account and show used tram lines

def specialize_stops_to_lines(network):
    # TODO: write this function as specified
    return network


def specialized_transition_time(spec_network, a, b, changetime=10):
    # TODO: write this function as specified
    return changetime


def specialized_geo_distance(spec_network, a, b, changedistance=0.02):
    # TODO: write this function as specified
    return changedistance

