from optparse import OptionParser
import re
import sys
from idmap import idmap

usage = "usage: %prog [options]"
parser = OptionParser(usage, version = "%prog dev-unreleased")
parser.add_option("-p", "--pfam-file", dest="pfam", help="location of pfam file", metavar="FILE")
parser.add_option("-s", "--organism", dest="org", help="Uniprot organism code", metavar="string")
parser.add_option("-o", "--output-prefix", dest = "opref", help = "prefix for output files", metavar = "string")
parser.add_option("-i", "--id-file", dest = "idfile", help = "file to map uniprot ids to the desired identifiers in the format <uniprot id>\\t<desired id>\\n", metavar = "FILE")


(options, args) = parser.parse_args()

if options.org is None:
    sys.stderr.write("--organism is required.\n")
    sys.exit()
if options.pfam is None:
    sys.stderr.write("--pfam file is required.\n")
    sys.exit()
if options.opref is None:
    sys.stderr.write("--prefix is required.\n")
    sys.exit()


pattern_id = re.compile("=GF AC\s+(.+)")
pattern_gene = re.compile("=GS (.+_" + options.org + ")" )
<<<<<<< local
pattern_pub = re.compile("=GF RM\s+(\d+)")
=======
pattern_pub = re.compile("=GF RM\s+(?P<pub>\d+)")
pattern_head = re.compile("=GF ID")
>>>>>>> other

pfam = open(options.pfam)
pfam_dat = open(options.opref + ".dat", "w")

id_name = None
if options.idfile is not None:
    id_name = idmap(options.idfile)

astrgenes = []

first = 1
for line in pfam:
    line = line.strip()

    if first:
        pubs = []
        first = 0
    elif re.search(pattern_head, line): # Found beginning of new set
        pubjoin = ','.join(pubs)
        for i in range(0, len(astrgenes)):
            for j in range(i + 1, len(astrgenes)):
                pfam_dat.write('\t'.join((astrgenes[i], astrgenes[j], '1', pubjoin)) + '\n')
        pubs = [] # Reset collection of PubMedIDs
        astrgenes = [] # Reset collection of genes

    try:
        pub = re.search(pattern_pub, line).group('pub')
        pubs.append(pub)
    except AttributeError: pass

    gid=re.search(pattern_gene,line)
    if gid:
        gene = gid.group(1).upper()
        if id_name is not None:
            gene_names = id_name.get(gene)
            if gene_names is None:
                continue
            for g in gene_names:
                try:
                    astrgenes.index(g)
                except ValueError:
                    astrgenes.append(g)
                    continue
        else:
            try:
                astrgenes.index(gene)
            except ValueError:
                astrgenes.append(gene)
                continue

# Finished reading whole file; print last group
pubjoin = ','.join(pubs)
for i in range(0, len(astrgenes)):
    for j in range(i+1, len(astrgenes)):
        pfam_dat.write('\t'.join((astrgenes[i], astrgenes[j], '1', pubjoin)) + '\n')

try:
    quant_f = open(options.opref + ".quant", "w")
    quant_f.write('\t'.join(('0.5','1.5')))
finally:
    quant_f.close()
