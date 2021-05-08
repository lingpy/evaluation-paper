"""
This script is designed only for the bootstrapping purpose.
"""

from lingpy.compare.partial import Partial
from lingpy.convert.strings import matrix2dst
from collections import defaultdict
from lingpy.algorithm.clustering import neighbor
from pathlib import Path
import random
from pkg.bootstrap import bootstrap, hamming_distances, splits_from_tree
from pylotree import Tree


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

cognate_sets = ["strict", "loose", "common", "salient"]

# make the matrix
for cognate in cognate_sets:
    paps = [v for k, v in sorted(part.get_paps(ref=cognate+"id").items(), key=lambda
        x: x[0])]
    matrix = hamming_distances(paps)
    tree = Tree(neighbor(matrix, part.cols))
    splits, trees = bootstrap(paps, part.cols, tree, iterations=1000)
    active_splits = splits_from_tree(tree)
    scores = []
    for (nodeA, nodeB), split in active_splits.items():
        scores += [len(splits[split])/1000]
        #print(nodeA, nodeB, len(splits[split]) / 100)
    print('{0:10} | {1:.2f}'.format(cognate, sum(scores)/len(scores)))

