"""
Analyze the data according to a cognate detection workflow.
"""
from lingpy import *
from lingpy.compare.partial import Partial
from lingpy.compare import partial
from linse.annotate import seallable
from collections import defaultdict
from lingrex.colex import find_colexified_alignments, find_bad_internal_alignments
from lingrex.align import template_alignment
from linse.transform import morphemes
from clldutils.text import strip_brackets, split_text

from util import base_path
from tabulate import tabulate
from lingpy.evaluate.acd import bcubes


# define function
def get_structure(sequence):
    """
    produce a list of structure tokens
    """
    out = []
    for m in morphemes(sequence):
        out += [
            "".join(
                seallable(
                    m,
                    medials={
                        "j","w","jw","wj","i̯","u̯","i̯u̯","u̯i̯","iu","ui","y","ɥ","l",
                        "lj","lʲ","r","rj","rʲ","ʐ","ʑ","ʂ","ʂ","rʷ","lʷ","u/w","i/j",
                        "ɹ","z","ʁ","m","wj/ɥ",
                    },
                )
            )
        ]
    return list("+".join(out))


# cogids2cogid
def cogids2cogid(wordlist, ref="cogids", cognates="cogid", morphemes="morphemes"):
    C, M = {}, {}
    current = 1
    for concept in wordlist.rows:
        base = split_text(strip_brackets(concept))[0].upper().replace(" ", "_")
        idxs = wordlist.get_list(row=concept, flat=True)
        cogids = defaultdict(list)
        for idx in idxs:
            M[idx] = [c for c in wordlist[idx, ref]]
            for cogid in basictypes.ints(wordlist[idx, ref]):
                cogids[cogid] += [idx]
        for i, (cogid, idxs) in enumerate(
            sorted(cogids.items(), key=lambda x: len(x[1]), reverse=True)
        ):
            for idx in idxs:
                if idx not in C:
                    C[idx] = current
                    M[idx][M[idx].index(cogid)] = base
                else:
                    M[idx][M[idx].index(cogid)] = "_" + base.lower()
            current += 1
    wordlist.add_entries(cognates, C, lambda x: x)
    if morphemes:
        wordlist.add_entries(morphemes, M, lambda x: x)


# partial cognate
try:
    part = Partial(base_path.joinpath("hmeval-partial.bin.tsv").as_posix())
except:
    wl = Wordlist(
        base_path.joinpath("hmeval.tsv").as_posix())
    D = {0: wl.columns}
    for idx in wl:
        if not 'remove' in wl[idx, 'note']:
            D[idx] = wl[idx]
    part = Partial(
        D, segments='tokens', #base_path.joinpath("hmeval.tsv").as_posix(), segments="tokens"
    )
    part.get_partial_scorer(runs=10000)
    part.output(
        "tsv",
        filename=base_path.joinpath("hmeval-partial.bin").as_posix(),
        ignore=[],
        prettify=False,
    )
for i in range(5,15):
    t = 0.05 * i
    ts = 't'+str(i)
    part.partial_cluster(
        method="lexstat", threshold=t, ref=ts, cluster_method="infomap",
    )
    part.add_cognate_ids(ts, "strict"+ts, idtype="strict")
    part.add_cognate_ids(ts, "loose"+ts, idtype="loose")
    cogids2cogid(part, ref=ts, cognates='auto'+ts, morphemes='morphemes'+ts)
    p, r, f = bcubes(part, 'cogid', 'auto'+ts, pprint=False)
    p1, r1, f1 = bcubes(part, 'cogid', 'strict'+ts, pprint=False)
    p2, r2, f2 = bcubes(part, 'cogid', 'loose'+ts, pprint=False)
    print('# {0:.2f} ({1})'.format(t, ts))
    print(tabulate([[p, r, f], [p1, r1, f1], [p2, r2, f2]], floatfmt='.2f',
        tablefmt='pipe'))

# splitter
part.add_entries("splitid", {idx: idx for idx in part}, lambda x: x)

# lumper
part.renumber("concept", "lumpid")

#part.output(
#    "tsv",
#    filename=base_path.joinpath("hmong-mien-alignments").as_posix(),
#    prettify=False,
#)

bcubes(part, 'cogid', 'lumpid', pprint=True)
bcubes(part, 'cogid', 'splitid', pprint=True)
