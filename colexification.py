"""
Step 2 : colexification ranking.

The result:
A standard output.
"""

from lingpy import *
from collections import defaultdict
import statistics
from tabulate import tabulate


def colidx(wordlist, ref="cogids", concept="concept", annotation=None):
    """
    This function takes a wordlist file as an input
    Mandatory columns: 
        cogids and concept
    Optional column:
        annotation (check derivation)
    """

    etd = wordlist.get_etymdict(
        ref=ref
    )  # key is a partial cognate id, value is the index.
    indices = {ln: {} for ln in wordlist.cols}  # setup a dictionary to collect taxa.
    for i, ln in enumerate(wordlist.cols):
        for cogid, reflexes in etd.items():
            if reflexes[i]:
                concepts = [wordlist[idx, concept] for idx in reflexes[i]]
                indices[ln][cogid] = len(set(concepts)) - 1
    all_scores = []
    for cnc in wordlist.rows:
        # loop through all the concepts in the data
        reflexes = wordlist.get_list(
            row=cnc, flat=True
        )  # the lexical entries of the concept.
        scores = []
        derivation = 0
        for idx in reflexes:
            ln, cogids = wordlist[idx, "doculect"], wordlist[idx, ref]
            scores += [statistics.mean([indices[ln][cogid] for cogid in cogids])]
            for m in wordlist[idx, annotation]:
                if "SUF" in m or "suffix" in m:
                    derivation += 1
        if derivation > 0:
            all_scores += [[cnc, statistics.mean(scores), "!derivation!"]]
        else:
            all_scores += [[cnc, statistics.mean(scores), ""]]
    return sorted(all_scores, key=lambda x: (x[1], x[0]))


# load data
wl = Wordlist("liusinitic.tsv")

# calculate
scores = colidx(wl, ref="cogids", concept="concept", annotation="morphemes")

# standard output
print(tabulate(scores))

# save to file
with open('colexification_concepts.tsv', 'w') as csvf:
     csvf.write('\t'.join(['Concept', 'colexification', 'derivation\n']))
     for c, colex, d in scores:
         csvf.write('\t'.join([c, str(round(colex, 2)), d+'\n']))
