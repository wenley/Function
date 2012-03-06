
import sys
import os
import re
from optparse import OptionParser

usage = "usage: %prog [options]"
parser = OptionParser(usage, version = "%prog dev-unreleased")
parser.add_option('-a', "--do-all", dest = "all_db", help = "Do all databases?", action = "store_true")
parser.add_option('-o', "--organism", dest = "org_choice", help = "Which organisms to do?", metavar = "string")
parser.add_option('-p', "--output-path", dest = "output_prefix", help = "Location of output files", metavar = "string")

(options, args) = parser.parse_args()

class database:
    def __init__(self, n):
        self.name = n
        self.short = n[:7]
        self.org = {}
    def add_org(self, org, ids):
        char = self.name + org
        self.org[org] = db_org(char)
        self.org[org].set_ids(ids)

class db_org:
    """
    Holds the key information about a databases's knowledge of a given organism
    ID analysis considers gene pairs accounting for varying PubMedIDs
    Gene Pair analysis only considers unique pairs
    Set analysis returns the Jaccard index between the two databases
    """
    def __init__(self, n):
        self.name = n
#        self.short = self.name[:6]
        self.id_overlap = {}
        self.gp_overlap = {}
        self.inter = {}
        self.union = {}
    def set_ids(self, i):
        self.ids = i
        self.gp_size = len(self.ids)
        self.id_size = 0
        for v in self.ids.itervalues():
#            if v == '': continue#
            self.id_size += len(v)
    def id_compare(self, another): # Number exactly duplicate citations
        try:
            idc = another.id_overlap[self.name]
        except KeyError:
            idc = 0
            for k, v1 in self.ids.iteritems():
                if k not in another.ids:
                    continue
                v2 = another.ids[k]
                setself = set(v1)
                setother = set(v2)
                for elem in setself.intersection(setother):
                    idc += min([v1.count(elem), v2.count(elem)])
            self.id_overlap[another.name] = idc
        return idc
    def gp_compare(self, another): # Overlap in unique gene pairs
        try:
            gpc = another.gp_overlap[self.name]
        except KeyError:
            setself = set(self.ids.keys())
            setother = set(another.ids.keys())
            self.inter[another.name] = setself.intersection(setother)
            gpc = len(self.inter[another.name])
            self.gp_overlap[another.name] = gpc
        return gpc
    def set_compare(self, another): # Jaccard index
        try:
            self.union[another.name] = another.union[self.name]
            self.inter[another.name] = another.inter[self.name]
        except KeyError:
            setself = set(self.ids.keys())
            setother = set(another.ids.keys())
            self.union[another.name] = setself.union(setother)
            self.inter[another.name] = setself.intersection(setother)
        return (len(self.inter[another.name]), len(self.union[another.name]))

# Store pubids under gene pair
def parse_gene_pairs(path, ids = {}):
    """
    Parses .dat file of given path with four column format:
    genea geneb weight pubid
    Stores pubids under gene pairs
    Appends to optional dictionary
    Returns finished dictionary
    """
    with open(path, 'r') as f:
        for line in f:
            linelist = line.split('\t')
            genea = linelist[0]
            geneb = linelist[1]
            tup = (genea, geneb)
            pubids = linelist[3].strip().split(',')

            if tup not in ids:
                ids[tup] = []
            if not pubids: continue
            ids[tup].extend(pubids)
    return ids

def do_dat(basepath, organism):
    db_name = os.path.split(basepath[:-1])[1]
    
    ids = {}
    subdir = basepath + organism
    if not os.path.exists(subdir):
        return 0
    for filename in os.listdir(subdir):
        if filename.endswith('.dat'):
            path = subdir + '/' + filename
            break # Know only looking for single .dat in given directory
    parse_gene_pairs(path, ids)
    if ids:
        if db_name not in dbs:
            dbs[db_name] = database(db_name)
        dbs[db_name].add_org(organism, ids)

def print_results(organism, database, subdir):
    if organism not in database.org:
        return 0

    path = subdir + '_'.join([database.name, organism]) + '.txt'
    saveout = sys.stdout
    f = open(path, 'w')
    sys.stdout = f

    print database.name.upper()
    print organism.upper(), '\n'

    firstline = '\t'.join(["ID size", "GP size", "DB name", "ID raw", "GP raw", "Set raw", "ID prop", "GP prop", "Set pro"])
    print firstline

    for v in dbs.itervalues():
        if organism not in v.org:
            continue
        things = []

        if v.name == 'biocyc' or database.name == 'biocyc':
            bc = 1
        else: bc = 0
        if bc:
            things.append('-')
        else:
            things.append(str(v.org[organism].id_size))
        things.append(str(v.org[organism].gp_size))
        things.append(v.short)

        if v == database:
            x = ['-', '-', '-', '1', '1', '1']
            things.extend(x)
            print '\t'.join(things)
            continue
        # Otherwise...
        if bc:
            things.append('-')
        else:
            id_raw = v.org[organism].id_compare(database.org[organism])
            things.append(str(id_raw))
            id_pro = id_raw / float(v.org[organism].id_size)


        gp_raw = v.org[organism].gp_compare(database.org[organism])
        things.append(str(gp_raw))
        gp_pro = gp_raw / float(v.org[organism].gp_size)

        set_out = v.org[organism].set_compare(database.org[organism])
        things.append(str(set_out[0]))
        set_pro = set_out[0] / float(set_out[1])

        if not bc:
            things.append('%.5f' % id_pro)
        else:
            things.append('-')
        things.append('%.5f' % gp_pro)
        things.append('%.5f' % set_pro)

        print '\t'.join(things)

    sys.stdout = saveout
    f.close()

dbs = {}

orgs = ['arabidopsis', 'celegans', 'fly', 'frog', 'human', 'mouse', 'rat', 'slime', 'yeast', 'all']

if __name__ == "overlap":
    print "Accessed if."
    options.all_db = 'all'
    options.org_choice = 'all'
    paths = {}
    paths['mint'] = '../../../mint/'
    paths['biogrid'] = '../../../biogrid/'
    paths['intact'] = '../../../intact/'
    paths['mips'] = '../../../mips/'
    paths['reactome'] = '../../../reactome/'
    paths['hprd'] = '../../../hprd/'
    paths['biocyc'] = '../../../biocyc/'
    # paths['pfama'] = '../../../pfama/'

    runs = paths.keys()
    for o in orgs[:-1]: #Exclude 'all' tag
        for key in runs:
            do_dat(paths[key], o)

if options.org_choice not in orgs:
    sys.stderr.write("Invalid choice of organism.\n")
    sys.exit()

if __name__ == '__main__':
    paths = {}
    paths['mint'] = '../../../mint/'
    paths['biogrid'] = '../../../biogrid/'
    paths['intact'] = '../../../intact/'
    paths['mips'] = '../../../mips/'
    paths['reactome'] = '../../../reactome/'
    paths['hprd'] = '../../../hprd/'
    paths['biocyc'] = '../../../biocyc/'
    paths['pfama'] = '../../../pfama/'

    runs = []
    if options.all_db:
        runs.extend(paths.keys())
    for tag in args:
        if tag in paths.keys() and tag not in runs:
            runs.append(tag)
        elif tag[0] == '-' and tag[1:] in paths.keys():
            try:
                runs.remove(tag[1:])
            except ValueError: pass
        else:
            print "Ignored invalid tag,", tag

    if len(runs) < 2:
        print "Need at least two databases to work with."
        sys.exit()

    if options.org_choice == 'all':
        for o in orgs[:-1]: #Exclude 'all' tag
            for key in runs:
                do_dat(paths[key], o)
    else:
        for key in runs:
            do_dat(paths[key], options.org_choice)

    for o in orgs[:-1]:
        for db in dbs.itervalues():
            print_results(o, db, options.output_prefix)

if __name__ == 'overlap':
    paths = {}
    paths['mint'] = '../../../mint/'
    paths['biogrid'] = '../../../biogrid/'
    paths['intact'] = '../../../intact/'
    paths['mips'] = '../../../mips/'
    paths['reactome'] = '../../../reactome/'
    paths['hprd'] = '../../../hprd/'
    paths['biocyc'] = '../../../biocyc/'
    # paths['pfama'] = '../../../pfama/'

    runs = paths.keys()
    for o in orgs[:-1]: #Exclude 'all' tag
        for key in runs:
            do_dat(paths[key], o)
