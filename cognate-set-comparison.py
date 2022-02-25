"""
Step 1: Compare the differences between strict and loose cognate sets per concept. This step is very important because the rest of the studies relies on the concepts' ranks (F-score) from this step.  

Input:
Fetch data from lexibank_liusinitic.

Output:
1. File output: `result/cognate-set-comparison.tsv` and `liusinitic/raw/liusinitic_ignored_IB.tsv`  
2. Standard output: concepts, Chinese character, Precision, Recall and F-score.  
"""

from lingpy.compare.partial import Partial
from pkg.code import compare_cognate_sets, get_liusinitic, get_chinese_map
from pkg.code import results_path

part = get_liusinitic(Partial, add_cognateset_ids=True)
chinese = get_chinese_map()

ranks = compare_cognate_sets(part, "strictid", "looseid")

with open(results_path("cognate-set-comparison.tsv"), "w") as f:
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
