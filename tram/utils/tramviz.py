# visualization of shortest path in Lab 3, modified to work with Django

from .trams import *
from .graphs import dijkstra
from .color_tram_svg import color_svg_network
import os
from django.conf import settings


def show_shortest(dep, dest, cost=lambda u, v: 1):
    network = readTramNetwork()

    distance, shortpath = dijkstra(
        network, dep, cost=network.specialized_geo_distance)
    
    min_distance = float('inf')
    shortest = None
    
    for i in shortpath:
        if i[0] == dest and distance[i] < min_distance:
            min_distance = distance[i]
            shortest = shortpath[i]      
    shortest = [item[0] for item in shortest]
    distacne_traveled = min_distance
 
    time, quickpath = dijkstra(network, dep, cost=network.specialized_transition_time)

    min_time = float('inf')
    quickest = None
    
    for i in quickpath:
        if i[0] == dest and time[i] < min_time:
            min_time = time[i]
            quickest = quickpath[i]

    quickest = [item[0] for item in quickest]
    travel_time = min_time
    
    timepath = 'Quickest: ' + dep + ', '+', '.join(quickest) + ' Time it took: ' + str(travel_time) + " min."
    
    geopath = 'Shortest: '+ dep + ', ' + ', '.join(shortest) + '. Distance traveled: ' "{:.3f}".format(distacne_traveled) +  ' km.'



    def colors(v):
        if v == dep:
            return 'red'
        elif v == dest:
            return 'yellow'
        elif v in shortest and v in quickest:
            return 'cyan'
        elif v in shortest:
            return 'limegreen'
        elif v in quickest:
            return 'orange'
        else:
            return 'white'
            

    # this part should be left as it is:
    # change the SVG image with your shortest path colors
    color_svg_network(colormap=colors)
    # return the path texts to be shown in the web page
    return timepath, geopath

