
from optparse import OptionParser
import re
from xml.etree import ElementTree as ET
import sys

cleantype_pattern = re.compile("\W")

usage = "usage: %prog [options]"
parser = OptionParser(usage, version = "%prog dev-unreleased")
parser.add_option("-p", "--psimi-file", dest = "psimi", help = "location of the psimi file to parse", metavar = "FILE")
parser.add_option("-i", "--id-file", dest = "idfile", help = "file to map gene-ids from the psimi to the desired identifiers in the format <id from psimi>\\t<desired id>\\n", metavar = "FILE")
parser.add_option("-o", "--output-prefix", dest = "opref", help = "prefix for output files", metavar = "string")

(options, args) = parser.parse_args()

if options.psimi is None:
    sys.stderr.write("--psimi-file is required.\n")
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

psimi = ET.parse(options.psimi)
interactions = psimi.findall('.//{net:sf:psidev:mi}interaction')
for interaction in interactions:
    try:
        pubid = interaction.find('.//{net:sf:psidev:mi}bibref').find('.//{net:sf:psidev:mi}primaryRef').attrib['id']
        pubid = pubid.replace(';', ',')
    except KeyError:
<<<<<<< local
        pubid = '-'
=======
        pubid = ''
>>>>>>> other
    reltype = interaction.find('.//{net:sf:psidev:mi}interactionDetection').find('.//{net:sf:psidev:mi}shortLabel').text
    genes = interaction.findall('.//{net:sf:psidev:mi}proteinParticipant')
    for i in xrange(len(genes)):
        for j in xrange(i + 1, len(genes)):
            try:
                genei = genes[i].find('.//{net:sf:psidev:mi}primaryRef').attrib['id']
                genej = genes[j].find('.//{net:sf:psidev:mi}primaryRef').attrib['id']
            except KeyError:
                continue
            if id_name is not None:
                try:
                    genei = id_name[genei]
                    genej = id_name[genej]
                except KeyError:
                    continue
                with open(options.opref + "_" + re.sub(cleantype_pattern, '_', reltype) + ".dat", 'a+') as rel_file:
                    rel_file.write('\t'.join((genei, genej, '1', pubid)) + '\n')
try:
    quant_f = open(options.opref + ".quant", "w")
    quant_f.write('\t'.join(('0.5','1.5')))
finally:
    quant_f.close()
