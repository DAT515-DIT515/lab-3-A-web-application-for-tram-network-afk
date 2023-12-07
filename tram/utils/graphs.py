import graphviz as gv



class Graph():
    def __init__(self, start=None, values=None, directed=False):
        # ATTRIBUTES
        # A dictionary to store the adjacency list representation of the grap
        self._adjlist = {}
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
        self._weightlist[a][b] = w

    def get_weight(self, a, b):
        return self._weightlist[a][b]

    def weights_all(self):
        return self._weightlist


def dijkstra(graph, source, cost=lambda u, v, g: 1):
    vertices = graph.vertices()
    dist = {v: float('inf') for v in vertices}
    prev = {v: None for v in vertices}
    paths = {v: [] for v in vertices}

    dist[source] = 0
    unexplored = set(vertices)

    while unexplored:
        current_vertex = min(unexplored, key=lambda v: dist[v])
        unexplored.remove(current_vertex)

        neighbors = graph.neighbors(current_vertex)
        for neighbor in neighbors:
            weight = cost(current_vertex, neighbor)
            if dist[current_vertex] + weight < dist[neighbor]:
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


