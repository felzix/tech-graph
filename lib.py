import networkx as nx

#import pygraphviz as viz

#XXX might need to be MultiDiGraph
GRAPH_CLASS = nx.DiGraph
LAYOUT      = "dot"
SHAPE       = "square"

class ModPack:
    """Note that later mods' images replace earlier mods' images"""
    def __init__(self, name, mods=[]):
        self.graph = GRAPH_CLASS(name=name)
        self.mods = mods
        for mod in mods:
            nx.compose(self.graph, mod.graph, name=name)

    def mod(self, mod):
        self.mods.append(mod)
        nx.compose(self.graph, mod.graph, name=self.graph.name)

    def draw(self, outfile):
        graph = nx.to_agraph(self.graph, label=name)
        graph.draw(outfile, "png", prog=LAYOUT)

class Mod:
    def __init__(self, name, image=None):
        self.graph = GRAPH_CLASS(name=name, image=image)

    def node(self, name, image):
        self.graph.add_node(name, image=image, shape=SHAPE, ratio=1, label="")

    def edge(self, edge, source, destination):
        color = edge.color
        label = None
        if isinstance(edge, EdgeManufacturedWith):
            label = str(edge.quantity)
        if isinstance(edge, EdgeFuelsOrPowers):
            label = str(edge.quantity) + " " + edge.unit
        if label:
            self.graph.add_edge(source, destination, color=color, label=label)
        else:
            self.graph.add_edge(source, destination, color=color)

    def draw(self, outfile):
        graph = nx.to_agraph(self.graph)
        graph.draw(outfile, "png", prog=LAYOUT)

class Edge:
    pass

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

class EdgeObtainedByDrop(Edge):
    name = "Obtained by drop"
    color = "red"

class EdgeProducedOrFoundBy(Edge):
    name = "Produced by / Found by"
    color = "yellow"

class EdgeFuelsOrPowers(Edge):
    name = "Fuels or Powers"
    color = "green"

    def __init__(self, quantity, unit=None):
        self.quantity = quantity
        # e.g. item, EU, EU/t, MJ
        self.unit = unit

