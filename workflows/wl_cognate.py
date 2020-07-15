from lingpy import *
from lingpy.compare.partial import Partial
from linse.annotate import seallable
from collections import defaultdict
from lingrex.colex import find_colexified_alignments, find_bad_internal_alignments
from lingrex.align import template_alignment
from linse.transform import morphemes
from clldutils.text import strip_brackets, split_text

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
                        "j",
                        "w",
                        "jw",
                        "wj",
                        "i̯",
                        "u̯",
                        "i̯u̯",
                        "u̯i̯",
                        "iu",
                        "ui",
                        "y",
                        "ɥ",
                        "l",
                        "lj",
                        "lʲ",
                        "r",
                        "rj",
                        "rʲ",
                        "ʐ",
                        "ʑ",
                        "ʂ",
                        "ʂ",
                        "rʷ",
                        "lʷ",
                        "u/w",
                        "i/j",
                        "ɹ",
                        "z",
                        "ʁ",
                        "m",
                        "wj/ɥ"
                    },
                )
            )
        ]
    return list("+".join(out))

# cogids2cogid
def cogids2cogid(wordlist, ref='cogids', cognates='cogid',
    morphemes='morphemes'):
    C, M = {}, {}
    current = 1
    for concept in wordlist.rows:
        base = split_text(strip_brackets(concept))[0].upper().replace(' ', '_')
        idxs = wordlist.get_list(row=concept, flat=True)
        cogids = defaultdict(list)
        for idx in idxs:
            M[idx] = [c for c in wordlist[idx, ref]]
            for cogid in basictypes.ints(wordlist[idx, ref]):
                cogids[cogid] += [idx]
        for i, (cogid, idxs) in enumerate(sorted(cogids.items(), key=lambda x: len(x[1]),
                reverse=True)):
            for idx in idxs:
                if idx not in C:
                    C[idx] = current
                    M[idx][M[idx].index(cogid)] = base
                else:
                    M[idx][M[idx].index(cogid)] = '_'+base.lower()
            current += 1
    wordlist.add_entries(cognates, C, lambda x: x)
    if morphemes:
        wordlist.add_entries(morphemes, M, lambda x: x)

# partial cognate
try:
    part = Partial("HM-wordlist-partial.bin.tsv")
except:
    part = Partial("HM-wordlist-for-evaluate.tsv", segments="tokens")
    part.get_partial_scorer(runs=10000)
    part.output("tsv", filename="HM-wordlist.bin", ignore=[], prettify=False)
finally:
    part.partial_cluster(
        method="lexstat",
        threshold=0.55,
        ref="cogids",
        mode="global",
        gop=-2,
        cluster_method="infomap",
    )
part.output("tsv", filename="HM-wordlist-partial", prettify=False)
# partial to cross-semantic
alms = Alignments("HM-wordlist-partial.tsv", ref="cogids")
alms.add_entries(
    "structure", "tokens", lambda x: get_structure(x),
)
print("[i] added segments")
D = {0: [c for c in alms.columns]}
for idx, tokens, structure in alms.iter_rows("tokens", "structure"):
    if len(tokens) != len(structure):
        print("[!]", tokens, structure, alms[idx, "concept"])
    elif "?" in structure:
        print("[!!]", tokens, structure, alms[idx, "concept"])
    else:
        D[idx] = alms[idx]

alms = Alignments(D, ref="cogids")
template_alignment(
    alms,
    ref="cogids",
    template="imnct+imnct+imnct+imnct+imnct+imnct",
    structure="structure",
    fuzzy=True,
    segments="tokens",
)
find_bad_internal_alignments(alms)
find_colexified_alignments(alms, cognates="cogids", segments="tokens", ref="crossids")
# re-align
template_alignment(
    alms,
    ref="crossids",
    template="imnct+imnct+imnct+imnct+imnct+imnct",
    structure="structure",
    fuzzy=True,
    segments="tokens",
)
# convert to full cognate
cogids2cogid(alms, ref="crossids", cognates="lebor_cogid")

alms.output("tsv", filename="HM-wordlist-cogids2cogid", prettify=False)
