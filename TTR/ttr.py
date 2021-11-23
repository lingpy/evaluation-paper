from lingpy.compare.partial import Partial
from collections import Counter

morpheme_dict = {}
compound_dict = {}
character_dict = {}
part = Partial("liusinitic.tsv")
total_morpheme = []
total_compound = []
for idx, morphemes, compounds, characters in part.iter_rows(
    "morphemes", "compounds", "characters"
):
    for m in morphemes:
        tmp = m.split("/")[0]
        if morpheme_dict.get(tmp):
            morpheme_dict[tmp] += 1
        else:
            morpheme_dict[tmp] = 1
    compound = compounds.split(" ")
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


# Type-Token Ratio: morpheme
ttr_morpheme = len(morpheme_dict.keys()) / sum(morpheme_dict.values())
print("ttr_morpheme:{0}".format(ttr_morpheme))
# Type-Token Ratio: morphosyntax
ttr_morphosyntax = len(compound_dict.keys()) / sum(compound_dict.values())
print("ttr_morphosyntax:{0}".format(ttr_morphosyntax))
# Type-Token Ratio: charaters
ttr_characters = len(character_dict.keys()) / sum(character_dict.values())
print("ttr_characters:{0}".format(ttr_characters))
