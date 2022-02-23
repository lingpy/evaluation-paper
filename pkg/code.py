"""
Helper functions used in our study.
"""
from lexibank_liusinitic import Dataset
import lingpy
from collections import defaultdict
from lingpy.evaluate.acd import _get_bcubed_score as bcs
import statistics
from clldutils.text import strip_brackets, split_text
from itertools import combinations
from lingpy.convert.tree import nwk2tree_matrix



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
    """
    fetch data from the lexibank dataset. 
    """
    return cls(Dataset().raw_dir.joinpath('liusinitic.tsv').as_posix())


def get_clean_liusinitic(cls=lingpy.Wordlist):
    """
    fetch data from the lexibank dataset. 
    """
    return cls(Dataset().raw_dir.joinpath('liusinitic_ignored_IB.tsv').as_posix())

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
        wordlist, ref="cogids", concept="concept", annotation=None, 
        suffixes=["suf", "suffix", "SUF", "SUFFIX"]):
    """
    This function takes a wordlist file as an input and calculate the concept colexification.
    """
    
    if annotation:
        D = {}
        for idx, cogids, morphemes in wordlist.iter_rows(ref, annotation):
            new_cogids = []
            for cogid, morpheme in zip(cogids, morphemes):
                if not sum([1 if s in morpheme else 0 for s in suffixes]):
                    new_cogids += [cogid]
            D[idx] = lingpy.basictypes.ints(new_cogids)
        wordlist.add_entries(ref+"_derived", D, lambda x: x)
        new_ref = ref+"_derived"
    else:
        new_ref = ref

    etd = wordlist.get_etymdict(ref=new_ref)
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
        for idx in reflexes:
            doculect, cogids = wordlist[idx, "doculect"], wordlist[idx, new_ref]
            scores += [statistics.mean([indices[doculect][cogid] for cogid in cogids])]
        all_scores += [[cnc, statistics.mean(scores), ""]]
    return sorted(all_scores, key=lambda x: (x[1], x[0]))


def common_morpheme_cognates(wordlist, ref="cogids", cognates="autoid",
        morphemes="automorphemes", override=True):
    """
    Convert partial cognates to full cognates.
    """

    C, M = {}, {}
    current = 1
    for concept in wordlist.rows:
        base = split_text(strip_brackets(concept))[0].upper().replace(" ", "_")
        idxs = wordlist.get_list(row=concept, flat=True)
        cogids = defaultdict(list)
        for idx in idxs:
            M[idx] = [c for c in wordlist[idx, ref]]
            for cogid in lingpy.basictypes.ints(wordlist[idx, ref]):
                cogids[cogid] += [idx]
        for i, (cogid, idxs) in enumerate(
            sorted(cogids.items(), key=lambda x: len(x[1]), reverse=True)
        ):
            for idx in idxs:
                if idx not in C:
                    C[idx] = current
                    M[idx][M[idx].index(cogid)] = base
                else:
                    M[idx][M[idx].index(cogid)] = "_" + base.lower()
            current += 1
    wordlist.add_entries(cognates, C, lambda x: x)
    if morphemes:
        wordlist.add_entries(morphemes, M, lambda x: x, override=override)


def salient_cognates(
        wl, ref="cogids", cognates="newcogid", morphemes="morphemes",
        override=True):
    """
    Convert partial cognates to full cognates ignoring non-salient cognate sets.
    """

    lookup, D = {}, {}
    for idx, cogids, morphemes in wl.iter_rows(ref, morphemes):
        selected_cogids = []
        for cogid, morpheme in zip(cogids, morphemes): 
            if not morpheme.startswith("_"):
                selected_cogids += [cogid]
        salient = tuple(selected_cogids)
        if salient in lookup:
            D[idx] = lookup[salient]
        elif D.values():
            next_cogid = max(D.values()) + 1
            lookup[salient] = next_cogid
            D[idx] = next_cogid
        else:
            lookup[salient] = 1
            D[idx] = 1

    wl.add_entries(cognates, D, lambda x: x, override=override)



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
