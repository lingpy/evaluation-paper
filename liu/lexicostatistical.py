from lingpy import Wordlist
from lingpy.compare.partial import Partial
import pickle
from lingpy import basictypes
from clldutils.text import strip_brackets, split_text
from collections import defaultdict

# cogids2cogid
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


# lang_A and lang_B distance
# If there is no match between A and B, the matches -1. On the other hand, as long as there is/are match(es), the matches remain unchange regardless how many matches are found.
def lexi_dist(wl, concept_list, ctype, lanA, lanB):
    matches = len(concept_list)
    for c in concept_list:
        tmp = wl.get_dict(row=c, entry=ctype)
        language_A, language_B = tmp[lanA], tmp[lanB]
        intersect = [x for x in language_A if x in language_B]
        if intersect == []:
            matches = matches - 1
    dist = 1 - ((matches) / len(concept_list))
    return dist


# Load data
part = Partial("liusinitic.tsv")

# Re-compute loose and strict. Re-compute the auto cognates, but store in another column.
# todo: semi-automatic (i.e. human selects the parts) cognate extraction.
part.add_cognate_ids("cogids", "strictid", idtype="strict")
part.add_cognate_ids("cogids", "looseid", idtype="loose")
cogids2cogid(part, ref="cogids", cognates="autoid", morphemes="morphemes_auto")

# lumper and splitter.
# splitter
part.add_entries("splitid", {idx: idx for idx in part}, lambda x: x)
# lumper
part.renumber("concept", "lumpid")

# select concepts, we want concepts with full coverage.
# todo: allow cut-off threshold.
remove_ele = []
for c in part.concepts:
    concept_dict = part.get_dict(row=c, entry="cogids")
    for k, v in concept_dict.items():
        if v == []:
            remove_ele.append(c)
concept_list = [x for x in part.concepts if x not in set(remove_ele)]

# main calculation.
# todo: maybe add semi-automatic (i.e. human selects the parts) later.
language_pair = {}
for i in part.doculect:
    for j in part.doculect:
        if i == j:
            language_pair.update(
                {
                    (i, j): {
                        "autoid_dist": 0,
                        "strictid_dist": 0,
                        "looseid_dist": 0,
                        "lumpid_dist": 0,
                        "splitid_dist": 0,
                    }
                }
            )
        else:
            language_pair.update(
                {
                    (i, j): {
                        "autoid_dist": lexi_dist(part, concept_list, "autoid", i, j),
                        "strictid_dist": lexi_dist(
                            part, concept_list, "strictid", i, j
                        ),
                        "looseid_dist": lexi_dist(part, concept_list, "looseid", i, j),
                        "lumpid_dist": lexi_dist(part, concept_list, "lumpid", i, j),
                        "splitid_dist": lexi_dist(part, concept_list, "splitid", i, j),
                    }
                }
            )

# pickle output
pickle.dump(language_pair, open("lexidist_full", "wb"))

# output individual distance matrix, for neighbor net.
doculect_number = len(part.doculect)
for output_column in ["autoid", "strictid", "looseid", "lumpid", "splitid"]:
    with open("lexi_{0}.dst".format(output_column), "w") as f:
        f.write("\t" + str(doculect_number) + "\n")
        for i in part.doculect:
            tmp = [i]
            for j in part.doculect:
                tmp.append(str(language_pair[(i, j)][output_column + "_dist"]))
            f.write("\t".join(tmp) + "\n")
