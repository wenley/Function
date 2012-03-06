
#N.B. Reactome has MANY duplicate annotations.  If these are not desired it might
#be best to put pairs into a set and to write that set out at a second step.

from optparse import OptionParser
import sys
import csv
from idmap import idmap

usage = "usage: %prog [options]"
parser = OptionParser(usage, version = "%prog dev-unreleased")
parser.add_option("-d", "--database-file", dest = "database", help = "location of database file", metavar = "FILE")
parser.add_option("-o", "--output-prefix", dest = "opref", help = "prefix for output files", metavar = "string")
parser.add_option("-i", "--id-file", dest = "idfile", help = "file to map UniProt identifiers to the desired identifiers in the format <uniprot id>\\t<desired id>\\n", metavar = "FILE")
parser.add_option("-a", "--a-column", dest = "acol", help = "the column where gene a's ID can be found (zero indexed)", metavar = "int", default = 0, type = "int")
parser.add_option("-b", "--b-column", dest = "bcol", help = "the column where gene b's ID can be found (zero indexed)", metavar = "int", default = 3, type = "int")
parser.add_option("-l", "--header-lines", dest = "hlines", help = "the number of header lines (default 0)", metavar = "int", default = 0, type = "int")
parser.add_option("-p", "--pubid-column", dest = "pcol", help = "the column where PubMed IDs can be found (zero indexed)", metavar = "int", default = 8, type = "int")
(options, args) = parser.parse_args()

if options.database is None:
    sys.stderr.write("--database-file is required.\n")
    sys.exit()
if options.opref is None:
    sys.stderr.write("--prefix is required.\n")
    sys.exit()
if options.acol is None or options.bcol is None:
    sys.stderr.write("--a-column and --b-column must be specified.\n")

id_name = None
if options.idfile is not None:
    id_name = idmap(options.idfile)

with open(options.database, 'rb') as db_file:
    db_reader = csv.reader(db_file, delimiter = '\t')
    try:
        with open(options.opref + ".dat", "w") as dbout_dat:
            for i in xrange(options.hlines):
                db_reader.next()
            for row in db_reader:
                genea = row[options.acol].split(':').pop()
                geneb = row[options.bcol].split(':').pop()
<<<<<<< local
=======
                interaction = row[6]
>>>>>>> other
                try:
                    pubids = row[options.pcol]
                except IndexError:
                    pubids = ''
                if id_name is not None:
                    genea_names = id_name.get(genea)
                    geneb_names = id_name.get(geneb)
                    if (genea_names is None or geneb_names is None):
                        #print('\t'.join([genea, str(genea_names), geneb, str(geneb_names)]))
                        pass
                    #elif (len(genea_names) > 1 or len(geneb_names) > 1):
                    #    print('\t'.join([genea, genea_names, geneb, geneb_names]))
                    if (genea_names is not None and geneb_names is not None):
                        for ga in genea_names:
                            for gb in geneb_names:
<<<<<<< local
                                dbout_dat.write('\t'.join((ga, gb, '1', pubids)) + '\n')
=======
                                dbout_dat.write('\t'.join((ga, gb, '1', pubids, interaction)) + '\n')
>>>>>>> other
                else:
<<<<<<< local
                    dbout_dat.write('\t'.join((genea, geneb, '', pubids)) + '\n')
=======
                    dbout_dat.write('\t'.join((genea, geneb, '', pubids, interaction)) + '\n')
>>>>>>> other
    except csv.Error, e:
        sys.exit('file %s, line %d: %s' % (options.database, db_reader.line_num, e))

try:
    zero_f = open("zeros.txt", "w")
    zero_f.write('\t'.join((options.opref, '0')))
finally:
    zero_f.close()

try:
    quant_f = open(options.opref + ".quant", "w")
    quant_f.write('\t'.join(('0.5', '1.5')))
finally:
    quant_f.close()
