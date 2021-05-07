"""
Step Appendix
This script is designed only for the bootstrapping purpose.
"""

from lingpy.compare.partial import Partial
from lingpy.convert.strings import matrix2dst
from collections import defaultdict
from lingpy.algorithm.clustering import neighbor
from pathlib import Path
import random

from pkg.code import (
    get_liusinitic,
    common_morpheme_cognates,
    salient_cognates,
    compare_cognate_sets,
    lexical_distances,
    get_revised_taxon_names,
)

part = get_liusinitic(Partial)
languages = get_revised_taxon_names()
taxa = [languages[t] for t in part.cols]
common_morpheme_cognates(part, ref="cogids", cognates="commonid", override=True)
salient_cognates(
    part, ref="cogids", cognates="salientid", morphemes="morphemes", override=True
)
part.add_cognate_ids("cogids", "strictid", idtype="strict", override=True)
part.add_cognate_ids("cogids", "looseid", idtype="loose", override=True)

# An array with all the name of all the full cognate sets.
cognate_sets = ["strict", "loose", "common", "salient"]

ranks = compare_cognate_sets(part, "strictid", "looseid")
target_concepts = [row[0] for row in ranks]

# print(
#     "{0} concepts are selected for computing distance matrices (threshold is 0.8).".format(
#         len(target_concepts)
#     )
# )

# compute the from the random sample
for cognate in cognate_sets:
    with open(
        Path("results", "full_random_trees_" + cognate + ".tre"), "w"
    ) as random_trees:
        for i in range(0, 1000):
            random_concepts = random.sample(
                target_concepts, int(len(target_concepts) * 0.7)
            )
            key = cognate + "_dist"
            matrixP = lexical_distances(part, random_concepts, ref=cognate + "id")
            treeP = neighbor(matrixP, taxa, distances=True)
            random_trees.write("{0}\n".format(str(treeP)))
    random_trees.close()
