from lingpy import *
from lingpy.convert.strings import matrix2dst, write_nexus
from util import base_path

wl = Wordlist(base_path.joinpath("hmong-mein-analysis.tsv").as_posix())

# output nexus
for i in range(5,15):
    col = 't'+str(i)
    nexus = write_nexus(wl, 
                        ref=col,
                        mode='SPLITSTREE',
                        filename=''.join(['HM',col,'.nex'])
                        )