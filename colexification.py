"""
colexification ranking.

The result:
A standard output. The results will be printed on the screen.
"""

from lingpy import *
from collections import defaultdict
import statistics
from tabulate import tabulate


def colidx(wordlist, ref="cogids", concept="concept", annotation=None):
    """
    This function takes the input data in a wordlist format.
    The input data must have a partial cognate column and a concept column.
    The annotation column is an option al column, the default is None.
    It is to check if the concept contains lexical entires which have suffix.
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
# output
print(tabulate(scores))
