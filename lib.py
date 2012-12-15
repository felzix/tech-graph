import networkx as nx

#import pygraphviz as viz

#XXX might need to be MultiDiGraph
GRAPH_CLASS = nx.DiGraph
LAYOUT      = "dot"
SHAPE       = "square"

class AbstractGraph:

    def __init__(self, name):
        self.graph = GRAPH_CLASS(name=name)

    def draw(self, outfile):
        graph = nx.to_agraph(self.graph, label=name)
        graph.draw(outfile, "png", prog=LAYOUT)

    def save(self, outfile):
        nx.write_dot(self.graph, outfile)

class ModPack(AbstractGraph):
    """Note that later mods' images replace earlier mods' images"""

    def __init__(self, name, mods=[]):
        AbstractGraph.__init__(self, name)
        self.mods = mods
        for mod in mods:
            nx.compose(self.graph, mod.graph, name=name)

    def mod(self, mod):
        self.mods.append(mod)
        nx.compose(self.graph, mod.graph, name=self.graph.name)

class Mod(AbstractGraph):

    def __init__(self, name):
        AbstractGraph.__init__(self, name)

    def node(self, name, image):
        self.graph.add_node(name, image=image, shape=SHAPE, ratio=1, label="")

    def edge(self, edge, source, destination):
        color = edge.color
        label = str(edge)
        if label:
            self.graph.add_edge(source, destination, color=color, label=label)
        else:
            self.graph.add_edge(source, destination, color=color)

    def draw(self, outfile):
        graph = nx.to_agraph(self.graph)
        graph.draw(outfile, "png", prog=LAYOUT)

    def save(self, outfile):
        nx.write_dot(self.graph, outfile)

class Edge:

    def __str__(self):
        return ""

class EdgeUsedToObtain(Edge):

    name = "Used to obtain"
    color = "blue"

class EdgeCreatedWith(Edge):

    name = "Created with"
    color = "purple"

class EdgeManufacturedWith(Edge):

    name = "Manufactured with"
    color = "black"

    def __init__(self, quantity=1):
        self.quantity = quantity

    def __str__(self):
        return str(self.quantity)

class EdgeObtainedByDrop(Edge):

    name = "Obtained by drop"
    color = "red"

class EdgeProducedOrFoundBy(Edge):

    name = "Produced by / Found by"
    color = "yellow"

class EdgeFuelsOrPowers(Edge):

    name = "Fuels or Powers"
    color = "green"

    def __init__(self, magnitude, unit=None):
        self.magnitude = magnitude
        # e.g. item, EU, EU/t, MJ
        self.unit = unit

    def __str__(self):
        return str(self.magnitude) + " " + self.unit

