"""
Step 2 : colexification ranking.

The result:
1. A standard output.
2. A file output.
"""

from lingpy import *
from collections import defaultdict
import statistics
from tabulate import tabulate


def colidx(wordlist, ref="cogids", concept="concept", annotation=None):
    """
    This function takes a wordlist file as an input and calculate the concept colexification.
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

# a dict object for concepts v.s. Chinese characters.
chinese = {}
for idx, concept, character in wl.iter_rows("concept", "characters"):
    character = character.replace(" ", "")
    if concept in chinese.keys():
        if character not in chinese.get(concept):
            if len(chinese.get(concept)) <= 2:
                # we take only maximum three Chinese compound words as example
                chinese[concept].append(character)
    else:
        chinese[concept] = [character]

with open('colexification_concepts.tsv', 'w') as csvf:
     csvf.write('\t'.join(['Concept', 'Chinese', 'colexification', 'derivation\n']))
     for c, colex, d in scores:
         character = ",".join(chinese[c]) 
         csvf.write('\t'.join([c, character, str(round(colex, 2)), d+'\n'])) # save to file
         print("{0:20}| {1:.2f}| {2:15}| {3:15}".format(
                c, colex, d,  character
            )) # standard output
