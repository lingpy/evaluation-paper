from lingpy import *
from lingpy.compare.partial import Partial
from lebor.algorithm import cogids2cogid
from linse.annotate import seallable
from lingrex.colex import find_colexified_alignments, find_bad_internal_alignments
from lingrex.align import template_alignment
from linse.transform import morphemes

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
                    },
                )
            )
        ]
    return list("+".join(out))


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

alms.output("tsv", filename="HM-wordlist-lebor", prettify=False)
