"""
check the correspondences.
"""
from lingpy import *
from lingpy.evaluate.acd import bcubes
from lingpy.evaluate.acd import diff, _get_bcubed_score
from util import base_path
from lingrex.copar import CoPaR


# read in data
cop = CoPaR(
    base_path.joinpath("hmong-mien-evaluation-output.tsv").as_posix(),
    ref="crossids",
    fuzzy=True,
    segment="tokens",
)

cop.get_sites(minrefs=3, structure='structure')
cop.cluster_sites()
cop.sites_to_pattern()
cop.add_patterns()
cop.write_patterns(base_path.joinpath('hmong-mien-patterns.tsv').as_posix())
cop.output('tsv', filename=base_path.joinpath('hmong-mien-correspondence-patterns.tsv').as_posix(), prettify=False)

# statistics
sps=['i','m','n','c','t']
    
total_correspondence_sets = len(cop.clusters)
print('{0}: {1}'.format('The total sound correspondence cluster sets', total_correspondence_sets))
    
print('The number of regular correspondence sets in each position')
for sp in sps:
    t = [x[1] for x, y in cop.clusters.items() if len(y)>1 and x[0] ==sp]
    print('{0}: {1}'.format(sp, len(t)))
    
print('The number of singletons in each position ')
for sp in sps:
    t = [x[1] for x, y in cop.clusters.items() if len(y)==1 and x[0] ==sp]
    print('{0}: {1}'.format(sp, len(t)))