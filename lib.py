import networkx as nx

#import pygraphviz as viz

#XXX might need to be MultiDiGraph
GRAPH_CLASS = nx.DiGraph

class ModPack:
    """Note that later mods' images replace earlier mods' images"""
    def __init__(self, name, mods=[]):
        self.graph = GRAPH_CLASS()
        self.mods = mods
        for mod in mods:
            nx.compose(self.graph, mod.graph)

    def mod(self, mod):
        self.mods.append(mod)
        nx.compose(self.graph, mod.graph)

    def draw(selfi, outfile):
        graph = nx.to_agraph(self.graph)
        graph.draw(outfile, "png")

class Mod:
    def __init__(self, name, image=None):
        self.graph = GRAPH_CLASS(name=name, image=image)

    def node(self, name, image):
        self.graph.add_node(name, image=image)

    def edge(self, edge, source, destination):
        self.graph.add_edge(source, destination, type=edge)

    def draw(self):
        graph = nx.to_agraph(self.graph)
        graph.draw(outfile, "png")

class Entity:
    def __init__(self, name):
        # name and image can be a lists for grouped entities.
        # Like logs and leaves.
        #XXX might not be implemented
        # name is used for uniqueness for composing mods into modpacks
        #TODO make sure this actually works
        self.name = name

    def draw(self):
        pass #TODO

    #TODO determine if this handles node uniqueness for composition
    def __str__(self):
        return self.name

    #TODO these can probably be removed
    def __eq__(self, other):
        return self.name == other.name

    def __ne__(self, other):
        return not self.__eq__(other)

class Edge:
    def draw(self):
        #XXX I'm not sure if pygraphviz can do custom edges
        #http://networkx.lanl.gov/reference/drawing.html
        pass #TODO

    def __eq__(self, other):
        return self.name == other.name

    def __ne__(self, other):
        return not self.__eq__(other)

class EdgeUsedToObtain(Edge):
    name = "Used to obtain"
    color = "blue"

class EdgeCreatedWith(Edge):
    name = "Created with"
    color = "purple"

class EdgeManufacturedWith(Edge):
    name = "Manufactured with"
    color = None

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
