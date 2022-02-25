"""
Step 7: Select the data with target concepts (ranks <0.8) and output the data in pep.nex and MrBayes nex file 

Input:
Fetch data from lexibank_liusinitic.

Output:
File output: 
    nexus/*.bayes.nex (for MrBayes)
    nexus/*.paps.nex (for maximum likelihood tree/networks)
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
    nexus_path
)

part = get_liusinitic(Partial, add_cognateset_ids=True)
languages = get_revised_taxon_names()
taxa = [languages[t] for t in part.cols]

# add new cognate sets
common_morpheme_cognates(part, ref="cogids", cognates="commonid", override=True)
salient_cognates(
    part, ref="cogids", cognates="salientid", morphemes="morphemes", override=True
)

# An array with all the name of all the full cognate sets.
cognate_sets = ["strict", "loose", "common", "salient"]

ranks = compare_cognate_sets(part, "strictid", "looseid")
target_concepts = [row[0] for row in ranks if row[-1] <= 0.8]

print(
    "{0} concepts are selected for computing distance matrices (threshold is 0.8).".format(
        len(target_concepts)
    )
)

D = {0: part.columns}
for idx in part:
    if part[idx, "concepts"] in target_concepts:
        D[idx] = part[idx]
        D[idx][part.columns.index("doculect")] = languages[part[idx, "doculect"]]

wl = Wordlist(D)
for ref in ["strictid", "looseid", "commonid", "salientid"]:
    wl.output("paps.nex", filename=nexus_path(ref).as_posix(), missing="-", ref=ref)
    write_nexus(
        wl,
        ref=ref,
        filename=nexus_path(ref).as_posix(),
        commands=[
            "set autoclose=yes nowarn=yes;",
            "lset coding=noabsencesites rates=gamma;",
            "taxset MinGroup = FuzhouMin XiamenMin;",
            "constraint MinGroup 100 = FuzhouMin XiamenMin;",
            "calibrate MinGroup = gamma(2, 1.15);",
            "constraint root = 1-.;",
            "prset clockratepr=exponential(3e5);",
            "prset treeagepr = uniform(3.5, 5.5);",
            "prset sampleprob=0.2 samplestrat=random speciationpr=exp(1);",
            "prset extinctionpr=beta(1,1) nodeagepr=calibrated;",
            "prset brlenspr=clock:fossilization clockvarpr=igr;",
            "mcmcp ngen=20000000 printfreq=100000 samplefreq=10000 nruns=2 nchains=4 savebrlens=yes filename={0}-out;".format(
                ref
            ),
        ],
    )
