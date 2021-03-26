"""
Stage 4:
heatmap and dendrogram
"""

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import itertools
from scipy.cluster import hierarchy
from scipy.cluster.hierarchy import linkage, average, dendrogram
from skbio import DistanceMatrix
from skbio.stats.distance import mantel
from tabulate import tabulate

def beauty(array):
    tmp_label=[]
    for x in array:
        if x == 'Xi_an':
            tmp_label.append("Xi'an")
        elif x == 'Ha_erbin':
            tmp_label.append("Harbin")
        else:
            tmp_label.append(x)
    return tmp_label

def create_plot(ndarray, label, fname):
    plt.figure(figsize=(14, 12))
    ax = sns.heatmap(
        ndarray,
        xticklabels=label,
        yticklabels=label,
        cmap="RdBu",
        vmin=-0.5,
        vmax=0.5,
    )
    ax.invert_yaxis()
    sns.set(font_scale=1.5)
    ax.figure.savefig(fname + ".png")


"""
load data
"""
files = ["lexi_semiid.dst", "lexi_autoid.dst", "lexi_looseid.dst", "lexi_strictid.dst"]
files_variable = ["semiid_dst","autoid_dst", "looseid_dst", "strictid_dst"]
matrix_doculect = {}
matrix_dict = {}
for i, j in zip(files, files_variable):
    with open(i, "r") as f:
        tmp = f.readlines()
        doculect = []
        tmp_matrix = []
        for ridx, row in enumerate(tmp):
            if ridx != 0:
                tmp_array = row.rstrip("\n").split("\t")
                doculect.append(tmp_array[0])
                tmp_matrix.append([float(x) for x in tmp_array[1:]])
        matrix_dict[j] = np.vstack(tmp_matrix)
        matrix_doculect[j] = doculect

"""
mantel test and heatmap
"""
plt.clf()
table = [["cogid_A", "cogid_B", "mantel coeff", "p-value"]]
for a, b in itertools.combinations(matrix_dict.keys(), 2):
    dm_a = DistanceMatrix(matrix_dict[a])
    dm_b = DistanceMatrix(matrix_dict[b])
    label_a = matrix_doculect[a]
    # for checking only
    label_b = matrix_doculect[b]
    checking = [x for idx, x in enumerate(label_a) if x != label_b[idx]]
    if checking != []:
        break
    else:
        coeff, p_value, n = mantel(
            dm_a, dm_b,
            method="pearson",
            permutations=999
            )
        table += [[a, b, coeff, p_value]]
        intersect = matrix_dict[a] - matrix_dict[b]
        intersect_opposite = matrix_dict[b] - matrix_dict[a]
        label_a = beauty(label_a)
        filename = "_".join([a.split("_")[0], b.split("_")[0], "heatmap"])
        filename_opposite = "_".join([b.split("_")[0], a.split("_")[0], "heatmap"])
        filename_diag = "_".join([a.split("_")[0], a.split("_")[0], "heatmap"])
        create_plot(intersect, label_a, filename)
        plt.clf()
        create_plot(intersect_opposite, label_a, filename_opposite)
        plt.clf()
        create_plot(matrix_dict[a], label_a, filename_diag)
        plt.clf()

# add the final diag. heatmap
create_plot(
    matrix_dict['strictid_dst'],
    matrix_doculect['strictid_dst'],
    'strictid_strictid_heatmap')
plt.clf()

print(tabulate(table, floatfmt=".4f"))

"""
Neighbor-join
"""
for a, p in matrix_dict.items():
    label = beauty(matrix_doculect[a])
    z = linkage(p, "average")
    fig = plt.figure(figsize=(12, 12))
    plt.box(False)
    dn = dendrogram(
        z,
        orientation="left",
        count_sort="descending",
        labels=label,
        leaf_font_size=30,
        link_color_func=lambda x: "black",
    )
    fig.savefig(a + "_dendro.svg", format='svg')
    plt.close()
