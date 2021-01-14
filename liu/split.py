"""
stage 2:
tree splits.
print jaccard distances between method 1 and method 2
"""
from lingpy import *
from lingpy.compare.partial import Partial
from clldutils.text import strip_brackets, split_text
from collections import defaultdict
from itertools import combinations
from tabulate import tabulate

trees = {}
#part = Partial("liusinitic.tsv")
part = Partial('liusinitic_semi.tsv')
for cogid in ["strictid", "looseid", "autoid", "semiid"]:
    part.calculate("tree", ref=cogid, force=True, tree_calc="upgma")
    trees[cogid] = str(part.tree)

splits = {cogid: defaultdict(list) for cogid in trees}
etds = {}
for cogid in trees:
    etds[cogid] = part.get_etymdict(ref=cogid)
for cogid, etd in etds.items():
    for cid in etd:
        groups = []
        for t in etd[cid]:
            if t:
                groups += [part[t[0], "doculect"]]
        if len(groups) > 1:
            splits[cogid][", ".join(groups)] += [cid]

table = []
for cogidA, cogidB in combinations(trees, r=2):
    dst = []
    all_splits = sorted(set(list(splits[cogidA]) + list(splits[cogidB])))
    weights = {}
    for split in all_splits:
        if split in splits[cogidA]:
            wA = len(splits[cogidA][split])
        else:
            wA = 0
        if split in splits[cogidB]:
            wB = len(splits[cogidB][split])
        else:
            wB = 0
        weights[split] = wA + wB
    jacs = []
    for split in all_splits:
        if split in splits[cogidA] and split in splits[cogidB]:
            jacs += [weights[split]]
    jac = sum(jacs) / sum(weights.values())

    jacs2 = []
    for split in all_splits:
        if split in splits[cogidA] and split in splits[cogidA]:
            jacs2 += [weights[split]]
    jac2 = sum(jacs2) / sum(weights.values())
    print(cogidA, jac2)

    table += [[cogidA, cogidB, jac]]

print("")
print(tabulate(table, floatfmt=".2f"))
