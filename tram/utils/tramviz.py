# visualization of shortest path in Lab 3, modified to work with Django

from .trams import readTramNetwork
from .graphs import dijkstra
from .color_tram_svg import color_svg_network
import os
from django.conf import settings


def show_shortest(dep, dest, cost=lambda u, v: 1):
    # TODO: uncomment this when it works with your own code
    network = readTramNetwork()

    # TODO: replace this mock-up with actual computation using dijkstra.
    # First you need to calculate the shortest and quickest paths, by using appropriate
    # cost functions in dijkstra().
    # Then you just need to use the lists of stops returned by dijkstra()
    #
    # If you do Bonus 1, you could also tell which tram lines you use and where changes
    # happen. But since this was not mentioned in lab3.md, it is not compulsory.

    quickest = [dep, 'Varmfrontsgatan', 'Temperaturgatan', dest]
    
    #distance, path = dijkstra(network, dep, cost)
    
    #shortest = path[dest]
    shortest = [dep, 'Chalmers', 'Temperaturgatan', dest]
    
    timepath = 'Quickest: ' + ', '.join(quickest) + ', time it took'
    
    geopath = 'Shortest: ' + ', '.join(shortest) + ', distance traveled (i think thats what they want)'



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

