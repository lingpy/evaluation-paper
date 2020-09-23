"""
This script merges the different datasets on Hmong-Mien languages.
"""
from lingpy import *
from pyconcepticon import Concepticon
from cldfcatalog import Config
from linse.annotate import soundclass

from collections import defaultdict

from lexibank_chenhmongmien import Dataset as chenhmongmien
from lexibank_ratliffhmongmien import Dataset as ratliffhmongmien
from lexibank_wold import Dataset as wold

from util import data_path, base_path

# set up the general structure of our datasets
columns = [
    "id",
    "language_id",
    "language_name",
    "language_subgroup",
    "language_glottocode",
    "concept_name",
    "concept_concepticon_id",
    "concept_concepticon_gloss",
    "concept_chinese_gloss",
    "value",
    "form",
    "segments",
    "cogid_cognateset_id",
    "tone_class",
    "tone_value",
]

namespace = [
    ("id", "lexibank_id"),
    ("language_subgroup", "subgroup"),
    ("concept_concepticon_gloss", "concept"),
    ("concept_name", "concept_in_source"),
    ("concept_chinese_gloss", "chinese_gloss"),
    ("language_id", "doculect"),
    ("language_name", "doculect_name"),
    ("language_glottocode", "glottocode"),
    ("segments", "tokens"),
    ("concept_concepticon_id", "concepticon"),
    ("cogid_cognateset_id", "cogid"),
    ("tone_class", "tone_class"),
    ("tone_value", "tone_value"),
]

# prepare concepticon references
concepticon = Concepticon(Config.from_file().get_clone("concepticon"))
concepts = {
    c.concepticon_gloss: c.concepticon_id
    for c in concepticon.conceptlists["Chen-2012-888"].concepts.values()
    if c.concepticon_id
}

languages = {
    row[0]: [row[3], row[4]]
    for row in csv2list(
        data_path.joinpath("languages.tsv").as_posix(), strip_lines=False
    )[1:]
}

print("[i] loaded the data")

# load datasets
ratliff = Wordlist.from_cldf(
    ratliffhmongmien().cldf_dir.joinpath("cldf-metadata.json").as_posix(),
    columns=columns,
    namespace=dict(namespace),
    filter=lambda row: row["language_id"] in languages.keys()
    and row["concept_concepticon_id"],
)

chen = Wordlist.from_cldf(
    chenhmongmien().cldf_dir.joinpath("cldf-metadata.json").as_posix(),
    columns=columns,
    namespace=dict(namespace),
    filter=lambda row: row["language_id"] in languages.keys()
    and row["concept_concepticon_id"],
)

whitehmong = Wordlist.from_cldf(
    wold().cldf_dir.joinpath("cldf-metadata.json").as_posix(),
    columns=columns,
    namespace=dict(namespace),
    filter=lambda row: row["language_id"] in languages.keys()
    and row["concept_concepticon_id"],
)

print("[i] loaded lexibank datasets")

# add tone information to the correspondence datasets
tones = defaultdict(dict)
for row in chenhmongmien().etc_dir.read_csv("tones.tsv", delimiter="\t", dicts=True):
    tones[row["Language_ID"]][row["Tone"]] = row["Category"]
for row in wold().etc_dir.read_csv("tones.tsv", delimiter="\t", dicts=True):
    tones[row["Language_ID"]][row["Tone"]] = row["Category"]

# add tone categories to our datasets
for idx, doculect, token in chen.iter_rows("doculect", "tokens"):
    tc, tv = [], []
    for t, s in zip(token, soundclass(token, "cv")):
        if s == "T":
            tc.append(tones[doculect].get(t.replace("/", ""), "?"))
            tv.append(t)
    chen[idx, "tone_class"] = " ".join(tc)
    chen[idx, "tone_value"] = " ".join(tv)
for idx, doculect, token in whitehmong.iter_rows("doculect", "tokens"):
    tc, tv = [], []
    for t, s in zip(token, soundclass(token, "cv")):
        if s == "T":
            tc.append(tones[doculect].get(t.replace("/", ""), "?"))
            tv.append(t)
    whitehmong[idx, "tone_class"] = " ".join(tc)
    whitehmong[idx, "tone_value"] = " ".join(tv)
    whitehmong[idx, "chinese_gloss"] = ""
    whitehmong[idx, "subgroup"] = "Hmongic"

# identify concepts in the datasets which are common
selected_concepts = set([c for c in ratliff.rows if c in chen.rows])

# create a new dataset
C = {
    0: [x[1] for x in namespace]
    + ["ratliff_language", "ratliff_tokens", "ratliff_index", "ratliff_cogid"]
}
idx = 1
for wl in [whitehmong, chen]:
    for i, c, l in wl.iter_rows("concept", "doculect"):
        if c in selected_concepts:
            tmp = [wl[i, x] for x in C[0][:-4]] + [languages[l][0], "", "", ""]
            C[idx] = tmp
            idx += 1
wl = Wordlist(C)
print("[i] created wordlist")

## add ratliff's info.
for language in wl.cols:
    rows = wl.get_dict(col=language, flat=True)
    ratliff_tmp = ratliff.get_dict(col=languages[language][0])
    for concept, idxs in rows.items():
        best_match, best_idx, dst = 0, 0, 1
        if ratliff_tmp[concept]:
            ratliff_tks = ratliff[ratliff_tmp[concept][0], "tokens"]
            for idx in idxs:
                for i, morpheme in enumerate(basictypes.lists(wl[idx, "tokens"]).n):
                    p = Pairwise(ratliff_tks, morpheme)
                    p.align(distance=True)
                    if p.alignments[0][-1] < dst:
                        dst = p.alignments[0][-1]
                        best_match, best_idx = idx, i
            if best_match:
                wl[best_match, "ratliff_tokens"] = ratliff_tks
                wl[best_match, "ratliff_index"] = best_idx
                wl[best_match, "cogid"] = ratliff[ratliff_tmp[concept][0], "cogid"]
                wl[best_match, "ratliff_cogid"] = ratliff[ratliff_tmp[concept][0], 'cogid']
            for idx in idxs:
                if idx != best_match:
                    wl[idx, 'cogid'] = 0
                    wl[idx, 'ratliff_cogid'] = 0

print("[i] added best matches")

wl.output(
    "tsv",
    filename=base_path.joinpath("hmong-mien-wordlist").as_posix(),
    ignore="all",
    prettify=False)

