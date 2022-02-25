"""
Cognate Set Comparison
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
