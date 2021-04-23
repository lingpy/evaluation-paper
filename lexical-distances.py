"""
Step 3
This stap calculates lexicostatistical distances between language pairs.

The results:
Four pairwise distance matrices in the PHYLIP formats
"""
from lingpy import Wordlist, basictypes
from lingpy.compare.partial import Partial
from lingpy.convert.strings import matrix2dst
from clldutils.text import strip_brackets, split_text
from collections import defaultdict
from itertools import combinations
from lexibank_liusinitic import Dataset as LS

def cogids2cogid(wordlist, ref="cogids", cognates="autoid", morphemes="morphemes_auto"):
    """
    Convert partial cognates to full cognates via shared morpheme.
    The selected morpheme will be shown as bold font in the EDICTOR interface
    """

    C, M = {}, {}
    current = 1
    for concept in wordlist.rows:
        base = split_text(strip_brackets(concept))[0].upper().replace(" ", "_")
        idxs = wordlist.get_list(row=concept, flat=True)
        cogids = defaultdict(list)
        for idx in idxs:
            M[idx] = [c for c in wordlist[idx, ref]]
            for cogid in basictypes.ints(wordlist[idx, ref]):
                cogids[cogid] += [idx]
        for i, (cogid, idxs) in enumerate(
            sorted(cogids.items(), key=lambda x: len(x[1]), reverse=True)
        ):
            for idx in idxs:
                if idx not in C:
                    C[idx] = current
                    M[idx][M[idx].index(cogid)] = base
                else:
                    M[idx][M[idx].index(cogid)] = "_" + base.lower()
            current += 1
    wordlist.add_entries(cognates, C, lambda x: x)
    if morphemes:
        wordlist.add_entries(morphemes, M, lambda x: x)


def cogid_from_morphemes(wl, ref="cogids", cognates="newcogid", morphemes="morphemes"):
    """
    Convert partial cognates to salient cognates according to manually highlighted morpheme column (salient)
    """

    lookup, D = {}, {}  # Store the data here
    for idx, cogids, morphemes in wl.iter_rows("cogids", "morphemes"):
        selected_cogids = []
        for cogid, morpheme in zip(cogids, morphemes):  # Make sure morphemes is a list!
            if not morpheme.startswith("_"):
                selected_cogids += [cogid]
        salient = tuple(selected_cogids)
        if salient in lookup:
            D[idx] = lookup[salient]
        elif D.values():
            next_cogid = max(D.values()) + 1
            lookup[salient] = next_cogid
            D[idx] = next_cogid
        else:
            lookup[salient] = 1
            D[idx] = 1

    wl.add_entries(cognates, D, lambda x: x)


def lexical_distances(wl, subset, ref="cogid"):
    """
    Compute lexicostatistical distance. The synonyms are ignored during the calculation.
    This function returns a matrix
    """

    matrix = [[0 for cell in range(wl.width)] for row in range(wl.width)]
    for (i, langA), (j, langB) in combinations(enumerate(wl.cols), r=2):
        common, total = 0, 0
        lookupA, lookupB = wl.get_dict(col=langA, entry=ref), wl.get_dict(
            col=langB, entry=ref
        )
        for concept in lookupA and subset:
            cogsA, cogsB = lookupA.get(concept, []), lookupB.get(concept, [])
            if [x for x in cogsA if x in cogsB]:
                common += 1
                total += 1
            elif cogsA and cogsB:  # This determines missing conepts now!
                total += 1
        matrix[i][j] = matrix[j][i] = 1 - (common / total)
    return matrix


# Load data
part = Partial(LS().raw_dir.joinpath('liusinitic.tsv').as_posix())

# Add salient cognates.
cogid_from_morphemes(part, ref="cogids", cognates="salientid", morphemes="morphemes")

# Check if all the essential columns are in the input file.
if "commonid" not in part.columns:
    cogids2cogid(part, ref="cogids", cognates="commonid", morphemes="morphemes_auto")
elif "strictid" not in part.columns:
    part.add_cognate_ids("cogids", "strictid", idtype="strict")
elif "looseid" not in part.columns:
    part.add_cognate_ids("cogids", "looseid", idtype="loose")

# An array with all the name of all the full cognate sets.
cognate_set_array = [
    x for x in part.columns if x not in ["cogids", "langid", "autoid", "concepticon_id", "doculect_id"] and "id" in x
]

# Take cut-off threshold 0.8
target_concepts = []
with open("results/cognate-set-comparison.tsv", "r") as f:
    data = []
    for line in f:
        data += [[x.strip() for x in line.split("\t")]]
    for row in data[1:]:
        #target_concepts +=[row[0]]
        if float(row[-1]) <= 0.8:
            target_concepts += [row[0]]
print(
    "{0:d} concepts are selected for computing distance matrices (the cut-off threshold is 0.8).".format(
        len(target_concepts)
    )
)

# Compute the distance matrices
Distances = {}
for cognate in cognate_set_array:
    key = cognate + "_dist"
    value = lexical_distances(part, target_concepts, cognate)
    Distances[key] = value


# Output
doculect_number = part.width
for output_column in cognate_set_array:
    m = Distances[output_column + "_dist"]
    matrix2dst(
        m, taxa=part.cols, filename="results/lexi_{0}".format(output_column), taxlen=10
    )

part.output(
    "tsv", filename="results/liusinitic.word_cognate", prettify=False
)  # As backup.
