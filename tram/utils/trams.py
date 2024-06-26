import json
from math import cos, sqrt, pi
import os
from .graphs import WeightedGraph
from django.conf import settings

TRAM_FILE = os.path.join(settings.BASE_DIR, 'static/tramnetwork.json')


class TramNetwork(WeightedGraph):
    def __init__(self, lines, stops, times):
        super().__init__()
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
        self.specialize_stops_to_lines()
        
    def all_lines(self):
        return self._linedict.keys()

    def all_stops(self):
        return self._stopdict.keys()

    def extreme_positions(self):
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

    def specialize_stops_to_lines(self):

        # BONUS 1
        # Create vertices for stops and lines
        for stop_name in self._stopdict.keys():
            for line in self._linedict.keys():
                if stop_name in self.line_stops(line):
                    self.add_vertex_pairs(stop_name, line)
                    stops = self._linedict[line]
                    for i in range(len(stops) - 1):
                        stop1 = stops[i]
                        stop2 = stops[i+1]
                        vertex1 = (stop1, line)
                        vertex2 = (stop2, line)
                        self.add_edge_pairs(vertex1, vertex2)
                    
        # Create edges between same stops
        for tram_line, stops in self._linedict.items():
            for i in range(len(stops) - 1):
                stop1 = (stops[i], tram_line)
                stop2 = (stops[i+1], tram_line)
                WeightedGraph.add_edge_pairs(self, stop1, stop2)
                # Create edges for stops and lines
                if i == 0:
                    # Connect first stop to itself for line transfer
                    self.add_edge_pairs(stop1, stop1)

        # Connect vertices with same stop and line
        for vertex_pair in self.vertices_pairs():
            for vertex in self.vertices():
                if vertex_pair[0] == vertex:
                    neighbors = self.neighbors(vertex)
                    for neighbor in neighbors:
                        for line in self._linedict.keys():
                            if vertex in self.line_stops(line) and neighbor in self.line_stops(line) and vertex_pair[1] == line:
                                neighbor_tuple = (neighbor, vertex_pair[1])
                                self.connect_edges(vertex_pair, neighbor_tuple)

        # Connect vertices with same stop but differnt lines
        for stop_name in self._stopdict.keys():
            lines_at_stop = [line for line in self._linedict.keys(
            ) if stop_name in self.line_stops(line)]
            for i in range(len(lines_at_stop)):
                for j in range(i + 1, len(lines_at_stop)):
                    line1 = lines_at_stop[i]
                    line2 = lines_at_stop[j]
                    vertex1 = (stop_name, line1)
                    vertex2 = (stop_name, line2)
                    self.add_edge_pairs(vertex1, vertex2)


    def specialized_transition_time(self, a, b, changetime=10):
        time = self.travel_time(a, b)
        if time == 0:
            return changetime
        else:
            return time

    def specialized_geo_distance(self, a, b, changedistance=0.02):
        distance = self.geo_distansce(a, b)
        if a == b:
                return changedistance
        else:
                return distance
    
def readTramNetwork(tramfile=TRAM_FILE):
    with open(tramfile, 'r') as file:
        Network = json.load(file)
    return TramNetwork(Network["lines"], Network['stops'], Network['times'])








