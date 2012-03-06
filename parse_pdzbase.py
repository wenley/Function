
import os
import sys
from optparse import OptionParser

usage = "usage: %prog [options]"
parser = OptionParser(usage, version = "%prog dev-unreleased")
parser.add_option('-o', "--organism", dest = 'org', help = "organism to parse", metavar = "string")
parser.add_option('-p', "--output-prefix", dest = 'opref', help = "directory for output files", metavar = "string")
parser.add_option('-i', "--id-file", dest = 'idfile', help = "file to map gene-ids to desired identifiers in the format <id from raw>\\t<desired id>\\n", metavar = "FILE")
parser.add_option('-f', "--intput-file", dest = 'input', help = "file to read", metavar = "FILE")
parser.add_option('-t', "--header", dest = 'header', help = "is there a header?", action = "store_true")

(options, args) = parser.parse_args()

id_name = None
if options.idfile is not None:
    id_name = {}
    with open(options.idfile) as idfile:
        for line in idfile:
            linelist = line.strip().split()
            id_name[linelist[0]] = linelist[1]

with open(options.input) as f:
    if options.header:
        f.readline() #pass header
    for line in f:
        linelist = line.strip().split('\t')
        if not linelist[5] == options.org:
            continue
        prota = linelist[1]
        protb = linelist[4]
        pubid = linelist[6]
        if id_name is not None:
            try:
                prota = id_name[prota]
                protb = id_name[protb]
            except KeyError:
                continue
        with open(options.opref + '.dat', 'a+') as out_f:
            out_f.write('\t'.join((prota, protb, '1', pubid)) + '\n')
