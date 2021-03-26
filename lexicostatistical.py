"""
Step 3: lexicostatistical distances between language pairs.
The result is pairwise-distance matrices
"""
from lingpy import Wordlist
from lingpy.compare.partial import Partial
from lingpy import basictypes
from clldutils.text import strip_brackets, split_text
from collections import defaultdict
from itertools import combinations
from sys import argv


def cogids2cogid(wordlist, ref="cogids", cognates="autoid", morphemes="morphemes_auto"):
    """
    Function: convert cogids to cogid via shared morpheme.
    The selected morpheme will be shown as bold font in Edictor.
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
    function: salient cogid
    convert cogid from cogids according to manually highlighted morpheme column (salient)
    """
    lookup, D = {}, {}  # store the data here
    for idx, cogids, morphemes in wl.iter_rows("cogids", "morphemes"):
        selected_cogids = []
        for cogid, morpheme in zip(cogids, morphemes):  # make sure morphemes is a list!
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
    function: lexicostatistics
    This function ignore synonyms.
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
            elif cogsA and cogsB:  # this determines missing conepts now!
                total += 1
        matrix[i][j] = matrix[j][i] = 1 - (common / total)
    return matrix


"""
load data and conversion
"""

part = Partial("liusinitic.tsv")

# check if all the essential columns are in the input file
if "--add_salient" in argv:
    # calculate salient cognate sets (computer-assisted approach) if "add_salient" exists.
    cogid_from_morphemes(
        part, ref="cogids", cognates="salientid", morphemes="morphemes"
    )
elif "greedid" not in part.columns:
    cogids2cogid(part, ref="cogids", cognates="greedid", morphemes="morphemes_auto")
elif "strictid" not in part.columns:
    part.add_cognate_ids("cogids", "strictid", idtype="strict")
elif "looseid" not in part.columns:
    part.add_cognate_ids("cogids", "looseid", idtype="loose")

# an array with all the converted cognate sets.
cognate_set_array = [
    x for x in part.columns if x not in ["cogids", "langid", "autoid"] and "id" in x
]

# take 100 concepts
target_concepts = []
with open("bcube_concepts.tsv", "r") as csvf:
    target_concepts = [
        x.strip().split("\t")[0] for i, x in enumerate(csvf.readlines()) if i <= 100
    ]

"""
main task.
"""
Distances = {}
for cognate in cognate_set_array:
    key = cognate + "_dist"
    value = lexical_distances(part, target_concepts, cognate)
    Distances[key] = value


"""
output
"""
doculect_number = part.width
for output_column in cognate_set_array:
    with open("lexi_{0}.dst".format(output_column), "w") as f:
        f.write("\t" + str(doculect_number) + "\n")
        m = Distances[output_column + "_dist"]
        for i, doc in enumerate(part.cols):
            tmp = "\t".join([str(x) for x in m[i]])
            f.write("{0}\t{1}\n".format(doc, tmp))

part.output("tsv", filename="liusinitic.word_cognate", prettify=False)
