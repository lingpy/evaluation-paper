from lingpy import *

from util import base_path

wl = Wordlist(base_path.joinpath("hmong-mein-analysis.tsv").as_posix())
# reference  : cogid
wl.calculate("dst", taxa="doculect", ref="cogid")
wl.output(
    "dst",
    filename=base_path.joinpath("hm-cogid").as_posix(),
    taxa="doculect",
    ref="cogid",
)
# threshold 0.55, cogids2cogid
wl.calculate("dst", taxa="doculect", ref="autot11")
wl.output(
    "dst",
    filename=base_path.joinpath("hm-autot11").as_posix(),
    taxa="doculect",
    ref="autot11",
)
