#!/usr/bin/env python
# 
# create general txt files that correspond to pre post beta images for full triad and AC; will need to be edited for participants # with any excluded runs

import pandas as pd

table = pd.DataFrame(columns = ['phase', 'run', 'triad', 'item'])
for phase in range(2):
    for run in range(3):
        for triad in range(4):
            r =  (run + 1)
            for item in range(3):
                p = phase + 1
                #r = p * (run + 1)
                tri = triad + 1
                it = (item + 1)
                table.loc[len(table)] = [p, r, tri, it]
                
out = ('/home1/09123/ofriend/analysis/temple/bin/templates/pre_post_ABC_items.txt')
table.to_csv(out, sep='\t', header=False, index=False)



table = pd.DataFrame(columns = ['phase', 'run', 'triad', 'item'])
for phase in range(2):
    for run in range(3):
        for triad in range(4):
            p = phase + 1
            r =  (run + 1)
            tri = triad + 1
            table.loc[len(table)] = [p, r, tri, 1]
            table.loc[len(table)] = [p, r, tri, 2]
out = ('/home1/09123/ofriend/analysis/temple/bin/templates/pre_post_AC_items.txt')
table.to_csv(out, sep='\t', header=False, index=False)
