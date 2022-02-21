"""
Step 3: Computing Cross-Semantic Cognate Statistics. 

Input (2 ways):
1. Directly fetch data from lexibank_liusinitic.
2. Use the one fetch from EDICTOR (see step 1). Eg. liusinitic_20211230.tsv

To fetch from lexibank_liusinitic, one should replace line 20 with the following commandline:
wl = get_liusinitic()


Output:
1. File output: result/cross-semantic-cognate-statistics.tsv
2. Standard output: concept, Chinese characters, and the cross-semantic cognate scores. 

"""
from lingpy import Wordlist
from pkg.code import cross_semantic_cognate_statistics, get_liusinitic, get_chinese_map

wl = Wordlist("liusinitic_20211230.tsv")

# remove ignore and loanwords.
D = {0: wl.columns}
for idx in wl:
    if all(i not in wl[idx, "note"] for i in ["!b", "!i"]):
        D[idx] = wl[idx]
chinese = get_chinese_map()

wl = Wordlist(D)

chinese = get_chinese_map()

# Calculate the score of cross semantic cognate statistics
scores = cross_semantic_cognate_statistics(
    wl, ref="cogids", concept="concept", annotation="morphemes"
)


with open("results/cross-semantic-cognate-statistics.tsv", "w") as f:
    f.write("\t".join(["Concept", "Chinese", "Score", "Derivation\n"]))
    for c, colex, d in scores:
        character = chinese[c]
        f.write("\t".join([c, character, str(round(colex, 2)), d + "\n"]))
        print("{0:20}| {1:.2f}| {2:15}| {3:15}".format(c, colex, d, character))
