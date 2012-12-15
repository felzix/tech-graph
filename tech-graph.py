#!/usr/bin/python

from lib import ModPack, Mod
from lib import EdgeUsedToObtain, EdgeCreatedWith, EdgeManufacturedWith
from lib import EdgeObtainedByDrop, EdgeProducedOrFoundBy, EdgeFuelsOrPowers

#TODO replace with file interpreting and/or loading

mod = Mod("Vanilla")

mod.entity("leather", "resources/vanilla/leather.png")

mod.draw()

