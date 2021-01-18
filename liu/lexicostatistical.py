"""
stage 1:
lexicostatistical distances between language pairs.
The result is a pairwise-distance matrix
"""
from lingpy import Wordlist
from lingpy.compare.partial import Partial
import pickle
from lingpy import basictypes
from clldutils.text import strip_brackets, split_text
from collections import defaultdict
from itertools import combinations


def cogids2cogid(wordlist, ref="cogids", cognates="autoid", morphemes="morphemes_auto"):
    """
    function: auto cogid
    convert cogid from cogids
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
    function: semi cogid
    convert cogid from cogids according to manually highlighted morpheme column
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


def lexical_distances(wl, ref="cogid"):
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
        for concept in lookupA:
            cogsA, cogsB = lookupA.get(concept, []), lookupB.get(concept, [])
            if [x for x in cogsA if x in cogsB]:
                common += 1
                total += 1
            elif cogsA and cogsB:  # this determines missing conepts now!
                total += 1
        matrix[i][j] = matrix[j][i] = 1 - (common / total)
    return matrix


"""
load data and recompute.
to do : uncomment or delete the semiid part.
"""
# part = Partial("liusinitic.tsv")
part = Partial("liusinitic.tsv")
# part.add_entries("semiid", "cogids", lambda x: 0)
part.add_cognate_ids("cogids", "strictid", idtype="strict")
part.add_cognate_ids("cogids", "looseid", idtype="loose")
cogids2cogid(part, ref="cogids", cognates="autoid", morphemes="morphemes_auto")
# cogid_from_morphemes(part, ref="cogids", cognates="semiid", morphemes="morphemes")

"""
main task.
"""
Distances = {}
for cognate in ["autoid", "looseid", "strictid",]:
    key = cognate + "_dist"
    value = lexical_distances(part, cognate)
    Distances[key] = value


"""
output
"""
doculect_number = part.width
for output_column in ["autoid", "strictid", "looseid"]:
    with open("lexi_{0}.dst".format(output_column), "w") as f:
        f.write("\t" + str(doculect_number) + "\n")
        m = Distances[output_column + "_dist"]
        for i, doc in enumerate(part.cols):
            tmp = "\t".join([str(x) for x in m[i]])
            f.write("{0}\t{1}\n".format(doc, tmp))
