from lingpy import *
from linse.annotate import *
from util import data_path, base_path
import collections
import math

# purity formula
def P_degree(in_array):
    counter_array = collections.Counter(in_array)
    tmp=[]
    for k,v in counter_array.items():
        t = (v/len(in_array))**2
        tmp.append(t)
    return(math.sqrt(sum(tmp)))

alm = Alignments(base_path.joinpath("hmong-mien-evaluation-output.tsv").as_posix(),ref="cogids")

# get the part which indicated by Ratliff index 
tone_dict = {}
for i in alm.msa['cogids']:
    if i not in tone_dict.keys():
        tone_dict[i]={'doculect':[],'tone_categories':[]}
        doc=[]
        categories=[]
    for idx in alm.msa['cogids'][i]['ID']:
        tone_position=alm[idx, 'cogids'].index(i)
        entire_tone_class = alm[idx, 'tone_class'].split(' ')
        tone_class=entire_tone_class[tone_position]
        doc.append(alm[idx,'doculect'])
        categories.append(tone_class)
    tone_dict[i]['doculect']=doc
    tone_dict[i]['tone_categories']=categories

# calculate the purity.
for key, value in tone_dict.items():
    purity = P_degree(value['tone_categories'])
    print(key,purity)