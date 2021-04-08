"""
Step 2 
Cross-semantic cognate statistics.

The results:
1. A standard output.
2. A TSV file.
"""

from lingpy import *
from collections import defaultdict
import statistics
from tabulate import tabulate
from lexibank_liusinitic import Dataset as LS


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
    )  # Key is a partial cognate id, value is the index.
    indices = {ln: {} for ln in wordlist.cols}  # Setup a dictionary to collect taxa.
    for i, ln in enumerate(wordlist.cols):
        for cogid, reflexes in etd.items():
            if reflexes[i]:
                concepts = [wordlist[idx, concept] for idx in reflexes[i]]
                indices[ln][cogid] = len(set(concepts)) - 1
    all_scores = []
    for cnc in wordlist.rows:
        # Loop through all the concepts in the data
        reflexes = wordlist.get_list(
            row=cnc, flat=True
        )  # The lexical entries of the concept.
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


# Load data
wl = Wordlist(LS().raw_dir.joinpath('liusinitic.tsv').as_posix())

# Calculate the score of cross semantic cognate statistics
scores = colidx(wl, ref="cogids", concept="concept", annotation="morphemes")

# A dictionary object for concepts v.s. Chinese characters.
chinese = {}
for idx, concept, character in wl.iter_rows("concept", "characters"):
    character = character.replace(" ", "")
    if concept in chinese.keys():
        if character not in chinese.get(concept):
            if len(chinese.get(concept)) <= 2:
                # Take maximum three Chinese compound words as examples
                chinese[concept].append(character)
    else:
        chinese[concept] = [character]

with open("results/cross-semantic-cognate-statistics.tsv", "w") as f:
    f.write("\t".join(["Concept", "Chinese", "Score", "Derivation\n"]))
    for c, colex, d in scores:
        character = ",".join(chinese[c])
        f.write(
            "\t".join([c, character, str(round(colex, 2)), d + "\n"])
        )  # Save to file
        print(
            "{0:20}| {1:.2f}| {2:15}| {3:15}".format(c, colex, d, character)
        )  # Standard output
