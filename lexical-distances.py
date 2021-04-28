"""
Step 3
This stap calculates lexicostatistical distances between language pairs.

The results:
Four pairwise distance matrices in the PHYLIP formats
"""
from lingpy.compare.partial import Partial
from lingpy.convert.strings import matrix2dst
from collections import defaultdict
from lingpy.algorithm.clustering import neighbor
from pathlib import Path

from pkg.code import (
        get_liusinitic,
        common_morpheme_cognates,
        salient_cognates,
        compare_cognate_sets,
        lexical_distances
        )

part = get_liusinitic(Partial) 

# add new cognate sets
common_morpheme_cognates(part, ref="cogids", cognates="commonid",
        override=True)
salient_cognates(part, ref="cogids", cognates="salientid",
        morphemes="morphemes", override=True)
part.add_cognate_ids("cogids", "strictid", idtype="strict", override=True)
part.add_cognate_ids("cogids", "looseid", idtype="loose", override=True)

# An array with all the name of all the full cognate sets.
cognate_sets = ["strict", "loose", "common", "salient"]

ranks = compare_cognate_sets(part, "strictid", "looseid")
target_concepts = [row[0] for row in ranks if row[-1] <= 0.8]

print("{0} concepts are selected for computing distance matrices (threshold is 0.8).".format( len(target_concepts)))

# compute the distance matrices
for cognate in cognate_sets:
    key = cognate + "_dist"
    matrixP = lexical_distances(part, target_concepts, ref=cognate+"id")
    matrixF = lexical_distances(part, part.rows, ref=cognate+"id")
    treeP = neighbor(matrixP, part.taxa, distances=True)
    treeF = neighbor(matrixF, part.taxa, distances=True)
    matrix2dst(
            matrixP,
            taxa=part.cols, filename=Path("results",
                "part_{0}".format(cognate)).as_posix(),
            taxlen=10
            )
    matrix2dst(
            matrixF,
            taxa=part.cols, filename=Path("results",
                "full_{0}".format(cognate)).as_posix(),
            taxlen=10
            )
    with open(Path('results', "part_"+cognate+'.tre'), 'w') as f:
            f.write(str(treeP))
    with open(Path('results', "part_"+cognate+'.tre'), 'w') as f:
            f.write(str(treeF))

part.output(
    "tsv", filename="results/liusinitic.word_cognate", prettify=False,
    ignore="all")
