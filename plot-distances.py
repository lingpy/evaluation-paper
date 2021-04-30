"""
Compute heatmaps from the lexical distances.
"""
from lingpy import *
from pathlib import Path
from lingpy.convert.plot import plot_heatmap
from lingpy.compare.partial import Partial
from itertools import combinations, product
import matplotlib.colors as colors
import matplotlib.pyplot as plt
from pkg.code import get_liusinitic, get_ordered_taxa, get_revised_taxon_names


part = get_liusinitic()
tree, taxa = get_ordered_taxa()
labels = get_revised_taxon_names()

# cognate conversion methods
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
