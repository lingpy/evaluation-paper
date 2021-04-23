"""
Step 4
Five different statistical analyses.

The five different statistical analyses are: 
 - Kendall tau correlation
 - Mantel test
 - Neighbor-joining tree
 - Generalized Robinson-Foulds Distance
 - Normalized Quartet Distance (optional)

 The results: 
 1. Four Newick files
 2. A screen output
"""
from csvw.dsv import UnicodeDictReader
import numpy as np
import itertools
from scipy import stats
from skbio import DistanceMatrix
from skbio.stats.distance import mantel
from tabulate import tabulate
from itertools import combinations
from lingpy import *
from lingpy.read.phylip import *
import sys, subprocess, glob
from sys import argv

# Correlation
concepts = {}
with UnicodeDictReader("results/cognate-set-comparison.tsv", delimiter="\t") as reader:
    concepts = {row["Concept"]: row for row in reader}

with UnicodeDictReader(
    "results/cross-semantic-cognate-statistics.tsv", delimiter="\t"
) as reader:
    for row in reader:
        concepts[row["Concept"]].update({"Cognates": row["Score"]})

# Correlation between cognate set comaprison and cross-semantic score
fscores, precisions, recalls, cognates = [], [], [], []
for row, d in concepts.items():
    for lst, key in [
        (fscores, "F-Score"),
        (precisions, "Precision"),
        (recalls, "Recall"),
        (cognates, "Cognates"),
    ]:
        lst += [d[key]]

tau, p_value = stats.kendalltau(fscores, cognates)
print("\nF-score v.s. Scores: {0} (P-value: {1})\n".format(tau, p_value))

# Mantel test
files = [
    "lexi_commonid.dst",
    "lexi_looseid.dst",
    "lexi_strictid.dst",
    "lexi_salientid.dst",
]
files_variable = ["commonid", "looseid", "strictid", "salientid"]
matrix_doculect, matrix = {}, {}
for f, v in zip(files, files_variable):
    matrix_doculect[v], matrix[v] = read_dst(
        "results/" + f
    )  # Function from lingpy.read.phylip

table = []
tree_dict = {}
for a, b in itertools.combinations(matrix.keys(), 2):
    label_a = matrix_doculect[a]
    label_b = matrix_doculect[b]
    dm_a = DistanceMatrix(matrix[a], label_a)
    dm_b = DistanceMatrix(matrix[b], label_b)
    # Check if label a and label b are in the same order and quantity
    checking = [x for idx, x in enumerate(label_a) if x != label_b[idx]]
    if checking != []:
        break
    else:
        coeff, p_value, n = mantel(dm_a, dm_b, method="pearson", permutations=999)
        table += [[a, b, coeff, p_value]]
    # Build a Neighbor-joining tree
    if a not in tree_dict.keys():
        tree_dict[a] = neighbor(matrix[a], label_a)
        print(
            tree_dict[a], file=open("".join(["results/", a, ".nwk"]), "w")
        )  # Print to file
    elif b not in tree_dict.keys():
        tree_dict[b] = neighbor(matrix[b], label_b)
        print(
            tree_dict[b], file=open("".join(["results/", b, ".nwk"]), "w")
        )  # Print to file

print("Mantel test:")
print(
    tabulate(
        table, floatfmt=".4f", headers=["Cogid A", "Cogid B", "Mantel coeff", "P-value"]
    )
)

# Calculate the similarity between two trees via generalized Robinson-Foulds Distance
print("\nSimilarity between two trees (Generalized Robinson-Foulds Distance, GRF):")
rgf_similarity = []
for tA, tB in combinations(list(tree_dict), r=2):
    treeA, treeB = Tree(str(tree_dict[tA])), Tree(str(tree_dict[tB]))
    rgf_similarity.append([tA, tB, treeA.get_distance(treeB)])

print(
    tabulate(
        rgf_similarity,
        floatfmt=".4f",
        headers=["Cogid A", "Cogid B", "GRF distance"],
    )
)

if "--nqd" in argv:
    """
    Calculate the similarity between two trees via Normalized Quartet Distance (NQD).
    The QDist is now replaced by tqDist, please install tqDist before using this function.

    This section is inspired by gqd.py in AutoCogPhylo (https://github.com/PhyloStar/AutoCogPhylo/blob/master/gqd.py)
    Becuase we are comparing two binary trees, we do not need Generalized Quartet Distance as written in the AutoCogPhylo.
    """

    print("\nSimilarity between two binary trees (Normalized Quartet Distance, NQD)")
    nqd_similarity = []
    for tA, tB in combinations(list(tree_dict), r=2):
        tA_file = "".join(["results/", tA, ".nwk"])
        tB_file = "".join(["results/", tB, ".nwk"])
        qd = subprocess.check_output(
            ["quartet_dist", "-v", tA_file, tB_file]
        )  # Execute tqDist tool
        qd_array = (
            str(qd).replace("\\n", "").replace("b'", "").split("\\t")
        )  # Bite-like object to a string, and then to an array.
        nqd = float(qd_array[3])  # Normalized Quartet Distance
        nqd_similarity.append([tA, tB, nqd])

    # Output
    print(
        tabulate(
            nqd_similarity,
            floatfmt=".4f",
            headers=["Cogid A", "Cogid B", "NQD Distance"],
        )
    )
