from lingpy import *
from pathlib import Path
from pkg.code import *
from tabulate import tabulate
import subprocess

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
