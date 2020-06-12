from lingpy import *
from lingpy import Wordlist
from lexibank_chenhmongmien import Dataset as chenhmongmien
from lexibank_ratliffhmongmien import Dataset as ratliffhmongmien
from pyconcepticon import Concepticon
from cldfcatalog import Config

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
ratliff = Wordlist.from_cldf(
    ratliffhmongmien().cldf_dir.joinpath("cldf-metadata.json").as_posix(),
    columns=columns,
    namespace=namespace,
)
chen = Wordlist.from_cldf(
    chenhmongmien().cldf_dir.joinpath("cldf-metadata.json").as_posix(),
    columns=columns,
    namespace=namespace,
)

concepticon = Concepticon(Config.from_file().get_clone("concepticon"))
concepts_ref = {}
for concept in concepticon.conceptlists["Chen-2012-888"].concepts.values():
    if concept.concepticon_id:
        concepts_ref[concept.concepticon_gloss] = concept.concepticon_id

concepts = set()
for c in ratliff.concept:
    if c in concepts_ref.keys():
        concepts.add(concepts_ref[c])

languages = {
    row[0]: [row[3], row[4]]
    for row in csv2list("../languages.tsv", strip_lines=False)[1:]
}

Combine = {0: [x for x in namespace.values()] + ["classification", "dataset"]}
entry_id = 1
ds = [ratliff, chen]
for dataset in ds:
    for idx, c, l in dataset.iter_rows("concepticon", "doculect"):
        if c in concepts:
            if l in languages:
                Combine[entry_id] = []
                tmp = [dataset[idx, x] for x in Combine[0][:13]]
                tmp = tmp + languages.get(l, "?")
                Combine[entry_id] = tmp
                entry_id += 1

Combine_wl = Wordlist(Combine)
Combine_wl.output("tsv", filename="HM-wordlist", prettify=False)
