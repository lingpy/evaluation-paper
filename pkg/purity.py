from lingpy import *
from linse.annotate import *
from util import data_path, base_path
import collections
import math
import operator

# purity formula
def P_degree(in_array, split_merger):
    counter_array = collections.Counter(in_array)
    tmp = []
    if split_merger:
        tmp_dict = {}
        for k, v in counter_array.items():
            k_array = k.split(".")
            if len(k_array) == 1:
                if k_array[0] in tmp_dict.keys():
                    tmp_dict[k_array[0]].append(v)
                else:
                    tmp_dict[k_array[0]] = [v]
            elif len(k_array) > 1:
                if set(k_array).intersection(tmp_dict.keys()):
                    compare_component = {}
                    for each in k_array:
                        if each in tmp_dict.keys():
                            compare_component[each] = tmp_dict[each]
                    to_tmp_key = max(
                        compare_component.items(), key=operator.itemgetter(1)
                    )[0]
                    tmp_dict[to_tmp_key].append(counter_array[k])
                else:
                    tmp_dict[k_array[0]] = [v]
        total = sum([sum(x) for x in tmp_dict.values()])
        for each_value in tmp_dict.values():
            t = (sum(each_value) / total) ** 2
            tmp.append(t)
    else:
        for k, v in counter_array.items():
            t = (v / len(in_array)) ** 2
            tmp.append(t)
    if tmp_dict:
        return tmp_dict, math.sqrt(sum(tmp))
    else:
        return math.sqrt(sum(tmp))


alm = Alignments(
    base_path.joinpath("hmong-mien-evaluation-output.tsv").as_posix(), ref="cogids"
)

# get the part which indicated by Ratliff index
tone_dict = {}
for i in alm.msa["cogids"]:
    if i not in tone_dict.keys():
        tone_dict[i] = {"doculect": [], "tone_categories": []}
        doc = []
        categories = []
    for idx in alm.msa["cogids"][i]["ID"]:
        tone_position = alm[idx, "cogids"].index(i)
        entire_tone_class = alm[idx, "tone_class"].split(" ")
        tone_class = entire_tone_class[tone_position]
        doc.append(alm[idx, "doculect"])
        categories.append(tone_class)
    tone_dict[i]["doculect"] = doc
    tone_dict[i]["tone_categories"] = categories

# calculate the purity.
print("COGIDS | Purity score | Tone patters| Analzed tone patterns |Doculects")

for key, value in tone_dict.items():
    purity_dict, purity = P_degree(value["tone_categories"], split_merger=True)
    print(
        key,
        "|",
        purity,
        "|",
        collections.Counter(value["tone_categories"]),
        "|",
        purity_dict,
        "|",
        value["doculect"],
    )
