"""
Various functions used in our study.
"""
from lexibank_liusinitic import Dataset
import lingpy
from collections import defaultdict
from lingpy.evaluate.acd import _get_bcubed_score as bcs
import statistics


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


def cross_semantic_cognate_statistics(
        wordlist, ref="cogids", concept="concept", annotation=None):
    """
    This function takes a wordlist file as an input and calculate the concept colexification.
    """

    etd = wordlist.get_etymdict(ref=ref)
    indices = {ln: {} for ln in wordlist.cols}
    for i, ln in enumerate(wordlist.cols):
        for cogid, reflexes in etd.items():
            if reflexes[i]:
                concepts = [wordlist[idx, concept] for idx in reflexes[i]]
                indices[ln][cogid] = len(set(concepts)) - 1

    all_scores = []
    for cnc in wordlist.rows:
        # Loop through all the concepts in the data
        reflexes = wordlist.get_list(
            row=cnc, flat=True
        )  # The lexical entries of the concept.
        scores = []
        derivation = 0
        if annotation:
            for idx in reflexes:
                ln, cogids = wordlist[idx, "doculect"], wordlist[idx, ref]
                scores += [statistics.mean([indices[ln][cogid] for cogid in cogids])]
                for m in wordlist[idx, annotation]:
                    if "SUF" in m or "suffix" in m:
                        derivation += 1
        if derivation > 0:
            all_scores += [[cnc, statistics.mean(scores), "!derivation!"]]
        else:
            all_scores += [[cnc, statistics.mean(scores), ""]]
    return sorted(all_scores, key=lambda x: (x[1], x[0]))

