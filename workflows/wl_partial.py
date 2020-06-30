from lingpy import *
from lingpy.compare.partial import Partial
from lebor.algorithm import cogids2cogid

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

# convert to full cognate
cogids2cogid(part, ref='cogids', cognates='lebor_cogid')


part.output("tsv", filename="HM-wordlist-partial", prettify=False)
