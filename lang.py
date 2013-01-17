__author__ = 'ngozi'

from pyparsing import Word, Literal, LineStart, LineEnd, OneOrMore, Group, Dict, Suppress, alphas, nums, alphanums, printables
import lib

DELIM = ','
EDGES = {'used': lib.EdgeUsedToObtain,
         'prod': lib.EdgeProducedOrFoundBy,
         'drop': lib.EdgeObtainedByDrop,
         'created': lib.EdgeCreatedWith,
         'fuel': lib.EdgeFuelsOrPowers,
         'mfg': lib.EdgeManufacturedWith}
BASIC_EDGES = ['used', 'prod', 'drop', 'created']
NONBASIC_EDGES = ['fuel', 'mfg']

class Lang:
    def read(self, file):
        modname = LineStart() + Suppress('{') + Word(alphas, alphanums) + Suppress('}') + Suppress(LineEnd())
        entity = Word(alphas, alphanums + '_')
        magnitude = Word(nums)
        unit = Word(printables)
        basic_relation = self.__relations_basic()
        delim = Suppress(DELIM)
        comment = Suppress(LineStart() + '#' + Word(printables + ' ' + '\t') + LineEnd())

        basic_edge = entity + delim + entity + delim + basic_relation
        fuel_edge = entity + delim + entity + delim + magnitude + delim + unit
        mfg_edge = entity + delim + entity + delim + magnitude

        mfg_edge.addParseAction(self.__actMfgEdge)
        fuel_edge.addParseAction(self.__actFuelEdge)

        relationship = LineStart() + (mfg_edge ^ fuel_edge ^ basic_edge ^ entity) + Suppress(LineEnd())
        relationship = Group(relationship)
        mod = Group(modname + Group(OneOrMore(comment ^ relationship)))
        modpack = Dict(OneOrMore(mod))

        parsed = modpack.parseFile(file)

        interpreted = self.__interpret_modpack(parsed)

        return interpreted

    def __relations_basic(self):
        ss = EDGES.keys()
        ss = [x for x in ss if x in BASIC_EDGES]
        o = Literal(ss.pop())

        for s in ss:
            o ^= Literal(s)

        return o

    def __actFuelEdge(self, s, loc, toks):
        return toks.insert(len(toks), 'fuel')
        #return toks + Literal( 'fuel' )

    def __actMfgEdge(self, s, loc, toks):
        return toks.insert(len(toks), 'mfg')

    def __interpret_modpack(self, mods):
        """Modifies argument."""
        for mod, rels in mods.items():
            for rel in rels:
                if len(rel) == 1: # single entity
                    pass
                elif len(rel) == 3: # basic relationship
                    rel[2] = EDGES[rel[2]]()
                elif len(rel) == 4: # mfg relationship
                    quantity = rel[2]
                    rel[2] = lib.EdgeManufacturedWith(quantity)
                    del rel[3:]
                elif len(rel) == 5: # fuel relationship
                    magnitude = rel[2]
                    unit = rel[3]
                    rel[2] = lib.EdgeFuelsOrPowers(magnitude, unit)
                    del rel[3:]
        return mods
