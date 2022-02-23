"""
Step 1: Fetch the data on EDICTOR and saved as a wordlist dataset.   

Input: 
Dataname on EDICTOR. Eg. liusinitic

Output:
1. File output: wordlist. Eg. liusinitic_20211230.tsv
2. Standard output: part of speech tag and the frequencies.  

"""
from lingpy import *
from pyedictor.util import *
from pyedictor import fetch
from collections import Counter
from tabulate import tabulate
from pathlib import Path


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
output_path = Path('liusinitic/raw/liusinitic')
wl.output("tsv", filename=output_path.as_posix(), prettify=False)
morpheme_dict = {}
compound_type_dict = {}
compound_dict = {}
character_dict = {}
for idx, concept, morphemes, compounds, characters in wl.iter_rows(
    "concept", "morphemes", "compounds", "characters"
):
    for m in morphemes:
        tmp = m.split("/")[0]
        if morpheme_dict.get(tmp):
            morpheme_dict[tmp] += 1
        else:
            morpheme_dict[tmp] = 1
    compound = compounds.split(" ")
    if compound_type_dict.get(compounds):
        compound_type_dict[compounds].append((concept, characters.replace(" ", "")))
    else:
        compound_type_dict[compounds] = [(concept, characters.replace(" ", ""))]
    for c in compound:
        if compound_dict.get(c):
            compound_dict[c] += 1
        else:
            compound_dict[c] = 1
    for chr in characters:
        chr_tmp = chr.split(" ")
        for chr_each in chr_tmp:
            if character_dict.get(chr_each):
                character_dict[chr_each] += 1
            else:
                character_dict[chr_each] = 1

# Part of speech summary
output_array = []
for k, v in compound_dict.items():
    output_array.append([k, v])

print(tabulate(output_array, headers=["Part of speech", "Times"]))

# Compound type
compound_array = []
for k, v in compound_type_dict.items():
    tmp_concepts = set()
    tmp_characters = set()
    for v1, v2 in v:
        tmp_concepts.add(v1)
        tmp_characters.add(v2)
    compound_array.append(
        [k, ",".join([x for x in tmp_concepts]), ",".join([y for y in tmp_characters])]
    )

with open("compound_type_summary.tsv", "w") as f:
    f.write("|{0}|{1}|\n".format("Compound type", "Chinese"))
    f.write("|{0}|{1}|\n".format("------", "------"))
    for each in compound_array:
        f.write("|{0}|{1}|\n".format(each[0], each[2]))
f.close()

print(tabulate(compound_array, headers=["Compound type", "Concepts", "Chinese"]))