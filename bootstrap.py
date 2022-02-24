"""
Step 5: Neighbor-join tree with 1000 iterations (bootstrapping score) 

Input:
Fetch data from lexibank_liusinitic.

Output:
File output: 
    plots/ete-loose.pdf
    plots/ete-loose.png
    plots/ete-strict.pdf
    plots/ete-strict.png
    plots/ete-common.pdf
    plots/ete-common.png
    plots/ete-salient.pdf
    plots/ete-salient.png
"""
from lingpy.compare.partial import Partial
from lingpy.convert.strings import matrix2dst
from collections import defaultdict
from pathlib import Path
import random
from pkg.bootstrap import bootstrap, hamming_distances, splits_from_tree
from pylotree import Tree as PTree
from ete3 import Tree, TreeStyle, AttrFace, faces, NodeStyle
from pylocluster import neighbor


from pkg.code import (
    get_liusinitic,
    common_morpheme_cognates,
    compare_cognate_sets,
    salient_cognates,
    compare_cognate_sets,
    lexical_distances,
    get_revised_taxon_names,
)

part = get_liusinitic(Partial)
languages = get_revised_taxon_names()
taxa = [languages[t] for t in part.cols]

# create common morpheme and salient morphemes
common_morpheme_cognates(part, ref="cogids", cognates="commonid", override=True)
salient_cognates(
    part, ref="cogids", cognates="salientid", morphemes="morphemes", override=True
)
ranks = compare_cognate_sets(part, "strictid", "looseid")
target_concepts = [row[0] for row in ranks if row[-1] <= 0.8]
D = {0: [c for c in part.columns]}
for idx in part:
    if part[idx, "concept"] in target_concepts:
        D[idx] = [part[idx, h] for h in D[0]]
part = Partial(D)


cognate_sets = ["strict", "loose", "common", "salient"]

I = 1000 # iterations

def layout(node):
    if node.is_leaf():
        N = AttrFace("name", fsize=8)
        faces.add_face_to_node(N, node, 1, position="aligned")

# style options for ete3
colors = {
        "Man": "#F2CC8F",
        "Yue": "#81B29A",
        "Xia": "#9DA0BE",
        "Hui": "#ECAEAE",
        "Jin": "#E58E76",
        "Hak": "#F4F1DE",
        "Wu": "#B8B8BA",
        "Gan": "#CED4DA",
        "Min": "#FF8C00",
        "Pin": "#DAA520"
        }


taxa = [languages[t] for t in part.cols]
style = NodeStyle(
        shape="square", 
        vt_line_width=2, 
        hz_line_width=2,
        fgcolor="black")
tsparams = dict(
        scale=100,
        mode="r",
        orientation=0,
        root_opening_factor=1,
        draw_guiding_lines=True,
        guiding_lines_type=0,
        guiding_lines_color="black",
        complete_branch_lines_when_necessary=True,
        extra_branch_line_type=0,
        show_branch_support=True,
        extra_branch_line_color="black",
        layout_fn=layout,
        show_leaf_name=False
        )
ts = TreeStyle()
for k, v in tsparams.items():
    setattr(ts, k, v)

# Generate Neighbor-joining trees and bootstrapping.
for cognate in cognate_sets:
    paps = [v for k, v in sorted(part.get_paps(ref=cognate+"id").items(), key=lambda
        x: x[0])]
    matrix = hamming_distances(paps)
    tree = PTree(neighbor(matrix, taxa))
    etetree = Tree(tree.newick, format=1)
    splits, trees = bootstrap(paps, taxa, tree, iterations=I)
    active_splits = splits_from_tree(tree)
    scores = []
    etetree.set_outgroup(
            etetree.get_common_ancestor("Fuzhou_Min", "Xiamen_Min"))
    etedict = {}
    for node in etetree.iter_descendants(strategy="postorder"):
        etedict[node.name] = node
    for (nodeA, nodeB), split in active_splits.items():
        if etedict[nodeA] in etedict[nodeB].children: 
            etedict[nodeA].support = len(splits[split])/I
            scores += [len(splits[split])/I]
    print('{0:10} | {1:.2f}'.format(cognate, sum(scores)/len(scores)))
    with open(Path("results", cognate+".trees"), "w") as f:
        for t in trees:
            f.write(t+'\n')
    for node in etetree.iter_descendants(strategy="postorder"):
        node.img_style = style
        #node.dist = 0.2
    etetree.img_style = style
    for group, color in colors.items():
        selection = [t for t in languages.values() if t.endswith("_"+group)]
        ca = etetree.get_common_ancestor(*selection)
        if len(ca.get_leaf_names()) <= len(selection) + 4:
            new_style = {k: v for k, v in style.items()}
            new_style["bgcolor"] = color
            ca.img_style = NodeStyle(**new_style)
        else:
            for t in selection:
                new_style = {k: v for k, v in style.items()}
                new_style["bgcolor"] = color
                etetree.get_leaves_by_name(t)[0].img_style = NodeStyle(**new_style)
    etetree.render(Path("plots", "ete-"+cognate+".pdf").as_posix(), tree_style=ts)



