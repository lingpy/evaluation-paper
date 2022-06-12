"""
Compare Strict and Loose Cognate Sets in the Data.

This is the first step of our workflow. It writes results to the file
`result/cognate-set-comparison.tsv`. 
"""

from lingrex.evaluate import compare_cognate_sets
from collections import defaultdict
from pkg.code import get_liusinitic, results_path, get_chinese_map
from tabulate import tabulate

# get the wordlist
wordlist = get_liusinitic()

# get a reference to Chinese characters
chinese = get_chinese_map()

# compute the ranks
ranks = compare_cognate_sets(wordlist, "strictid", "looseid")

table = []
with open(results_path("cognate-set-comparison.tsv"), "w") as f:
    f.write("\t".join(["Concept", "Character", "Precision", "Recall", "F-Score\n"]))
    for concept, p, r, fs in sorted(ranks, key=lambda x: x[-1]):
        table += [[
            concept,
            chinese[concept],
            "{0:.2f}".format(p),
            "{0:.2f}".format(r),
            "{0:.2f}".format(fs)]]

        f.write(
            "\t".join(
                [
                    concept,
                    chinese[concept],
                    "{0:.2f}".format(p),
                    "{0:.2f}".format(r),
                    "{0:.2f}".format(fs)
                 ]
            )+"\n"
        )
print(tabulate(table, 
    headers=["Concept", "Chinese", "Precision", "Recall", "F-Score"]))
