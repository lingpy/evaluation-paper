"""
Step 5
heatmaps
"""
from lingpy import *
from lingpy.convert.plot import plot_heatmap
from lingpy.compare.partial import Partial
from lingpy.convert.tree import nwk2tree_matrix
from lexibank_liusinitic import Dataset
from itertools import combinations, product
import matplotlib.colors as colors
import matplotlib.pyplot as plt

tree = (
    Dataset()
    .etc_dir.read_csv("trees.tsv", delimiter="\t")[1][1]
    .replace("XiAn", "Xi_an")
    .replace("Haerbin", "Ha_erbin")
)
part = Partial(Dataset().raw_dir.joinpath("liusinitic.tsv").as_posix())
taxa = nwk2tree_matrix(tree)[1]

# strict cognate conversion
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
                print(concept, tA, tB, cogA, cogB)
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


plot_heatmap(part, tree=tree, matrix=matrixS, filename="plot/strict", cmap=plt.cm.RdBu, left=0.09, textsize=6.5, figsize=(8.4,4.5))
plot_heatmap(part, tree=tree, matrix=matrixL, filename="plot/loose", cmap=plt.cm.RdBu, left=0.09, textsize=6.5, figsize=(8.4,4.5))
plot_heatmap(
    part, tree=tree, matrix=matrixD, filename="plot/difference", vmax=0.3, cmap=plt.cm.RdBu, left=0.09, textsize=6.5, colorbar_label="Delta Values",figsize=(8.4,4.5)
)