"""
Stage 4:
Correlation, Mantel test, and neighbor-join tree

The results of correlation and mantel test are standard outputs. 
The outputs of neighbor-join trees are 
"""
import csv
import numpy as np
import itertools
from scipy import stats
from skbio import DistanceMatrix
from skbio.stats.distance import mantel
from tabulate import tabulate
from itertools import combinations
from lingpy import *
import sys, subprocess, glob
from sys import argv

# Correlation
Concepts = {}
with open("bcube_concepts.tsv", "r") as file:
    for a in csv.DictReader(file, delimiter="\t"):
        Concepts[a["Concept"]] = {
            "Precision": a["Precision"],
            "Recall": a["Recall"],
            "F-Score": a["F-score"],
        }
file.close()

with open("colexification_concepts.tsv", "r") as file:
    for b in csv.DictReader(file, delimiter="\t"):
        Concepts[b["Concept"]].update({"Colexification": b["colexification"]})

# correlation between F-Score and colexification
Fscore, Precision, Recall, Colexification = [], [], [], []
for key, value in Concepts.items():
    Fscore.append(value["F-Score"])
    Precision.append(value["Precision"])
    Recall.append(value["Recall"])
    Colexification.append(value["Colexification"])

tau, p_value = stats.kendalltau(Fscore, Colexification)
print("\nF-score v.s. Colexification: {0} (p-value: {1})\n".format(tau, p_value))

# Mantel
files = [
    "lexi_greedid.dst",
    "lexi_looseid.dst",
    "lexi_strictid.dst",
    "lexi_salientid.dst",
]
files_variable = ["greedid", "looseid", "strictid", "salientid"]
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

table = []
tree_dict = {}
for a, b in itertools.combinations(matrix_dict.keys(), 2):
    label_a = matrix_doculect[a]
    label_b = matrix_doculect[b]
    dm_a = DistanceMatrix(matrix_dict[a], label_a)
    dm_b = DistanceMatrix(matrix_dict[b], label_b)
    # check if label a and label b are in the same order and quantity
    checking = [x for idx, x in enumerate(label_a) if x != label_b[idx]]
    if checking != []:
        break
    else:
        coeff, p_value, n = mantel(dm_a, dm_b, method="pearson", permutations=999)
        table += [[a, b, coeff, p_value]]
    # make tree
    if a not in tree_dict.keys():
        tree_dict[a] = neighbor(matrix_dict[a], label_a)
    elif b not in tree_dict.keys():
        tree_dict[b] = neighbor(matrix_dict[b], label_b)

print("Mantel test:")
print(
    tabulate(
        table, floatfmt=".4f", headers=["cogid_A", "cogid_B", "mantel coeff", "p-value"]
    )
)

# Calculate the similarity between two trees via generalized Robinson-Foulds Distance
print("\nsimilarity between two trees (generalized Robinson-Foulds Distance, GRF):")
rgf_similarity = []
for tA, tB in combinations(list(tree_dict), r=2):
    treeA, treeB = Tree(str(tree_dict[tA])), Tree(str(tree_dict[tB]))
    rgf_similarity.append([tA, tB, treeA.get_distance(treeB)])

print(
    tabulate(
        rgf_similarity,
        floatfmt=".4f",
        headers=["cogid_A", "cogid_B", "GRF distance"],
    )
)

"""
 Calculate the similarity between two trees via Quartet distance. 
 The QDist is now replaced by tqDist, users need to install tqDist. 
 More detail about general quartet distance: 
    Taraka Rama and Johann-Mattis List (2019). An automated framework for fast cognate detection and Bayesian phylogenetic inference in computational historical linguistics. ACL 

This section is inspired by gqd.py in AutoCogPhylo (https://github.com/PhyloStar/AutoCogPhylo/blob/master/gqd.py)
"""
if "--general_quartet_dist" in argv:
    print("\nsimilarity between two trees (General Quartet Distance, GQD)")
    gqd_similarity = []
    for tA, tB in combinations(list(tree_dict), r=2):
        qd = subprocess.check_output(
            ["quartet_dist", "-v", tA + ".nex", tB + ".nex"]
        )  # execute tqDist tool
        qd_array = (
            str(qd).replace("\\n", "").replace("b'", "").split("\\t")
        )  # bite-like object to string and then to array
        gqd = float(qd_array[4]) / float(qd_array[2])  # general quartet distance
        gqd_similarity.append([tA, tB, gqd])
    # output
    print(
        tabulate(
            gqd_similarity,
            floatfmt=".4f",
            headers=["cogid_A", "cogid_B", "GQD distance"],
        )
    )
