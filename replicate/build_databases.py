
import os
import sys

db_names = ['hprd', 'mint', 'mips', 'intact', 'bind', 'pdzbase', 'reactome']
#org_names = ['arabidopsis', 'celegans', 'fly', 'frog', 'human', 'mouse', 'rat', 'yeast']
# dbs.append('dip')
#db_names = ['dummy']
org_names = ['human'] # Paper only looked at human genes

class database:
    def __init__(self, n):
        self.name = n
        self.proteins = {}
        self.interactions = {}
        self.citations = 0
        self.overlap = {} # Stores overlap in (interactions, proteins) under name
        self.mult_cit = {}
    def set_values(self, p, i, c):
        self.proteins = p
        self.interactions = i
        self.citations = c
    def calculate_intrinsic(self):
        self.degree = {}
        lens = []
        for v in self.proteins.values():
            bin = len(v) / 10
            if bin not in self.degree:
                self.degree[bin] = 0
            self.degree[bin] += 1
            lens.append(len(v))
        self.avg_degree = sum(lens)/float(len(lens))
        self.avg_citations = self.citations / float(len(self.interactions.keys()))

        for v in self.interactions.values():
            bin = len(v)
            if bin not in self.mult_cit:
                self.mult_cit[bin] = 0
            self.mult_cit[bin] += 1

        return (self.avg_degree, self.avg_citations)
    def disease(self):
        pass # Access OMIM database to filter for genes associated with diseases
    def compare(self, other):
        try:
            self.overlap[other.name] = other.overlap[self.name]
        except KeyError:
            p_over = set(self.proteins.keys()).intersection(set(other.proteins.keys()))
            i_over = set(self.interactions.keys()).intersection(set(other.interactions.keys()))
            self.overlap[other.name] = (i_over, p_over)
        return (len(self.overlap[other.name][0]), len(self.overlap[other.name][1]))

def extract(path):
    proteins = {} #Will store list of interactors under main protein name
    interactions = {} #Will store list of citations under pairwise interactions
    citations = 0 #Will store total number of citations
    with open(path, 'r') as f:
        for line in f:
            linelist = line.split('\t')
            if linelist[0] not in proteins:
                proteins[linelist[0]] = []
            if linelist[1] not in proteins:
                proteins[linelist[1]] = []
            proteins[linelist[0]].append(linelist[1])
            proteins[linelist[1]].append(linelist[0])

            if linelist[0] > linelist[1]: #Lesser goes first
                hold = linelist[1]
                linelist[1] = linelist[0]
                linelist[0] = hold

            pair = (linelist[0], linelist[1])
            if pair not in interactions:
                interactions[pair] = []
            pubid = linelist[3].strip().split(',')
            interactions[pair].extend(pubid)
            citations += len(pubid)
    name = path.split('/')[3][:6]
    dbs[name] = database(name)
    dbs[name].set_values(proteins, interactions, citations)
    print '\nIn', name, '...'
    print len(proteins.keys()), '\tnumber of proteins'
    print len(interactions.keys()), '\tnumber of interactions'
    print citations, '\ttotal citations'
            

dbs = {}
function = '../../../'
for db_name in db_names:
    db_path = function + db_name
    for dirname in os.listdir(db_path):
        if dirname in org_names:
            for filename in os.listdir(db_path + '/' + dirname):
                if filename.endswith('.dat'):
                    extract('/'.join((db_path, dirname, filename)))
                    break # Only expect single dat file per organism in a database
print dbs.keys(), '\n\n'

print '\t'.join(('Name', 'Avg. Degree', 'Avg. Citations per Interaction'))
for db in dbs.itervalues():
    print db.name, '\t%.5f\t\t%.5f' % db.calculate_intrinsic()
print '\n\n', "Distribution of Proteins by Interactors per protein"
print '\t'.join(('db','1-10','11-20','21-30','31-40','41-50','51-60', '61-70', '71-80', '81-90', '91-100', '>100'))
for db in dbs.itervalues():
    strings = [db.name]
    first = range(10)
    for num in first:
        try:
            strings.append(str(db.degree[num]))
        except KeyError:
            strings.append('0')
    total = 0
    for key in db.degree.keys():
        if key not in first:
            total += db.degree[key]
    strings.append(str(total))
        
    print '\t'.join(strings)

print '\n\n', "Distribution of Percent of Interactions by Citations per Interaction"
print '\t'.join(('db', '1', '2', '3', '4', '>=5'))
for db in dbs.itervalues():
    raws = []
    first = range(1, 5)
    for num in first:
        try:
            raws.append(db.mult_cit[num])
        except KeyError:
            raws.append(0)
    total = 0
    for key in db.mult_cit.keys():
        if key not in first:
            total += db.mult_cit[key]
    raws.append(total)
    strings = [db.name]
    strings.extend([t / float(sum(raws)) for t in raws])
    print '%s \t%.5f\t%.5f\t%.5f\t%.5f\t%.5f' % tuple(strings)

print '\n\n'
for db1 in dbs.itervalues():
    for db2 in dbs.itervalues():
        if db1 >= db2: continue
        print db1.name, db2.name, db1.compare(db2)

# Count proteins - Done
# Count interactions - Done
# Bin proteins by interactions per protein - Done
# Calculate average - Done
# Bin interactions by citations per - Done
# Calculate average - Done
# Num human genes w/ interacting protein
# Number disease-associated human genes
