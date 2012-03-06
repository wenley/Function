
from optparse import OptionParser
import re
import sys

type_pattern = re.compile("\((?P<type>[\w\s-]+)\)")
<<<<<<< local
pub_pattern = re.compile("pubmed:(?P<pub>[\d]+)")
=======
pub_pattern = re.compile('pubmed:(?P<pub>[\d]+)')
>>>>>>> other
cleantype_pattern = re.compile("\W")
gene_name_pattern = re.compile(":(?P<gene_name>\w+)") #might not need

usage = "usage: %prog [options]"
parser = OptionParser(usage, version = "%prog dev-unreleased")
parser.add_option("-m", "--mitab-file", dest = "mitab", help = "location of the mitab file to parse", metavar = "FILE")
parser.add_option("-i", "--id-file", dest = "idfile", help = "file to map gene-ids from the mitab to the desired identifiers in the format <id from mitab>\\t<desired id>\\n", metavar = "FILE")
parser.add_option("-o", "--output-prefix", dest = "opref", help = "prefix for output files", metavar = "string")
parser.add_option("-n", "--mint-db", dest = "mint", help = "is database mint style (only single gene-ids)?", action="store_true")
parser.add_option("-b", "--bind-db", dest = "bind", help = "is database bind style (no header)?", action = "store_true")

(options, args) = parser.parse_args()

if options.mint:
    gene_pattern = re.compile(":(?P<gene>\w+)")
else:
    gene_pattern = re.compile(":(?P<gene>\w+)\|")

if options.mitab is None:
    sys.stderr.write("--mitab-file is required.\n")
    sys.exit()

if options.opref is None:
    sys.stderr.write("--output-prefix is required.\n")
    sys.exit()

id_name = None
if options.idfile is not None:
    id_name = {}
    with open(options.idfile) as idfile:
        for line in idfile:
            linelist = line.strip().split()
            id_name[linelist[0]] = linelist[1]

with open(options.mitab) as mitab:
<<<<<<< local
    mitab.readline() #pass header
    pubids = []
#    c = 1#
=======
    if not options.bind:
        mitab.readline() #pass header
>>>>>>> other
    for line in mitab:
#        c = c + 1#
        linelist = line.strip().split('\t')
        try:
            genea = re.search(gene_pattern, linelist[0]).group('gene')
            geneb = re.search(gene_pattern, linelist[1]).group('gene')
        except AttributeError:
#            print "Attribute Error in line ", c#
            continue
        if id_name is not None:
            try:
                genea = id_name[genea]
                geneb = id_name[geneb]
            except KeyError:
#                print "Key error in line ", c#
                continue
        try:
            reltype = re.search(type_pattern, linelist[6]).group('type')
        except AttributeError:
            print('Unrecognized experiment type ' + linelist[6] + ".  Setting this as 'other.'")
            reltype = "other"
        try:
<<<<<<< local
            pubid = re.search(pub_pattern, linelist[8]).group('pub')
=======
            pubid = []
            for entry in linelist[8].split('|'):
                pubid.append(re.search(pub_pattern, entry).group('pub'))
            pubid = ','.join(pubid)
>>>>>>> other
        except AttributeError:
            pubid = ''

        with open(options.opref + "_" + re.sub(cleantype_pattern, '_', reltype) + ".dat", 'a+') as rel_file:
            rel_file.write('\t'.join((genea, geneb, '1', pubid)) + '\n')

        pub_f = open(options.opref + ".pub", "a+")
        try:
            genea_name = re.search(gene_name_pattern, linelist[2]).group('gene_name')
            geneb_name = re.search(gene_name_pattern, linelist[3]).group('gene_name')
#            pubid = re.search(pub_pattern, linelist[8]).group('pub')
            output = '\t'.join([pubid, genea_name, geneb_name, reltype])
            pub_f.write(output + '\n')
            pub_f.close()
        except AttributeError:
            pub_f.close()

        try:
            quant_f = open(options.opref + "_" + re.sub(cleantype_pattern, '_', reltype) + ".quant", "w")
            quant_f.write('\t'.join(('0.5','1.5')))
        finally:
            quant_f.close()
