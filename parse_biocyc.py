# TODO: optparse is deprecated i.f.o. argparse

from optparse import OptionParser
import re
import sys
import os
from idmap import idmap

usage = "usage: %prog [options]"
parser = OptionParser(usage, version = "%prog dev-unreleased")
parser.add_option("-b", "--biocyc-dir", dest="biocyc", help="location of biocyc files (required)", metavar="string")
parser.add_option("-s", "--organism", dest="org", help="Uniprot organism code (required)", metavar="string")
parser.add_option("-o", "--output-prefix", dest = "opref", help = "prefix for output files (required)", metavar = "string")
parser.add_option("-r", "--release", dest="release", help="read files in <biocyc-dir>/<organism>/<release>/data/", metavar="string")
parser.add_option("-i", "--id-file", dest = "idfile", help = "file to map uniprot ids to the desired identifiers in the format <uniprot id>\\t<desired id>\\n", metavar = "FILE")

(options, args) = parser.parse_args()


# Check all the required args have been specified:
error = None
if options.org is None:
    sys.stderr.write("--organism ORGANISM is required.\n")
    error = True
if options.biocyc is None:
    sys.stderr.write("--biocyc DIRECTORY is required.\n")
    error = True
if options.opref is None:
    sys.stderr.write("--prefix PREFIX is required.\n")
    error = True
if error:
    sys.exit()


pattern_id = re.compile("=GF AC\s+(.+)")
pattern_gene = re.compile("=GS (.+_" + options.org + ")" )


# If "pathways.col: is found, colspath will be set to base + release + cols:
colspath = None
base = options.biocyc + '/' + options.org.lower() + '/'
cols = '/data/' + 'pathways.col'

# For backwards compatibility, search for a suitable "release":
if options.release is None:
    for release in os.listdir(base):
        testcols = base + release + cols
        if os.path.isfile(testcols):
            colspath=testcols
            break
else:
    release  = options.release
    testcols = base + release + cols
    if os.path.isfile(testcols):
        colspath=testcols

if colspath is None:
    if options.release is None:
        print >> sys.stderr, "Error: pathways.col not found under " + base + 'data/'
    else:
        print >> sys.stderr, "Error: " + testcols + " not found"
    sys.exit()

print >> sys.stderr, "Using Biocyc release:", release

biocyc = open(colspath)
biocyc_dat = open(options.opref + ".dat", "w")

id_name = None
if options.idfile is not None:
    id_name = idmap(options.idfile)

for line in biocyc:
    if line[0] == '#':
        continue

    fields = line.rstrip('\n').split('\t')

    if fields[0] == 'UNIQUE-ID':
        continue

    pathway_unique_id = fields.pop(0)
    pathway_name = fields.pop(0)

    #print fields

    path_genes = []
    for g in fields:
        if g == '':
            continue

        if id_name is not None:
            gene_names = id_name.get(g)
            if gene_names is None:
                continue
            path_genes.extend(gene_names)
        else:
            path_genes.append(g)

    for i, g1 in enumerate(path_genes):
        for j in xrange(i+1, len(path_genes)):
            g2 = path_genes[j]
            biocyc_dat.write('\t'.join((g1, g2, '1', '')) + '\n')

try:
    quant_f = open(options.opref + ".quant", "w")
    quant_f.write('\t'.join(('0.5','1.5')))
finally:
    quant_f.close()
