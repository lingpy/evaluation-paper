"""
Computing Cross-Semantic Cognate Statistics

Step 2 of the workflow creates file
`result/cross-semantic-cognate-statistics.tsv` and prints results to the
terminal.
"""

from pkg.code import get_liusinitic, get_chinese_map, results_path
from lingrex.evaluate import cross_semantic_cognate_statistics
from tabulate import tabulate

# get the wordlist
wordlist = get_liusinitic()

# get a reference to Chinese characters
chinese = get_chinese_map()

# calculate cross semantic cognate statistics
scores = cross_semantic_cognate_statistics(
    wordlist, ref="cogids", concept="concept", morpheme_glosses="morphemes",
    ignore_affixes=True)

table = []
with open(results_path("cross-semantic-cognate-statistics.tsv"), "w") as f:
    f.write("\t".join(["Concept", "Chinese", "Score", "Derivation\n"]))
    for c, colex in scores:
        character = chinese[c]
        f.write("\t".join([c, character, "{0:.2f}".format(colex)]) + "\n")
        table += [[
            c, 
            character,
            "{0:.2f}".format(colex)]] 
print(tabulate(table, headers=["Concept", "Chinese", "Score"], tablefmt="simple"))

