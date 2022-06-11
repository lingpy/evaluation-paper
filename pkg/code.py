"""
Various functions used in our study.
"""
from lexibank_liusinitic import Dataset
import lingpy
from collections import defaultdict
from clldutils.text import strip_brackets, split_text
from itertools import combinations
from lingpy.convert.tree import nwk2tree_matrix
from pathlib import Path


def repo_path(*comps):
    return Path(__file__).parent.parent.joinpath(*comps)


def results_path(*comps):
    return Path(__file__).parent.parent.joinpath("results", *comps)


def plots_path(*comps):
    return Path(__file__).parent.parent.joinpath("plots", *comps)


def nexus_path(*comps):
    return Path(__file__).parent.parent.joinpath("bayes", *comps)


def get_liusinitic(cls=lingpy.Wordlist):
    return cls(str(repo_path("edictor", "liusinitic.tsv")))


def get_chinese_map():
    wordlist = get_liusinitic()
    chinese = defaultdict(list)
    for idx, concept, character in wordlist.iter_rows("concept", "characters"):
        chinese[concept] += [character.replace(" ", "")]
    for k, v in chinese.items():
        chinese[k] = "/".join(
                sorted(set(v), key=lambda x: v.count(x), reverse=True)[:2])
    return chinese


def lexical_distances(wordlist, subset, ref="cogid"):
    """
    Compute lexicostatistical distances.
    """

    matrix = [[0 for cell in range(wordlist.width)] for row in range(wordlist.width)]
    for (i, langA), (j, langB) in combinations(enumerate(wordlist.cols), r=2):
        common, total = 0, 0
        lookupA, lookupB = wordlist.get_dict(col=langA, entry=ref), wordlist.get_dict(
            col=langB, entry=ref
        )
        for concept in lookupA and subset:
            cogsA, cogsB = lookupA.get(concept, []), lookupB.get(concept, [])
            if [x for x in cogsA if x in cogsB]:
                common += 1
                total += 1
            elif cogsA and cogsB:
                total += 1
        matrix[i][j] = matrix[j][i] = 1-(common/total)
    return matrix


def get_ordered_taxa():
    tree = Dataset().etc_dir.read_csv("trees.tsv", delimiter="\t")[1][1].replace("XiAn", "Xi_an").replace("Haerbin", "Ha_erbin")
    taxa = nwk2tree_matrix(tree)[1]
    return tree, taxa


def get_revised_taxon_names():
    
    languages = {}
    for language in Dataset().languages:
        languages[language['Name']] = language['ID']+'_'+language['DialectGroup'][:3]
    return languages
