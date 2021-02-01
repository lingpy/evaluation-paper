"""
Calculate the agreements between two types of 
cognate coversion methods via Bcube scores.

The Result:
A screen output.
"""

from lingpy.evaluate.acd import _get_bcubed_score as bcs
from lingpy import Wordlist

wordlist = Wordlist("liusinitic.tsv")

ranks = []
for concept in wordlist.rows:
    idxs = wordlist.get_list(row=concept, flat=True)
    cogsA = [wordlist[idx, "strictid"] for idx in idxs]
    cogsB = [wordlist[idx, "looseid"] for idx in idxs]
    p, r = bcs(cogsA, cogsB), bcs(cogsB, cogsA)
    f = 2 * (p * r) / (p + r)
    ranks += [[concept, p, r, f]]

for concept, p, r, f in sorted(ranks, key=lambda x: x[-1]):
    print("{0:20} | {1:.2f} | {2:.2f} | {3:.2f}".format(concept, p, r, f))
