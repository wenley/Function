
import sys
import os
from overlap import dbs

"""
Case Study of the overlap between Biogrid, Mint, and Intact
"""

orgs = ['fly', 'celegans', 'human', 'arabidopsis', 'yeast', 'mouse', 'rat', 'frog']

mint = {}
three = {}
intact = {}
biogrid = {}
mint_ids = {}
three_ids = {}
intact_ids = {}
biogrid_ids = {}

for org in orgs:
    biogrid[org] = set(dbs['biogrid'].org[org].ids.keys())
    total_ids = 
    biogrid_ids[org] = dbs['biogrid'].org[org].ids
    mint[org] = set(dbs['mint'].org[org].ids.keys())
    mint_ids[org] = dbs['mint'].org[org].ids
    intact[org] = set(dbs['intact'].org[org].ids.keys())
    intact_ids[org] = dbs['intact'].org[org].ids
    three[org] = biogrid[org].intersection(mint[org]).intersection(intact[org])
    all_c = 0
    for key in three[org]:
        all_ids = set(biogrid_ids[org][key]).intersection(mint_ids[org][key]).intersection(intact_ids[org][key])
        for num in all_ids:
            all_c += min(biogrid_ids[org][key].count(num),
                         mint_ids[org][key].count(num),
                         intact_ids[org][key].count(num))

    bm = len(biogrid[org].intersection(mint[org]).difference(three[org]))
    bi = len(biogrid[org].intersection(intact[org]).difference(three[org]))
    mi = len(mint[org].intersection(intact[org]).difference(three[org]))

    print org.upper()
    print "Total:\t\t\t", len(biogrid[org].union(mint[org]).union(intact[org]))
    print "All:\t\t", len(three[org])
    print "All IDs:\t\t\t", all_c
    print "Bio and Mint:\t\t", bm
    print "Bio and Intact:\t\t", bi
    print "Mint and Intact:\t", mi
    print "\nJust Bio:\t\t", len(biogrid[org]) - bm - bi - len(three[org])
    print "Just Mint:\t\t", len(mint[org]) - bm - mi - len(three[org])
    print "Just Intact:\t\t", len(intact[org]) - bi - mi - len(three[org])
    print '\n\n'
