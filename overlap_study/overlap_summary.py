
import os
import sys
import re
from optparse import OptionParser

usage = "usage: %prog [options]"
parser = OptionParser(usage, version = "%prog dev-unreleased")
parser.add_option('-o', "--organism", dest = "org_choice", help = "Which organism to summarize?", metavar = "string")
parser.add_option('-d', "--database", dest = "db_choice", help = "Which database to summarize?", metavar = "string")
parser.add_option('-p', "--output-dir", dest = "subdir", help = "Where to put summaries?", metavar = "string")
parser.add_option('-i', "--intput-dir", dest = "indir", help = "Where to find outputs?", metavar = "string")

(options, args) = parser.parse_args()

orgs = ['arabidopsis', 'celegans', 'fly', 'frog', 'human', 'mouse', 'rat', 'slime', 'yeast', 'all']
dbs = ['biocyc', 'biogrid', 'intact', 'mint', 'mips', 'pfama', 'reactome', 'hprd', 'all']
if not options.org_choice and not options.db_choice:
    sys.stderr.write("Nothing to summarize.\n")
    sys.exit()
if options.org_choice and options.org_choice not in orgs:
    sys.stderr.write("Invalid choice of organism.\n")
    sys.exit()
if options.db_choice and options.db_choice not in dbs:
    sys.stderr.write("Invalid choice of database.\n")
    sys.exit()

def summarize_org(org):
    f = open(options.subdir + org + '_summary.txt', 'w')
    for filename in os.listdir(options.indir):
        if filename.endswith(org + '.txt'):
            g = open(options.indir + filename, 'r')
            f.write(g.read())
            g.close()
            f.write('\n\n')
    f.close()

def summarize_db(db):
    f = open(options.subdir + db + '_summary.txt', 'w')
    for filename in os.listdir(options.indir):
        if filename.startswith(db):
            g = open(options.indir + filename, 'r')
            f.write(g.read())
            g.close()
            f.write('\n\n')
    f.close()
        
if options.org_choice and options.org_choice == 'all':
    for org in orgs[:-1]:
        summarize_org(org)
elif options.org_choice:
    summarize_org(options.org_choice)

if options.db_choice and options.db_choice == 'all':
    for db in dbs[:-3]: #Exclude reactome, hprd
        summarize_db(db)
elif options.db_choice and db in dbs[:-3]: #exclude reactome, hprd
    summarize_db(options.db_choice)
