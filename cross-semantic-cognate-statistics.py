"""
Computing Cross-Semantic Cognate Statistics (Workflow 2)
"""

from pkg.code import cross_semantic_cognate_statistics, get_liusinitic, get_chinese_map

wl = get_liusinitic()
chinese = get_chinese_map()

# Calculate the score of cross semantic cognate statistics
scores = cross_semantic_cognate_statistics(
    wl, ref="cogids", concept="concept", annotation="morphemes"
)


with open("results/cross-semantic-cognate-statistics.tsv", "w") as f:
    f.write("\t".join(["Concept", "Score", "Derivation", "Chinese\n"]))
    for c, colex, d in scores:
        character = chinese[c]
        f.write("\t".join([c, character, str(round(colex, 2)), d + "\n"]))
        print("{0:20}| {1:.2f}| {2:15}| {3:15}".format(c, colex, d, character))
