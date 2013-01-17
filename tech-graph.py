#!/usr/bin/python

from lib import  Mod
from lang import Lang
from sys import argv, exit

if len(argv) < 3:
    print "Must pass input TG (tech-graph) filename and png output filename."
    exit(1)

file = argv[1]
png = argv[2]

if png == 'dot':
    dot = True
    png = argv[3]

RESOURCE_DIR = "resources"

modpack = Lang().read(file)

for modname, rels in modpack.items():
    mod = Mod(modname)
    for rel in rels:
        src = rel[0]
        dest = rel[1]
        edge = rel[2]
        # mod.node() quietly ignores duplicates
        folder = RESOURCE_DIR + '/' + modname.lower()
        mod.node(src, folder + '/' + src + '.png')
        mod.node(dest, folder + '/' + dest + '.png')
        mod.edge(edge, src, dest)
    mod.draw(png)