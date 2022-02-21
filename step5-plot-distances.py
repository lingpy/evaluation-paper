"""
Step 5: Compute heatmaps from the lexical distances.

Input (2 ways):
1. Directly fetch data from lexibank_liusinitic.
2. Use the one from step 2. Eg. liusinitic_20211230_ignored_IB.tsv

To fetch from lexibank_liusinitic, one should replace line 26 with the following commandline:
part = get_liusinitic()

Output:
File output: 
    plots/loose.pdf
    plots/strict.pdf
    plots/difference.pdf

"""
from lingpy import *
from pathlib import Path
from lingpy.convert.plot import plot_heatmap
from lingpy.compare.partial import Partial
from itertools import combinations, product
import matplotlib.colors as colors
import matplotlib.pyplot as plt
from pkg.code import  compare_cognate_sets, get_liusinitic, get_ordered_taxa, get_revised_taxon_names


part = Partial("liusinitic_20211230_ignored_IB.tsv")
# Get the reference tree 
tree, taxa = get_ordered_taxa()
# Beautiful labels
labels = get_revised_taxon_names()

# Compute ranks
ranks = compare_cognate_sets(part, "strictid", "looseid")
target_concepts = [row[0] for row in ranks if row[-1] <= 0.8]

# Compute loose and strict pairwise distances and the delta (loose - strict)
matrixS, matrixL = [[1 for t in taxa] for t in taxa], [[1 for t in taxa] for t in taxa]
matrixD = [[0 for t in taxa] for t in taxa]
for (i, tA), (j, tB) in combinations(enumerate(taxa), r=2):
    cogsA = part.get_dict(col=tA, entry="cogids")
    cogsB = part.get_dict(col=tB, entry="cogids")
    strict, loose = [], []
    for concept in part.rows:
        match_l, match_s = [], []
        if concept in cogsA and concept in cogsB:
            for cogA, cogB in product(cogsA[concept], cogsB[concept]):
                if set(cogA).intersection(set(cogB)):
                    match_l += [1]
                if cogA == cogB:
                    match_s += [1]
            if match_l:
                loose += [1]
            else:
                loose += [0]
            if match_s:
                strict += [1]
            else:
                strict += [0]
    matrixS[i][j] = matrixS[j][i] = sum(strict) / len(strict)
    matrixL[i][j] = matrixL[j][i] = sum(loose) / len(loose)
    matrixD[i][j] = matrixD[j][i] = sum(loose) / len(loose) - sum(strict) / len(strict)

# plot 3 heatmaps
plot_heatmap(
    part,
    tree=tree,
    matrix=matrixS,
    filename=Path("plots", "strict").as_posix(),
    cmap=plt.cm.RdBu,
    left=0.09,
    textsize=6.5,
    figsize=(8.4, 4.5),
    labels=labels,
    width=0.85,    
)
plot_heatmap(
    part,
    tree=tree,
    matrix=matrixL,
    filename=Path("plots", "loose").as_posix(),
    cmap=plt.cm.RdBu,
    left=0.09,
    textsize=6.5,
    figsize=(8.4, 4.5),
    labels=labels,
    width=0.85,
)
plot_heatmap(
    part,
    tree=tree,
    matrix=matrixD,
    filename=Path("plots", "difference").as_posix(),
    vmax=0.3,
    cmap=plt.cm.RdBu,
    left=0.09,
    textsize=6.5,
    width=0.85,
    colorbar_label="Delta Values",
    figsize=(8.4, 4.5),
    labels=labels,
)
