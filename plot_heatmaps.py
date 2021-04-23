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


plot_heatmap(part, tree=tree, matrix=matrixS, filename="plot/strict", cmap=plt.cm.RdBu)
plot_heatmap(part, tree=tree, matrix=matrixL, filename="plot/loose", cmap=plt.cm.RdBu)
plot_heatmap(
    part, tree=tree, matrix=matrixD, filename="plot/difference", vmax=0.3, cmap=plt.cm.RdBu
)
# from lingpy import *
# from lingpy.read.phylip import *
# from itertools import combinations
# import numpy as np
# import matplotlib
# import matplotlib.pyplot as plt
# import seaborn as sns
# import itertools
# from scipy.cluster import hierarchy
# from scipy.cluster.hierarchy import linkage, average, dendrogram
# from tabulate import tabulate


# def reorder(ndarray, label, reference_array):
#     """
#     Reorder a given matrix according to a reference array.
#     """
#     tmp = [
#         [0 for cell in range(len(reference_array))]
#         for row in range(len(reference_array))
#     ]
#     for (i, langA), (j, langB) in combinations(enumerate(reference_array), r=2):
#         cell_value = ndarray[label.index(langA)][label.index(langB)]
#         tmp[i][j] = tmp[j][i] = cell_value
#     return tmp


# def create_plot(ndarray, label, fname):
#     """
#     Load matrix to draw a heatmap
#     """

#     plt.figure(figsize=(14, 14))
#     ax = sns.heatmap(
#         ndarray,
#         xticklabels=label,
#         yticklabels=label,
#         cmap="RdBu",
#         vmin=-0.5,
#         vmax=0.5,
#     )
#     ax.invert_yaxis()
#     sns.set(font_scale=2)
#     plt.tight_layout()
#     ax.figure.savefig(fname + ".pdf")


# # Load data
# files = [
#     "lexi_commonid.dst",
#     "lexi_looseid.dst",
#     "lexi_strictid.dst",
#     "lexi_salientid.dst",
# ]
# files_variable = ["commonid", "looseid", "strictid", "salientid"]
# matrix_doculect, matrix = {}, {}
# for f, v in zip(files, files_variable):
#     matrix_doculect[v], matrix[v] = read_dst(
#         "results/" + f
#     )  # Function from lingpy.read.phylip


# """
# Reorder the matrix's arrangement based on expert's subgroups.

# The detail of the groupings please see the article:
#       List, Johann-Mattis. “Network Perspectives on Chinese Dialect History.” Bulletin of Chinese linguistics 8 (2015): 27-47.

# Except the above reference, we also consult expert's suggestion and Glottolog about the arrangment of Jin, Pinghua and Hui language varieties
# """
# # taxa_list = Tree(tree='parsimony.tre') #getting a list from the tree, waiting for the tree.
# taxa_list = [
#     "Taiyuan",
#     "Beijing",
#     "Ha_erbin",
#     "Xi_an",
#     "Nanjing",
#     "Jinan",
#     "Rongcheng",
#     "Chengdu",
#     "Suzhou",
#     "Wenzhou",
#     "Jixi",
#     "Changsha",
#     "Loudi",
#     "Nanchang",
#     "Meixian",
#     "Guilin",
#     "Guangzhou",
#     "Fuzhou",
#     "Xiamen",
# ]


# """
# Create Heatmaps according to the reference list.
# The "heat" (red and blue) is limited to the range between -0.5 and 0.5
# """
# for a, b in combinations(matrix.keys(), r=2):
#     # Output filename
#     filename = a + "_" + b
#     filename_opposite = b + "_" + a
#     # Re-order
#     matrix_A = np.vstack(reorder(matrix[a], matrix_doculect[a], taxa_list))
#     matrix_B = np.vstack(reorder(matrix[b], matrix_doculect[b], taxa_list))
#     intersect = matrix_A - matrix_B
#     intersect_opposite = matrix_B - matrix_A
#     # Plot
#     create_plot(intersect, taxa_list, "plot/" + "heatmap_" + filename)
#     plt.clf()
#     create_plot(intersect_opposite, taxa_list, "plot/" + "heatmap_" + filename_opposite)
#     plt.clf()
#     create_plot(matrix_A, taxa_list, "plot/" + "heatmap_" + a)
#     plt.clf()
#     create_plot(matrix_B, taxa_list, "plot/" + "heatmap_" + b)
