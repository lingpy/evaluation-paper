"""
Step 3: This step calculates lexicostatistical distances between language pairs.

Input:
Fetch data from lexibank_liusinitic.

Output:
File output: 
    result/part_*.tre (trees from the subset of data. The subset is drawn by the ranks from step 2. )
    result/full_*.tre (trees from the post processed full dataset. The one downloaded from step 1.)
    result/part_*.dst (pairwise distance matrices from the subset of data. The output is in the PHYLIP formats)
    result/full_*.dst (pairwise distance matrices from post processed full dataset. The one downloaded from step 1. The output is in the PHYLIP formats)
    result/results/liusinitic.word_cognate (wordlist format)
"""
from lingpy.compare.partial import Partial
from lingpy import Wordlist
from lingpy.convert.strings import matrix2dst
from collections import defaultdict
from lingpy.algorithm.clustering import neighbor
from lingpy.convert.strings import write_nexus

from pkg.code import (
    get_liusinitic,
    common_morpheme_cognates,
    salient_cognates,
    compare_cognate_sets,
    lexical_distances,
    get_revised_taxon_names,
    results_path
)

part = get_liusinitic(Partial, add_cognateset_ids=True)


# Rename taxon
languages = get_revised_taxon_names()
taxa = [languages[t] for t in part.cols]

# Add new cognate sets: common, salient, loose, strict
common_morpheme_cognates(part, ref="cogids", cognates="commonid", override=True)
salient_cognates(
    part, ref="cogids", cognates="salientid", morphemes="morphemes", override=True
)

# An array with all the name of all the full cognate sets.
cognate_sets = ["strict", "loose", "common", "salient"]

# Get ranks of concepts
ranks = compare_cognate_sets(part, "strictid", "looseid")
target_concepts = [row[0] for row in ranks if row[-1] <= 0.8]

# Standard output as report
print(
    "{0} concepts are selected for computing distance matrices (threshold is 0.8).".format(
        len(target_concepts)
    )
)

# compute the distance matrices
all_trees = open(results_path("all_trees.tre"), "w")

# Compute the distance matrices
for cognate in cognate_sets:
    print("[i] computing phylogenetic trees for "+cognate)
    key = cognate + "_dist"
    matrixP = lexical_distances(part, target_concepts, ref=cognate + "id")
    matrixF = lexical_distances(part, part.rows, ref=cognate + "id")
    treeP = neighbor(matrixP, taxa, distances=True)
    treeF = neighbor(matrixF, taxa, distances=True)
    matrix2dst(
        matrixP,
        taxa=taxa,
        filename=results_path("part_{0}".format(cognate)).as_posix(),
        taxlen=10,
    )
    matrix2dst(
        matrixF,
        taxa=taxa,
        filename=results_path("full_{0}".format(cognate)).as_posix(),
        taxlen=10,
    )
    with open(results_path("part_"+cognate+".tre"), "w") as f:
        f.write(str(treeP))
    with open(results_path("full_"+cognate+".tre"), "w") as f:
        f.write(str(treeF))
    all_trees.write("{0}\n{1}\n".format(
        str(treeP),
        str(treeF)))
all_trees.close()

part.output(
    "tsv", filename=results_path("liusinitic.word_cognate").as_posix(), prettify=False, ignore="all"
)




