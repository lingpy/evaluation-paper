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
import itertools

"""
function: auto cogid
convert cogid from cogids
"""


def cogids2cogid(wordlist, ref="cogids", cognates="autoid", morphemes="morphemes_auto"):
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


"""
function: semi cogid
convert cogid from cogids according to manually highlighted morpheme column
"""


def cogids2semi(wl, ref="cogids", cognates="semi", ref_morpheme="morphemes"):
    # starting point
    cids_array = set()
    for idx, cids in part.iter_rows(ref):
        for i in cids:
            cids_array.add(i)
    start_point = max(cids_array) + 10
    # start converting
    complex_cases = {}
    for idx, concept, cids, mor in part.iter_rows("concept", ref, ref_morpheme):
        if len(cids) == 1:
            part[idx, cognates] = cids
        else:
            hl = [i for i, x in enumerate(mor) if "_" not in x]
            if len(hl) == 1:
                part[idx, cognates] = cids[hl[0]]
            else:
                cids_tmp = sorted([cids[i] for i in hl])
                cids_key = tuple(cids_tmp)
                if cids_key not in complex_cases.keys():
                    complex_cases[cids_key] = start_point
                    part[idx, cognates] = start_point
                    start_point += 1
                else:
                    part[idx, cognates] = complex_cases[cids_key]


"""
function: lexicostatistics
This function ignore synonyms.
"""


def lexi_dist(wl, ctype, lanA, lanB):
    common_concepts = 0
    matches = 0
    for c in part.concepts:
        tmp = wl.get_dict(row=c, entry=ctype)
        if len(tmp.get(lanA)) != 0 and len(tmp.get(lanB)) != 0:
            common_concepts += 1
        language_A, language_B = tmp[lanA], tmp[lanB]
        intersect = [x for x in language_A if x in language_B]
        if len(intersect) != 0:
            matches += 1
    dist = 1 - (matches / common_concepts)
    return dist


"""
load data and recompute.
"""
# part = Partial("liusinitic.tsv")
part = Partial("liusinitic_semi.tsv")
part.add_entries("semiid", "cogids", lambda x: 0)
part.add_cognate_ids("cogids", "strictid", idtype="strict")
part.add_cognate_ids("cogids", "looseid", idtype="loose")
cogids2cogid(part, ref="cogids", cognates="autoid", morphemes="morphemes_auto")
cogids2semi(part, ref="cogids", cognates="semiid", ref_morpheme="morphemes")


"""
main task.
"""
language_pair = {}
for a, b in itertools.combinations(part.doculect, 2):
    auto_d = lexi_dist(part, "autoid", a, b)
    loose_d = lexi_dist(part, "looseid", a, b)
    strict_d = lexi_dist(part, "strictid", a, b)
    semi_d = lexi_dist(part, "semiid", a, b)
    language_pair[(a, b)] = {
        "autoid_dist": auto_d,
        "strictid_dist": strict_d,
        "looseid_dist": loose_d,
        "semiid_dist": semi_d,
    }

"""
output
"""
doculect_number = len(part.doculect)
for output_column in ["autoid", "strictid", "looseid", "semiid"]:
    with open("lexi_{0}.dst".format(output_column), "w") as f:
        f.write("\t" + str(doculect_number) + "\n")
        for i in part.doculect:
            tmp = [i]
            for j in part.doculect:
                if language_pair.get((i, j)):
                    tmp.append(str(language_pair[(i, j)][output_column + "_dist"]))
                elif i == j:
                    tmp.append(str(0))
                else:
                    tmp.append(str(language_pair[(j, i)][output_column + "_dist"]))
            f.write("\t".join(tmp) + "\n")
