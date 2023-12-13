import graphviz as gv



class Graph():
    def __init__(self, start=None, values=None, directed=False):
        # ATTRIBUTES
        # A dictionary to store the adjacency list representation of the grap
        self._adjlist = {}
        self._adjlist_pairs = {}
        self._combined = {}
        if values is None:
            values = {}
        # A dictionary to store values associated with each vertex.
        self._valuelist = values
        # A boolean indicating whether the graph is directed or not.
        self._isdirected = directed

    # METHODS
    def vertices(self):
        return list(self._adjlist.keys())

    def edges(self):
        edges = set()
        for vertex, neighbors in self._adjlist.items():
            for neighbor in neighbors:
                edges.add((vertex, neighbor))
        return edges

    def neighbors(self, v):
        return self._adjlist.get(v, set())

    def add_edge(self, a, b):
        self.add_vertex(a)
        self.add_vertex(b)
        # The use of set() ensures that we have sets to store the neighbors of both vertex1 and vertex2
        self._adjlist.setdefault(a, set()).add(b)
        # Undirected graph so both ways should be considered
        self._adjlist.setdefault(b, set()).add(a)

    def add_vertex(self, a):
        self._adjlist.setdefault(a, set())

    def is_directed(self):
        return self.is_directed

    def get_vertex_value(self, v):
        return self._valuelist.get(v, None)

    def set_vertex_value(self, v, x):
        self._valuelist[v] = x

    def __len__(self):
        return len(self._adjlist)

    def remove_edge(self, u, v):
        if u in self._adjlist and v in self._adjlist[u]:
            self._adjlist[u].remove(v)
        if not self._isdirected and v in self._adjlist and u in self._adjlist[v]:
            self._adjlist[v].remove(u)

    def remove_vertices(self, n):
        if n in self._adjlist:
            del self._adjlist[n]
            for vertex, neighbors in self._adjlist.items():
                if n in neighbors:
                    neighbors.remove(n)

    def adj_list(self):
        return self._adjlist
    # BONUS PART 1

    def vertices_pairs(self):
        return list(self._adjlist_pairs.keys())

    def edges_pairs(self):
        edges = set()
        for vertex, neighbors in self._adjlist_pairs.items():
            for neighbor in neighbors:
                edges.add((vertex, neighbor))
        return edges

    def add_vertex_pairs(self, stop, line):
        self._adjlist_pairs[(stop, line)] = set()

    def add_edge_pairs(self, stop1, stop2):
        # self.add_vertex_pairs(stop1, line)
        # self.add_vertex_pairs(stop2, line)
        # self._adjlist_pairs.setdefault((stop1), set()).add((stop2))
        # self._adjlist_pairs.setdefault((stop2), set()).add((stop1))\
        self._adjlist_pairs.setdefault(
            (stop1[0], stop1[1]), set()).add((stop2[0], stop2[1]))
        self._adjlist_pairs.setdefault(
            (stop2[0], stop2[1]), set()).add((stop1[0], stop1[1]))
        # print(self.edges_pairs())

        # self.add_vertex(a)
        # self.add_vertex(b)
        # # The use of set() ensures that we have sets to store the neighbors of both vertex1 and vertex2
        # self._adjlist.setdefault(a, set()).add(b)
        # # Undirected graph so both ways should be considered
        # self._adjlist.setdefault(b, set()).add(a)

    def neighbors_pairs(self, v):
        return self._adjlist_pairs.get(v, set())

        # BONUS PART 1
    def vertices_pairs(self):
        return list(self._adjlist_pairs.keys())

    def edges_pairs(self):
        edges = set()
        for vertex, neighbors in self._adjlist_pairs.items():
            for neighbor in neighbors:
                edges.add((vertex, neighbor))
        return edges

    def add_vertex_pairs(self, stop, line):
        self._adjlist_pairs[(stop, line)] = set()

    def add_edge_pairs(self, stop1, stop2):
        self._adjlist_pairs.setdefault(
            (stop1[0], stop1[1]), set()).add((stop2[0], stop2[1]))
        self._adjlist_pairs.setdefault(
            (stop2[0], stop2[1]), set()).add((stop1[0], stop1[1]))
        # print(self.edges_pairs())

    def connect_edges(self, node, neighbor):
        self._adjlist_pairs.setdefault(node, set()).add(neighbor)

    def neighbors_pairs(self, v):
        return self._adjlist_pairs.get(v, set())


class WeightedGraph(Graph):
    def __init__(self, start=None):
        super().__init__(start)
        self._weightlist = {}
        self.edge_list = Graph.edges(self)
        # creating an empty weight list
        for edge in self.edge_list:
            self._weightlist[edge] = {}
            for stop in self.edge_list[edge]:
                temp = {stop: 'none'}
                self._weightlist[edge].update(temp)

    def set_weight(self, a, b, w):
        # Check if a and b have the same stop (transfer between lines)
        if a[0] == b[0]:
            self._weightlist.setdefault(a, {}).setdefault(b, w)
        else:
            # Handle transfer time and distance for different lines
            change_distance = 0.02
            change_time = 10

            # Check if a and b have the same line
            if a[1] == b[1]:
                self._weightlist.setdefault(a, {}).setdefault(b, w)
            else:
                # Different lines - set transfer time and distance
                self._weightlist.setdefault(
                    a, {}).setdefault(b, change_distance)
                self._weightlist.setdefault(
                    b, {}).setdefault(a, change_distance)
                self._weightlist.setdefault(a, {}).setdefault(b, change_time)
                self._weightlist.setdefault(b, {}).setdefault(a, change_time)

    def get_weight(self, a, b):
        return self._weightlist[a][b]

    def weights_all(self):
        return self._weightlist


def dijkstra(graph, source, cost=lambda u, v, g: 1):

    vertices = graph.vertices_pairs()
    dist = {v: float('inf') for v in vertices}
    prev = {v: None for v in vertices}
    paths = {v: [] for v in vertices}

    for i in dist:
        if i[0] == source:
            dist[i] = 0
            # break
    unexplored = set(vertices)

    while unexplored:
        current_vertex = min(unexplored, key=lambda v: dist[v])
        unexplored.remove(current_vertex)

        change_distance = 0
        change_time = 10

        neighbors = graph.neighbors_pairs(current_vertex)
        for neighbor in neighbors:
            # Maybe add an if statment if the cost was dist/time
            weight = cost(current_vertex[0], neighbor[0])
            if weight != 0:
                if dist[current_vertex] + weight < dist[neighbor]:
                    if neighbor in dist:
                        dist[neighbor] = dist[current_vertex] + weight
                        prev[neighbor] = current_vertex
                        paths[neighbor] = paths[current_vertex] + [neighbor]
            else:
                # Maybe create a seperate dijkstra function for time
                weight = 0
                # weight = change_time
                if (dist[current_vertex]) + weight < dist[neighbor]:
                    if neighbor in dist:
                        dist[neighbor] = dist[current_vertex] + weight
                        prev[neighbor] = current_vertex
                        paths[neighbor] = paths[current_vertex] + [neighbor]

    return dist, paths


def visualize(graph, view='dot', name='mygraph.gv', nodecolors={}, engine='dot'):
    dot = gv.Graph(engine)
    edge_list = graph.edges()

    for edge in edge_list:
        source, target = edge  # Unpack the edge tuple
        edge_to_color = list(nodecolors.keys())
        dot.node(str(source))
        dot.node(str(target))

        if str(source) in edge_to_color and str(target) in edge_to_color:
            dot.edge(str(source), str(target), color="orange")
        else:
            dot.edge(str(source), str(target))

    for node, col in nodecolors.items():
        dot.node(str(node), fillcolor=col, style='filled')

    dot.render(name, view, format='png')


#def view_shortest(G, source, target, cost=TramNetwork.geo_distansce):
def view_shortest(G, source, target, cost=lambda u, v: 1):
    distance, path = dijkstra(G, source, cost=lambda u, v, graph: cost(u, v, graph))
    path_target = path[target]
    colormap = {str(v): 'orange' for v in path_target}
    src = {str(source): "red"}
    trg = {str(target): "yellow"}
    colormap.update(src)
    colormap.update(trg)
    visualize(G, view='view', nodecolors=colormap)


