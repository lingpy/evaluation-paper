import pickle
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.cluster import hierarchy
from scipy.cluster.hierarchy import linkage, average, dendrogram

# create (1) the differences between two ways of calculation. (2) a pure heatmap with one way of calculation.
def create_ndarray(dict_obj, label, col1, col2):
    tmp_matrix = []
    group_label = []
    if col1 != col2:
        for m in label:
            tmp_array = []
            for n in label:
                tmp_array.append(dict_obj[(m, n)][col1] - dict_obj[(m, n)][col2])
                group_label.append((m, n))
            tmp_matrix.append(tmp_array)
    else:
        for m in label:
            tmp_array = []
            for n in label:
                tmp_array.append(dict_obj[(m, n)][col1])
                group_label.append((m, n))
            tmp_matrix.append(tmp_array)
    return tmp_matrix, group_label


def create_plot(ndarray, label, fname):
    plt.figure(figsize=(14, 12))
    ax = sns.heatmap(
        ndarray, xticklabels=label, yticklabels=label, cmap="RdBu", vmin=-0.5, vmax=0.5
    )
    ax.invert_yaxis()
    ax.figure.savefig(fname + ".png")


# load data
all_dist = pickle.load(open("lexidist_full", "rb"))

# set up an name list
label = []
for k in all_dist.keys():
    label.append(k[0])
label = set(label)

label_array = [x for x in label]

# transforming and plotting
d_auto, d_auto_label = create_ndarray(all_dist, label, "autoid_dist", "autoid_dist")
d_auto_strict, d_auto_strict_label = create_ndarray(
    all_dist, label, "autoid_dist", "strictid_dist"
)
d_auto_loose, d_auto_loose_label = create_ndarray(
    all_dist, label, "autoid_dist", "looseid_dist"
)
d_loose, d_loose_label = create_ndarray(all_dist, label, "looseid_dist", "looseid_dist")
d_loose_auto, d_loose_auto_label = create_ndarray(
    all_dist, label, "looseid_dist", "autoid_dist"
)
d_loose_strict, d_loose_strict_label = create_ndarray(
    all_dist, label, "looseid_dist", "strictid_dist"
)
d_strict, d_strict_label = create_ndarray(
    all_dist, label, "strictid_dist", "strictid_dist"
)
d_strict_loose, d_strict_loose_label = create_ndarray(
    all_dist, label, "strictid_dist", "looseid_dist"
)
d_strict_auto, d_strict_auto_label = create_ndarray(
    all_dist, label, "strictid_dist", "autoid_dist"
)

# heatmap plotting
plt.clf()
for p, p_name in [
    (d_auto, "auto"),
    (d_auto_strict, "auto_strict"),
    (d_auto_loose, "auto_loose"),
    (d_loose, "loose"),
    (d_loose_auto, "loose_auto"),
    (d_loose_strict, "loose_strict"),
    (d_strict, "strict"),
    (d_strict_loose, "strict_loose"),
    (d_strict_auto, "strict_auto"),
]:
    plt.clf()
    create_plot(p, label, p_name + "_heatmap")

# upgma tree
plt.clf()
for p, p_name in [
    (d_auto, "auto"),
    (d_loose, "loose"),
    (d_strict, "strict"),
]:
    z = linkage(p, "average")
    fig = plt.figure(figsize=(12, 12))
    plt.box(False)
    dn = dendrogram(
        z,
        orientation="left",
        count_sort="descending",
        labels=label_array,
        leaf_font_size=13,
        link_color_func=lambda x: "black",
    )
    fig.savefig(p_name + "_dendro")
    plt.clf()
