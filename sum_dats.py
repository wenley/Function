
from optparse import OptionParser
import sys, os

usage = "usage: %prog [options]"
parser = OptionParser(usage, version = "%prog dev-unreleased")
parser.add_option("-i", "--input-dir", dest = "input", help = "the directory containing the binary dat files to sum", metavar = "FILE")
parser.add_option("-o", "--output-prefix", dest = "output", help = "the name of the file that the final dat will be output to (.dat will be appended and .quant will be made)", metavar = "FILE")

(options, args) = parser.parse_args()

if options.input is None:
    sys.stderr.write("--input-dir is required.\n")
    sys.exit()

if options.output is None:
    sys.stderr.write("--output-prefix is required.\n")
    sys.exit()

gene_interactions = {}

for filename in os.listdir(options.input):
    if filename.endswith('.dat'):
        int_type = filename.split('.')[0]
        with open(options.input + '/' + filename) as input_file:
            for line in input_file:
                try:
                    (genea, geneb, interaction, pubid) = line.strip().split()[:4]
                except ValueError:
                    (genea, geneb, interaction) = line.strip().split()[:3]
                    pubid = None
                if interaction == '1':
                    if genea <= geneb:
<<<<<<< local
                        try:
                            gene_interactions[(genea, geneb)][0].add(int_type)
                            if pubid:
                                gene_interactions[(genea, geneb)][1].add(pubid)
                        except KeyError:
                            if pubid:
                                gene_interactions[(genea, geneb)] = (set((int_type,)), set((pubid,)))
                            else:
                                gene_interactions[(genea, geneb)] = (set((int_type,)), set())
=======
                        key = (genea, geneb)
                        if key not in gene_interactions:
                            gene_interactions[key] = (set((int_type,)), [])
                        if pubid:
                            gene_interactions[key][1].append(pubid)
                        gene_interactions[key][0].add(int_type)
>>>>>>> other
                    else:
<<<<<<< local
                        try:
                            gene_interactions[(geneb, genea)][0].add(int_type)
                            if pubid:
                                gene_interactions[(geneb, genea)][1].add(pubid)
                        except KeyError:
                            if pubid:
                                gene_interactions[(geneb, genea)] = (set((int_type,)), set((pubid,)))
                            else:
                                gene_interactions[(geneb, genea)] = (set((int_type,)), set())
=======
                        key = (geneb, genea)
                        if key not in gene_interactions:
                            gene_interactions[key] = (set((int_type,)), [])
                        if pubid:
                            gene_interactions[key][1].append(pubid)
                        gene_interactions[key][0].add(int_type)
>>>>>>> other
                else:
                    sys.stderr.write("This is only meant for use on binary dat files")
                    sys.exit()

with open(options.output + '.dat', 'w') as output:
    for (genes, (types, pubids)) in gene_interactions.iteritems():
        output.write('\t'.join(genes) + '\t' + str(len(types)) + '\t' + ','.join(list(pubids)) + '\n')

with open(options.output + '.quant', 'w') as quant:
    quant.write('\t'.join(('0.5', '1.5', '2.5', '4.5')) + '\n')
