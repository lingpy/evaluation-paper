"""
Step 1 : Calculate the agreements between two types of 
cognate coversion methods via Bcube scores.

The Result:
A standard output. The rankings are sorted according to the F-score.
A tsv file with top 100 "low F-score" concepts.
"""

from lingpy.evaluate.acd import _get_bcubed_score as bcs
from lingpy import Wordlist
from lingpy.compare.partial import Partial

part = Partial("liusinitic.tsv")

# check if strict ids and loose ids are in the data.
if "strictid" not in part.columns:
    part.add_cognate_ids("cogids", "strictid", idtype="strict")
elif "looseid" not in part.columns:
    part.add_cognate_ids("cogids", "looseid", idtype="loose")

wordlist = Wordlist(part)

ranks = []
for concept in wordlist.rows:
    idxs = wordlist.get_list(row=concept, flat=True)
    cogsA = [wordlist[idx, "strictid"] for idx in idxs]
    cogsB = [wordlist[idx, "looseid"] for idx in idxs]
    p, r = bcs(cogsA, cogsB), bcs(cogsB, cogsA)
    f = 2 * (p * r) / (p + r)
    ranks += [[concept, p, r, f]]

with open('bcube_concepts.tsv', 'w') as file:
    file.write('\t'.join(['Concept','Precision','Recall','F-score\n']))
    for concept, p, r, f in sorted(ranks, key=lambda x: x[-1]):
        print("{0:20} | {1:.2f} | {2:.2f} | {3:.2f}".format(concept, p, r, f))
        file.write('\t'.join([concept, str(round(p, 2)), str(round(r, 2)), str(round(f, 2))+'\n']))
file.close()
