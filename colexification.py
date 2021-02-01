"""
colexification ranking.

The result:
A screen output.
"""

from lingpy import *
from collections import defaultdict
import statistics
from tabulate import tabulate


def colidx(wordlist, ref="cogids", concept="concept"):

    etd = wordlist.get_etymdict(ref=ref)

    indices = {ln: {} for ln in wordlist.cols}
    for i, ln in enumerate(wordlist.cols):
        for cogid, reflexes in etd.items():
            if reflexes[i]:
                concepts = [wordlist[idx, concept] for idx in reflexes[i]]
                indices[ln][cogid] = len(set(concepts)) - 1
    all_scores = []
    for cnc in wordlist.rows:
        reflexes = wordlist.get_list(row=cnc, flat=True)
        scores = []
        for idx in reflexes:
            ln, cogids = wordlist[idx, "doculect"], wordlist[idx, ref]
            scores += [statistics.mean([indices[ln][cogid] for cogid in cogids])]
        all_scores += [[cnc, statistics.mean(scores)]]
    return sorted(all_scores, key=lambda x: (x[1], x[0]))


wl = Wordlist("liusinitic.tsv")

scores = colidx(wl)
print(tabulate(scores))
