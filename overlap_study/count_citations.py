import os
import sys
from optparse import OptionParser

usage = "usage: %prog [options]"

parser = OptionParser(usage, version = "%prog dev-unreleased")
parser.add_option('-a', "--do-all", dest = "doall", help = "do all databases", action = "store_true")
parser.add_option('-r', "--remove", dest = "remove", help = "remove databases from list, comma delimited", metavar = "string")

(options, args) = parser.parse_args()
dbs = ['biogrid', 'hprd', 'intact', 'mint', 'mips', 'pfama', 'reactome']

if options.doall:
    full = 1
    build = 0
else:
    for db_name in dbs[:]:
        if db_name not in args:
            dbs.remove(db_name)
    build = 1
if options.remove is not None:
    for name in options.remove.split(','):
        try:
            dbs.remove(name)
            full = 0
        except: pass

print dbs
sys.exit()

orgs = ['arabidopsis', 'celegans', 'fly', 'frog', 'human', 'mouse', 'rat', 'slime', 'yeast']

pubmed = {}
function = '../../..'
for db_name in dbs:
    for org_name in orgs:
        try:
            files = os.listdir('/'.join((function, db_name, org_name)))
        except: continue
        for filename in files:
            if filename.endswith('.dat'):
                toopen = '/'.join((function, db_name, org_name, filename))
                break
        with open(toopen, 'r') as f:
            for line in f:
                try:
                    ids = line.split('\t')[3].strip().split(',')
                except IndexError:
                    print db_name
                    print line
                    sys.exit()
                for num in ids:
                    if num not in pubmed:
                        pubmed[num] = 0
                    pubmed[num] += 1

reverse = {}
for num, count in pubmed.items():
    if count in reverse:
        reverse[count].append(num)
    else:
        reverse[count] = [num]

saveout = sys.stdout
if full:
    outname = 'output_all.txt'
    histname = 'hist_all.txt'
else:
    outname = 'output_' + '_'.join(dbs) + '.txt'
    histname = 'hist_' + '_'.join(dbs) + '.txt'

sys.stdout = open(outname, 'w')
counts = reverse.keys()
counts.sort()
counts.reverse()
for count in counts:
    print count, '\t', len(reverse[count]), '\t', '\t'.join(reverse[count])
sys.stdout.close()

sys.stdout = open(histname, 'w')
hist = {}
for count, ids in reverse.items():
    bin = count / 1000
    if bin not in hist:
        hist[bin] = 0
    hist[bin] += len(ids)
print 'bin\tids'
bins = hist.keys()
bins.sort()
bins.reverse()
for bin in bins:
    print bin, '\t', hist[bin]
sys.stdout.close()
sys.stdout = saveout

print len(pubmed), "total ids"
