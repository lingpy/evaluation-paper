from lingpy import *

from util import base_path

wl = Wordlist(base_path.joinpath("hmong-mein-analysis.tsv").as_posix())
# reference  : cogid
wl.calculate("dst", taxa="doculect", ref="cogid")
wl.output("dst", filename="hm-cogid", taxa="doculect", ref="cogid")
# threshold 0.55, cogids2cogid
wl.calculate("dst", taxa="doculect", ref="autot11")
wl.output("dst", filename="hm-autot11", taxa="doculect", ref="autot11")
