"""
Bootstrap implementation.
"""

from lingpy.algorithm.clustering import neighbor
from pylotree import Tree
import random
import itertools
from tqdm import tqdm as progressbar
from collections import defaultdict
random.seed(1234)


def strap(patterns, strip=0.7):
    """
    Get a subset of the patterns.
    """
    this_sample = random.sample(
            range(len(patterns)),
            int(strip*len(patterns)+0.5)
            )
    for i in range(int(0.3*len(patterns)+0.5)):
        this_sample += [random.choice(this_sample)]
    new_patterns = []
    for i in this_sample:
        new_patterns += [patterns[i]]
    return new_patterns


def hamming_distances(patterns, missing="Ø"):
    """
    get the hamming distance
    """
    matrix = [[0 for i in range(len(patterns[0]))] for j in
            range(len(patterns[0]))]
    for i, j in itertools.combinations(range(len(patterns[0])), r=2):
        hits, total = 0, 0
        for row in patterns:
            if missing in (row[i], row[j]):
                continue
            if row[i] == row[j]:
                hits += 1
            total += 1
        matrix[i][j] = matrix[j][i] = 1-hits/total
    return matrix


def get_splits(run, tree, splits):
    leaves = frozenset(tree.root.get_leaf_names())
    visited = set()
    for node in tree.preorder[1:]:
        splitA = frozenset(node.get_leaf_names())
        splitB = frozenset([l for l in leaves if l not in splitA])
        if splitA not in visited:
            splits[splitA] += [run]
        if splitB not in visited:
            splits[splitB] += [run]

        visited.add(splitA)
        visited.add(splitB)
        

def splits_from_tree(tree):
    splits = {}
    leaves = frozenset(tree.root.get_leaf_names())
    for node in tree.preorder[1:]:
        splitA = frozenset(node.get_leaf_names())
        splitB = frozenset([l for l in leaves if l not in splitA])

        if node.ancestor.name == tree.root.name:
            nodeA = node.name
            nodeB = [n.name for n in node.ancestor.descendants if n.name != nodeA][0]
        else:
            nodeA = node.name
            nodeB = node.ancestor.name
        splits[nodeA, nodeB] = splitA
        splits[nodeB, nodeA] = splitB
    return splits


def bootstrap(patterns, taxa, tree, cluster_method=neighbor, iterations=100,
        strip=0.7):
    splits = defaultdict(list)
    trees = []
    for i in progressbar(range(iterations), desc="bootstrapping"):
        new_patterns = strap(patterns, strip=strip)
        matrix = hamming_distances(new_patterns, missing="Ø")
        new_tree = Tree(neighbor(matrix, taxa))
        trees += [new_tree.newick]
        get_splits(i, new_tree, splits)
    return splits, trees



