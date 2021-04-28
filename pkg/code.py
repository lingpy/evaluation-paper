"""
Various functions used in our study.
"""
from lexibank_liusinitic import Dataset
import lingpy
from collections import defaultdict
from lingpy.evaluate.acd import _get_bcubed_score as bcs


def compare_cognate_sets(wordlist, refA, refB):
    """
    Compute cognate set comparison statistics.
    """
    ranks = []
    for concept in wordlist.rows:
        cogsA = wordlist.get_list(row=concept, flat=True, entry=refA)
        cogsB = wordlist.get_list(row=concept, flat=True, entry=refB)
        p, r = bcs(cogsA, cogsB), bcs(cogsB, cogsA)
        f = 2 * (p * r) / (p + r)
        ranks += [[concept, p, r, f]]
    return ranks


def get_liusinitic(cls=lingpy.Wordlist):
    return cls(Dataset().raw_dir.joinpath('liusinitic.tsv').as_posix())


def get_chinese_map():
    wordlist = get_liusinitic()
    chinese = defaultdict(list)
    for idx, concept, character in wordlist.iter_rows("concept", "characters"):
        chinese[concept] += [character.replace(" ", "")]
    for k, v in chinese.items():
        chinese[k] = "/".join(
                sorted(set(v), key=lambda x: v.count(x), reverse=True)[:2])
    return chinese
