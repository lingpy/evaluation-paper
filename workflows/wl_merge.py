from lingpy import *
from lingpy import Wordlist
from lexibank_chenhmongmien import Dataset as chenhmongmien
from lexibank_ratliffhmongmien import Dataset as ratliffhmongmien
from lexibank_wold import Dataset as wold
from pyconcepticon import Concepticon
from cldfcatalog import Config

"""
This script merged chen and wold data, and add ratliff's cognates as references
"""
# set up structure
columns = [
    "local_id",
    "id",
    "language_id",
    "language_name",
    "language_subgroup",
    "language_glottocode",
    "concept_name",
    "concept_concepticon_id",
    "concept_concepticon_gloss",
    "value",
    "form",
    "segments",
    "cogid_cognateset_id",
]
namespace = {
    "id": "lexibank_id",
    "language_subgroup": "subgroup",
    "local_id": "id_in_source",
    "concept_concepticon_gloss": "concept",
    "concept_name": "concept_in_source",
    "concept_chinese_gloss": "chinese_gloss",
    "language_id": "doculect",
    "language_name": "doculect_name",
    "language_glottocode": "glottocode",
    "segments": "tokens",
    "concept_concepticon_id": "concepticon",
    "parameter_id": "concepticon_id",
    "cogid_cognateset_id": "cogid",
}

concepticon = Concepticon(Config.from_file().get_clone("concepticon"))
concepts_ref = {}
for concept in concepticon.conceptlists["Chen-2012-888"].concepts.values():
    if concept.concepticon_id:
        concepts_ref[concept.concepticon_gloss] = concept.concepticon_id

languages = {
    row[0]: [row[3], row[4]]
    for row in csv2list("../languages.tsv", strip_lines=False)[1:]
}
# load datasets
ratliff = Wordlist.from_cldf(
    ratliffhmongmien().cldf_dir.joinpath("cldf-metadata.json").as_posix(),
    columns=columns,
    namespace=namespace,
    filter=lambda row: row["language_id"] in languages.keys(),
)
chen = Wordlist.from_cldf(
    chenhmongmien().cldf_dir.joinpath("cldf-metadata.json").as_posix(),
    columns=columns,
    namespace=namespace,
    filter=lambda row: row["language_id"] in languages.keys(),
)

whitehmong = Wordlist.from_cldf(
    wold().cldf_dir.joinpath("cldf-metadata.json").as_posix(),
    columns=columns,
    namespace=namespace,
    filter=lambda row: row["language_id"] == "WhiteHmong",
)

# cognate id info from ratliff, need to confirm with Mattis
ratliff.add_entries("classification", "doculect", lambda x: languages[x][0])

# merging
concepts = set()
for c in ratliff.concept:
    if c in concepts_ref.keys():
        concepts.add(concepts_ref[c])

Combine = {0: [x for x in namespace.values()] + ["classification"]}
entry_id = 1
ds = [whitehmong, chen]
for dataset in ds:
    for idx, c, l in dataset.iter_rows("concepticon", "doculect"):
        if c in concepts:
            tmp = [dataset[idx, x] for x in Combine[0][:13]] + [languages[l][0]]
            Combine[entry_id] = tmp
            entry_id += 1

# adding info
Combine_wl = Wordlist(Combine)
Combine_wl.add_entries("ratliff_form", "classification", lambda x: "")
used_cogid = set()
for idx, concept, language, classification in Combine_wl.iter_rows(
    "concept", "doculect", "classification"
):
    for ridx in ratliff:
        if (
            concept == ratliff[ridx, "concept"]
            and classification == ratliff[ridx, "classification"]
        ):
            Combine_wl[idx, "cogid"] = ratliff[ridx, "cogid"]
            Combine_wl[idx, "ratliff_form"] = ratliff[ridx, "tokens"]
            used_cogid.add(ratliff[ridx, "cogid"])
Combine_wl.output("tsv", filename="HM-wordlist-for-evaluate", prettify=False)

# fix cogid ==0
min_cogid = max(used_cogid) + 1
for idx in Combine_wl:
    if Combine_wl[idx, "cogid"] == 0:
        Combine_wl[idx, "cogid"] = min_cogid
        min_cogid += 1

Combine_wl.output("tsv", filename="HM-wordlist", prettify=False)
