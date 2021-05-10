from lingpy import *
from pathlib import Path
from pkg.code import *
from tabulate import tabulate
import subprocess
from pyloconcordance.concordance import rscf
from pylotree import Tree as PTree

cognates = ['strict', 'loose', 'common', 'salient']

sims, quarts = [], []
tree_string = open('sagart2005.tre').read().strip() 
tree = Tree(tree_string)

for cognate in cognates:
    treeB = open(Path("results", "part_"+cognate+".tre")).read().strip()
    treeC = open(Path("results",
        "full_"+cognate+".tre")).read().strip()

    sims += [["subset", cognate, tree.get_distance(Tree(treeB))]]
    sims += [["all", cognate, tree.get_distance(Tree(treeC))]]


print("# RF")
print(tabulate(sorted(sims)))

for cognate in cognates:

    pathA = "results/part_"+cognate+".tre"
    pathB = "results/full_"+cognate+".tre"
    qd = subprocess.check_output(
        ["quartet_dist", "-v", "sagart2005.tre", pathA]
    )
    qd_array = (str(qd).replace("\\n", "").replace("b'", "").split("\\t"))
    nqdA = float(qd_array[3])
    qd = subprocess.check_output(
        ["quartet_dist", "-v", "sagart2005.tre", pathB]
    )    
    qd_array = (str(qd).replace("\\n", "").replace("b'", "").split("\\t"))
    nqdB = float(qd_array[3])
    quarts += [["subset", cognate, nqdA]]
    quarts += [["all", cognate, nqdB]]
print("# Quartets")
print(tabulate(sorted(quarts)))

wl = Wordlist(Path("results", "liusinitic.word_cognate.tsv").as_posix())
languages = get_revised_taxon_names()
taxa = [languages[x] for x in wl.cols]
print("")
stree = PTree(get_ordered_taxa()[0])
patterns = []
tree = PTree(open(Path("results", "full_"+cognate+".tre.rooted")).read().strip())
for concept in wl.rows:
    idxs = wl.get_dict(row=concept, entry=cognate+"id")
    pattern = []
    for taxon in wl.cols:
        entry = idxs[taxon]
        if not entry:
            pattern += ["Ø"]
        else:
            pattern += [[str(e) for e in entry]]
    patterns += [pattern]
    scores = rscf(stree, wl.cols, patterns, iterate=100)
    all_scores = []
    for node in stree.preorder[1:]:
        if node.descendants:
            if [n for n in node.descendants if n.descendants]:
                all_scores += [scores[node.name]["alld"]]
    print('{0:20} | {1:.4f} | {2}'.format(
        cognate,
        sum(all_scores)/len(all_scores),
        len(patterns)
        ))
    
print("")

for cognate in cognates:
    tree = PTree(open(Path("results", "full_"+cognate+".tre.rooted")).read().strip())
    etd = wl.get_etymdict(ref=cognate+"id")
    patterns = []
    for cogid, row in etd.items():
        pattern = []
        for idx in row:
            if idx != 0:
                pattern += ["1"]
            else:
                pattern += ["0"]
        patterns += [pattern]
    scores = rscf(tree, taxa, patterns, iterate=100)
    all_scores = []
    for node in tree.preorder[1:]:
        if node.descendants:
            if [n for n in node.descendants if n.descendants]:
                all_scores += [scores[node.name]["alld"]]

    print('{0:20} | {1:.4f} | {2}'.format(
        cognate,
        sum(all_scores)/len(all_scores),
        len(patterns)
        ))


