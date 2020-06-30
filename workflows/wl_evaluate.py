from lingpy import *
from lingpy.evaluate.acd import bcubes
from lingpy.evaluate.acd import diff, _get_bcubed_score

wl = Wordlist('HM-wordlist-lebor.tsv')

D = {0:wl.columns}
didx=1
for idx in wl:
    if wl[idx, 'cogid'] !=0:
        D[didx]=[]
        for lab in D[0]:
            D[didx].append(wl[idx,lab])
        didx +=1

wl_filtered=Wordlist(D)
bcubes(wl_filtered, 'lebor_cogid','cogid')

def renumber(liste):
    x = {}
    count = 1
    out = []
    for idx in liste:
        if idx in x:
            out += [x[idx]]
        else:
            out += [count]
            x[idx] = count
            count += 1
    return out

text = ''
for concept in wl_filtered.rows:
    idxs = wl_filtered.get_list(row=concept, flat=True)
    cog_ratliff=[wl_filtered[idx, 'cogid'] for idx in idxs]
    cog_lebor = [wl_filtered[idx, 'lebor_cogid'] for idx in idxs]
    langs = [wl_filtered[idx, 'doculect'] for idx in idxs]
    
    cog_RATLIFF = renumber(cog_ratliff)
    cog_LEBOR = renumber(cog_lebor)


