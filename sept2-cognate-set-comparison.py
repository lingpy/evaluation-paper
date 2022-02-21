"""
Step 2: Compare the differences between strict and loose cognate sets per concept. This step is very important because the rest of the studies relies on the concepts' ranks (F-score) from this step.  

Input (2 ways):
1. Directly fetch data from lexibank_liusinitic.
2. Use the one fetch from EDICTOR (see step 1). Eg. liusinitic_20211230.tsv

To fetch from lexibank_liusinitic, one should replace line 20 with the following commandline:
part = get_liusinitic(Partial)


Output:
1. File output: `result/cognate-set-comparison.tsv` and `liusinitic_20211230_ignored_IB.tsv`  
2. Standard output: concepts, Chinese character, Precision, Recall and F-score.  

"""
from lingpy.compare.partial import Partial
from pkg.code import compare_cognate_sets, get_liusinitic, get_chinese_map

part = Partial("liusinitic_20211230.tsv")
# remove !i (lexical entries that should be ignored) and !b (loanwords) 
D = {0: part.columns}
for idx in part:
    if all(i not in part[idx, "note"] for i in ["!b", "!i"]):
        D[idx] = part[idx]
chinese = get_chinese_map()

part = Partial(D)

# calculate the strict and loose cognate sets in case that the strict and loose cognates are not existing in the dataset. 
for conversion in ["strict", "loose"]:
    part.add_cognate_ids("cogids", conversion + "id", idtype=conversion, override=True)

ranks = compare_cognate_sets(part, "strictid", "looseid")

with open("results/cognate-set-comparison.tsv", "w") as f:
    f.write("\t".join(["Concept", "Character", "Precision", "Recall", "F-Score\n"]))
    for concept, p, r, fs in sorted(ranks, key=lambda x: x[-1]):
        print(
            "{0:20}| {1:.2f} | {2:.2f} | {3:.2f} | {4:10}".format(
                concept, p, r, fs, chinese[concept]
            )
        )
        f.write(
            "\t".join(
                [
                    concept,
                    chinese[concept],
                    str(round(p, 2)),
                    str(round(r, 2)),
                    str(round(fs, 2)) + "\n",
                ]
            )
        )

part.output("tsv", filename="liusinitic_20211230_ignored_IB.tsv")