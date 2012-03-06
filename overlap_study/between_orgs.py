import os

dbs = ['biocyc', 'biogrid', 'hprd' ,'intact', 'mint', 'mips', 'reactome']
# dbs = ['intact', 'mint']
orgs = ['arabidopsis', 'celegans', 'fly', 'frog', 'human', 'mouse', 'rat', 'yeast']

function = '../../../'

pairs = {}
for db in dbs:
    files = {}
    for dirname in os.listdir(function + db):
        if dirname not in orgs:
            continue
        for filename in os.listdir(function + db  + '/' + dirname):
            if filename.endswith('.dat'):
                files[dirname] = open(function + '/'.join((db, dirname, filename)), 'r')
    # Finish loading all files into dictionary
    for k, v in files.items():
        pairs[(db, k)] = set()
        for line in v:
            linelist = line.strip().split('\t')
            tup = (linelist[0], linelist[1])
            pairs[(db, k)].add(tup)
    for v in files.values():
        v.close()
    # Finish transfer to sets

for k1, v1 in pairs.items():
    for k2, v2 in pairs.items():
        if k1 < k2: # Stop looking both ways
            continue
        if k1[1] == k2[1]: # Stop looking at self
            continue
        if not len(v1.intersection(v2)) == 0:
            print k1, k2, len(v1.intersection(v2))
