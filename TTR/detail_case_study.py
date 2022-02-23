"""
Checking step: This script is for pulling out cases that the compound words cannot be separated. It is a step to assist linguists checking their annotation during the annotation process. 

Input file: 
Dataname on EDICTOR. Eg. liusinitic

Output:
1. File output: .tsv Eg. case_by_case_discussion.tsv
2. Standard output: concept, Chinese, compound structure. 

"""
from lingpy import *
from pyedictor.util import *
from pyedictor import fetch
from collections import Counter
from tabulate import tabulate

# pull from Edictor
wl = fetch(
    "liusinitic",
    columns=[
        "DOCULECT",
        "CONCEPT",
        "TOKENS",
        "MORPHEMES",
        "COMPOUNDS",
        "COGIDS",
        "AUTOID",
        "STRICTID",
        "LOOSEID",
        "CHARACTERS_IS",
        "CHARACTERS",
        "LEXEME_NOTE",
        "CONCEPT_CHINESE",
        "STRUCTURE",
        "NOTE",
    ],
    to_lingpy=True,
)

"""
check the highlighted/salient morpheme.
"""
cases = {}
for idx, doculect, concept, morphemes, compounds, characters, notes in wl.iter_rows(
    "doculect", "concept", "morphemes", "compounds", "characters", "note"
):
    hmorphemes = [m for m in morphemes if "_" not in m]
    if "multisyllabic" in notes and not cases.get(concept):
        cases[concept] = {
            "multisyllabic": ["True"],
            "chinese": [characters.replace(" ", "")],
            "morpheme": [morphemes],
            "highlighted": [hmorphemes],
            "compound": [compounds],
            "doculect": [doculect],
        }
    elif "multisyllabic" in notes and cases.get(concept):
        cases[concept]["multisyllabic"].append("False")
        cases[concept]["chinese"].append(characters.replace(" ", ""))
        cases[concept]["morpheme"].append(morphemes)
        cases[concept]["highlighted"].append(hmorphemes)
        cases[concept]["compound"].append(compounds),
        cases[concept]["doculect"].append(doculect)
    elif (
        not cases.get(concept)
        and len(hmorphemes) == len(morphemes)
        and len(morphemes) > 1
    ):
        cases[concept] = {
            "multisyllabic": ["False"],
            "chinese": [characters.replace(" ", "")],
            "morpheme": [morphemes],
            "highlighted": [hmorphemes],
            "compound": [compounds],
            "doculect": [doculect],
        }
    elif (
        cases.get(concept) and len(hmorphemes) == len(morphemes) and len(morphemes) > 1
    ):
        cases[concept]["multisyllabic"].append("False")
        cases[concept]["chinese"].append(characters.replace(" ", ""))
        cases[concept]["morpheme"].append(morphemes)
        cases[concept]["highlighted"].append(hmorphemes)
        cases[concept]["compound"].append(compounds),
        cases[concept]["doculect"].append(doculect)

# standard output
cases_output = []
for key, value in cases.items():
    tmp_morpheme = [" ".join(x) for x in value["morpheme"]]
    tmp_highlighted = [" ".join(x) for x in value["highlighted"]]
    cases_output.append(
        [
            key,
            ",".join(value["chinese"]),
            ",".join(value["compound"]),
            ",".join(tmp_morpheme),
            ",".join(tmp_highlighted),
            ",".join(value["doculect"]), 
            ",".join(value["multisyllabic"]),
        ]
    )

# file output
with open("case_by_case_discussion.tsv", "w") as f:
    f.write(
        "|{0}|{1}|{2}|{3}|{4}|{5}|{6}|\n".format(
            "English",
            "Chinese",
            "compound",
            "morpheme",
            "highlighted",
            "doculect",
            "multisyllabic",
        )
    )
    f.write(
        "|{0}|{1}|{2}|{3}|{4}|{5}|{6}|\n".format(
            "------", "------", "------", "------", "------", "------", "------"
        )
    )
    for each in cases_output:
        f.write(
            "|{0}|{1}|{2}|{3}|{4}|{5}|{6}|\n".format(
                each[0], each[1], each[2], each[3], each[4], each[5], each[6]
            )
        )
f.close()
