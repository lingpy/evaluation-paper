"""
Step 6
This stap output the pap files for the bootstrapping analysis.
"""
from lingpy.compare.partial import Partial
from lingpy import Wordlist
from lingpy.convert.strings import matrix2dst
from collections import defaultdict
from lingpy.algorithm.clustering import neighbor
from pathlib import Path
from lingpy.convert.strings import write_nexus

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

# add new cognate sets
common_morpheme_cognates(part, ref="cogids", cognates="commonid", override=True)
salient_cognates(
    part, ref="cogids", cognates="salientid", morphemes="morphemes", override=True
)
part.add_cognate_ids("cogids", "strictid", idtype="strict", override=True)
part.add_cognate_ids("cogids", "looseid", idtype="loose", override=True)

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
    D[idx] = part[idx]
    D[idx][part.columns.index("doculect")] = languages[part[idx, "doculect"]]
wl = Wordlist(D)
for ref in ['strictid', 'looseid', 'commonid', 'salientid']:
    wl.output('paps.nex', filename=Path("nexus", ref).as_posix(),
            missing="-", ref=ref)
    write_nexus(wl, ref=ref, filename=Path("nexus", ref).as_posix(),
            commands=[
                    "set autoclose=yes nowarn=yes;",
                    "lset coding=noabsencesites rates=gamma;",
                    "constraint root = 1-.;",
                    "prset clockratepr=exponential(3e5);",
                    "prset sampleprob=0.2 samplestrat=random speciationpr=exp(1);",
                    "prset extinctionpr=beta(1,1) nodeagepr=calibrated;", 
                    "prset brlenspr=clock:fossilization clockvarpr=igr;",
                    "mcmcp ngen=20000000 printfreq=100000 samplefreq=10000 nruns=2 nchains=4 savebrlens=yes filename={0}-out;".format(ref)
                ])



