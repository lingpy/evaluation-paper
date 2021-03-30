"""
Step 1: Calculate the agreements between two types of 
cognate coversion methods via Bcube scores.

The Result:
1. A standard output. The rankings are sorted according to the F-score.
2. A .tsv file
"""

from lingpy.evaluate.acd import _get_bcubed_score as bcs
from lingpy import Wordlist
from lingpy.compare.partial import Partial

# load data
part = Partial("liusinitic.tsv")

# check if strict ids and loose ids are in the data.
if "strictid" not in part.columns:
    part.add_cognate_ids("cogids", "strictid", idtype="strict")
elif "looseid" not in part.columns:
    part.add_cognate_ids("cogids", "looseid", idtype="loose")

wordlist = Wordlist(part)

# a dict object for concepts v.s. Chinese characters. Also sort the salient morpheme.
chinese = {}
for idx, concept, character in wordlist.iter_rows("concept", "characters"):
    character = character.replace(" ", "")
    if concept in chinese.keys():
        if character not in chinese.get(concept):
            if len(chinese.get(concept)) <= 2:
                # we take only maximum three Chinese compound words as example
                chinese[concept].append(character)
    else:
        chinese[concept] = [character]

# start calculating the rank
ranks = []
for concept in wordlist.rows:
    idxs = wordlist.get_list(row=concept, flat=True)
    cogsA = [wordlist[idx, "strictid"] for idx in idxs]
    cogsB = [wordlist[idx, "looseid"] for idx in idxs]
    p, r = bcs(cogsA, cogsB), bcs(cogsB, cogsA)
    f = 2 * (p * r) / (p + r)
    character = chinese[concept]  # check with chinese dict. object.
    ranks += [[concept, ",".join(character), p, r, f]]

with open("results/cognate-set-comparison.tsv", "w") as file:
    file.write(
        "\t".join(["Concept", "character", "Precision", "Recall", "F-score\n"])
    )  # file header
    for concept, character, p, r, f in sorted(ranks, key=lambda x: x[-1]):
        print(
            "{0:20}| {1:.2f} | {2:.2f} | {3:.2f} | {4:10}".format(
                concept, p, r, f, character
            )
        )  # standard output
        file.write(
            "\t".join(
                [
                    concept,
                    character,
                    str(round(p, 2)),
                    str(round(r, 2)),
                    str(round(f, 2)) + "\n",
                ]
            )
        )  # file output to results/
file.close()
