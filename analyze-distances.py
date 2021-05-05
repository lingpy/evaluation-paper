"""
Analyze the distance measures.
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
from pathlib import Path

from pkg.code import (
    compare_cognate_sets,
    get_liusinitic,
    cross_semantic_cognate_statistics,
    get_ordered_taxa,
    get_revised_taxon_names
)


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
print("# Cognate Set Comparisons vs. Cross-Semantic Cognates\n")
print("{0:4f} (P-value: {1:4f})".format(tau, p_value))
print("")

cognate_sets = ["common", "loose", "strict", "salient"]
matrix_doculect, matrix, tree_dict = {}, {}, {}
for c in cognate_sets:
    matrix_doculect[c], matrix[c] = read_dst(
        Path("results", "part_" + c + ".dst").as_posix()
    )
    tree_dict[c] = open(Path("results", "part_" + c + ".tre").as_posix()).read().strip()

table = []
for a, b in itertools.combinations(matrix, 2):
    label_a = matrix_doculect[a]
    label_b = matrix_doculect[b]
    dm_a = DistanceMatrix(matrix[a], label_a)
    dm_b = DistanceMatrix(matrix[b], label_b)

    checking = [x for idx, x in enumerate(label_a) if x != label_b[idx]]
    if checking != []:
        break
    else:
        coeff, p_value, n = mantel(dm_a, dm_b, method="pearson", permutations=999)
        table += [[a, b, coeff, p_value]]

print("# Mantel Tests\n")
print(
    tabulate(
        table, floatfmt=".4f", headers=["Cogid A", "Cogid B", "Mantel coeff", "P-value"]
    )
)

# Calculate the similarity between two trees via generalized Robinson-Foulds Distance
print("\n# Tree Similarity (Generalized Robinson-Foulds Distance)\n")
rgf_similarity = []
for tA, tB in combinations(tree_dict, r=2):
    treeA, treeB = Tree(str(tree_dict[tA])), Tree(str(tree_dict[tB]))
    rgf_similarity.append([tA, tB, treeA.get_distance(treeB)])

print(
    tabulate(
        rgf_similarity,
        floatfmt=".4f",
        headers=["Cogid A", "Cogid B", "GRF distance"],
    )
)


print(
    tabulate(
        reference_similarity,
        floatfmt=".4f",
        headers=["Cognates", "GRF distance"],
    )
)


if "--nqd" in argv:
    """
    Calculate the similarity between two trees via Normalized Quartet Distance (NQD).
    The QDist is now replaced by tqDist, please install tqDist before using this function.

    This section is inspired by gqd.py in AutoCogPhylo (https://github.com/PhyloStar/AutoCogPhylo/blob/master/gqd.py)
    Becuase we are comparing two binary trees, we do not need Generalized Quartet Distance as written in the AutoCogPhylo.
    """

    print("\n# Similarity between Trees (Normalized Quartet Distance)\n")
    nqd_similarity = []
    for tA, tB in combinations(list(tree_dict), r=2):
        tA_file = "/".join(["results", "part_" + tA + ".tre"])
        tB_file = "/".join(["results", "part_" + tB + ".tre"])
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
