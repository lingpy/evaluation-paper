"""
Analyze the Lexical Distances

This is step five of our workflow. Results from the comparison are written to
the terminal.
"""
from csvw.dsv import UnicodeDictReader
import numpy as np
import itertools
from scipy import stats
from skbio import DistanceMatrix
from skbio.stats.distance import mantel
from tabulate import tabulate
from lingpy import *
from lingpy.read.phylip import *

from pkg.code import (
    get_liusinitic,
    get_ordered_taxa,
    results_path,
    get_revised_taxon_names
)


# Generate dictionary. Key = concepts, Values = nested dictionary {Cognates: scores}
concepts = {}
with UnicodeDictReader(results_path("cognate-set-comparison.tsv"), delimiter="\t") as reader:
    concepts = {row["Concept"]: row for row in reader}

with UnicodeDictReader(
    results_path("cross-semantic-cognate-statistics.tsv"), delimiter="\t"
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


for pref in ["full", "part"]:
    cognate_sets = ["common", "loose", "strict", "salient"]
    matrix_doculect, matrix = {}, {}
    for c in cognate_sets:
        matrix_doculect[c], matrix[c] = read_dst(
            str(results_path(pref+"_" + c + ".dst"))
        )
    
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
    
    print("# Mantel Tests ({0})\n".format(pref))
    print(
        tabulate(
            table, floatfmt=".4f", headers=["Cogid A", "Cogid B", "Mantel coeff", "P-value"]
        )
    )
    print("")


