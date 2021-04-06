"""
Step 1 
Calculate the agreements between two types of 
cognate coversion methods via B-Cube scores.

The results:
1. A standard output. The rankings are sorted according to the F-score.
2. A TSV file
"""
from lingpy.evaluate.acd import _get_bcubed_score as bcs
from lingpy import Wordlist
from lingpy.compare.partial import Partial
from lexibank_liusinitic import Dataset as LS

# Load data
part = Partial(LS().raw_dir.joinpath('liusinitic.tsv').as_posix())

# Check if strictid and looseid are in the data.
if "strictid" not in part.columns:
    part.add_cognate_ids(
        "cogids", "strictid", idtype="strict"
    )  # Add strictid if missing
elif "looseid" not in part.columns:
    part.add_cognate_ids("cogids", "looseid", idtype="loose")  # Add looseid if missing

wordlist = Wordlist(part)

# A dict object for concepts v.s. Chinese characters.
chinese = {}
for idx, concept, character in wordlist.iter_rows("concept", "characters"):
    character = character.replace(" ", "")
    if concept in chinese.keys():
        if character not in chinese.get(concept):
            if len(chinese.get(concept)) <= 2:
                # Take maximum three Chinese compound words as examples
                chinese[concept].append(character)
    else:
        chinese[concept] = [character]

# Calculate the rank
ranks = []
for concept in wordlist.rows:
    idxs = wordlist.get_list(row=concept, flat=True)
    cogsA = [wordlist[idx, "strictid"] for idx in idxs]
    cogsB = [wordlist[idx, "looseid"] for idx in idxs]
    p, r = bcs(cogsA, cogsB), bcs(cogsB, cogsA)
    f = 2 * (p * r) / (p + r)
    character = chinese[concept]  # Check with chinese dictionary object.
    ranks += [[concept, ",".join(character), p, r, f]]

# Output
with open("results/cognate-set-comparison.tsv", "w") as f:
    f.write(
        "\t".join(["Concept", "Character", "Precision", "Recall", "F-Score\n"])
    )  # File header
    for concept, character, p, r, fs in sorted(ranks, key=lambda x: x[-1]):
        print(
            "{0:20}| {1:.2f} | {2:.2f} | {3:.2f} | {4:10}".format(
                concept, p, r, fs, character
            )
        )  # Standard output
        f.write(
            "\t".join(
                [
                    concept,
                    character,
                    str(round(p, 2)),
                    str(round(r, 2)),
                    str(round(fs, 2)) + "\n",
                ]
            )
        )  # File output to results/

