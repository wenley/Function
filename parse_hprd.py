
from optparse import OptionParser
import re
import sys
from idmap import idmap

usage = "usage: %prog [options]"
parser = OptionParser(usage, version = "%prog dev-unreleased")
parser.add_option("-f", "--hprd-file", dest = "hprd", help = "location of hprd file", metavar = "FILE")
parser.add_option("-o", "--output-prefix", dest = "opref", help = "prefix for output files", metavar = "string")
parser.add_option("-i", "--id-file", dest = "idfile", help = "file to map HGNC ids to the desired identifiers in the format <HGNC Symbol>\\t<desired id>\\n", metavar = "FILE")

(options, args) = parser.parse_args()

if options.hprd is None:
    sys.stderr.write("--hgnc-file is required.\n")
    sys.exit()
if options.opref is None:
    sys.stderr.write("--prefix is required.\n")
    sys.exit()

hprd_dat = open(options.opref + ".dat", "w")
hprd = open(options.hprd)

id_name = None
if options.idfile is not None:
    id_name = idmap(options.idfile)
#        id_name = {}
#        idfile = open(options.idfile)
#        for line in idfile:
#                linelist = line.strip().split()
#                id_name[linelist[0]] = linelist[1]

pub_set = set()

for line in hprd:
    toks = line.strip().split('\t')
    gene1 = toks[0]
    gene2 = toks[3]
    pubs = toks[7]
    for pub in pubs.split(','):
        pub_set.add(int(pub))

    if id_name is not None:
        gene_names1 = id_name.get(gene1)
        gene_names2 = id_name.get(gene2)
        if gene_names1 is None or gene_names2 is None:
            continue

        for g1 in gene_names1:
            for g2 in gene_names2:
                hprd_dat.write('\t'.join((g1, g2, '1', pubs)) + '\n')
    else:
        hprd_dat.write('\t'.join((gene1, gene2, '1', pubs)) + '\n')

print('\n'.join([str(x) for x in pub_set]))

try:
    quant_f = open(options.opref + ".quant", "w")
    quant_f.write('\t'.join(('0.5','1.5')))
finally:
    quant_f.close()
