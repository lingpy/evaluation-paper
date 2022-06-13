"""
Export Data to Nexus Files for Phylogenetic Analysis

Final step of our workflow, produces various Nexus files, to be analyzed with
MrBayes, written to the folder `bayes`.
"""

from lingpy import Wordlist
from lingpy.convert.strings import matrix2dst
from collections import defaultdict
from lingpy.convert.strings import write_nexus
from lingrex.evaluate import compare_cognate_sets

from pkg.code import (
    get_liusinitic,
    lexical_distances,
    get_revised_taxon_names,
    nexus_path
)

part = get_liusinitic()
languages = get_revised_taxon_names()
taxa = [languages[t] for t in part.cols]


# An array with all the name of all the full cognate sets.
cognate_sets = ["strict", "loose", "common", "salient"]

ranks = compare_cognate_sets(part, "strictid", "looseid")
target_concepts = [row[0] for row in ranks if row[-1] <= 0.8]

print(
    "{0} concepts are selected for computing distance matrices (threshold is 0.8).".format(
        len(target_concepts)
    )
)

D, D2 = {0: part.columns}, {0: part.columns}
for idx in part:
    if part[idx, "concepts"] in target_concepts:
        D[idx] = part[idx]
        D[idx][part.columns.index("doculect")] = languages[part[idx, "doculect"]]
        D2[idx] = part[idx]
    else:
        D2[idx] = part[idx]
        D2[idx][part.columns.index("doculect")] = languages[part[idx, "doculect"]]


commands = [
    "set autoclose=yes nowarn=yes;",
    "lset coding=noabsencesites rates=gamma;",
    "prset clockratepr=exponential(3e5);",
    "prset treeagepr = uniform(1.5, 2.5);",
    "prset sampleprob=0.2 samplestrat=random speciationpr=exp(1);",
    "prset extinctionpr=beta(1,1) nodeagepr=calibrated;",
    "prset brlenspr=clock:fossilization clockvarpr=igr;",
    "mcmcp ngen=20000000 printfreq=100000 samplefreq=10000 nruns=2 nchains=4 savebrlens=yes"
    ]


wl = Wordlist(D)
for ref in ["strictid", "looseid", "commonid", "salientid"]:
    print("[i] writing {0}".format(ref))
    new_commands = [c for c in commands]
    new_commands[-1] += " filename=part-{0}-out;".format(ref)
    write_nexus(
        wl,
        ref=ref,
        commands=new_commands,
        filename=nexus_path("part-"+ref+'.nex').as_posix(),
    )
    new_commands = [c for c in commands]
    new_commands[-1] += " filename=full-{0}-out;".format(ref)
    write_nexus(
        Wordlist(D2),
        ref=ref,
        filename=nexus_path("full-"+ref+'.nex').as_posix(),
        commands=new_commands,
    )
