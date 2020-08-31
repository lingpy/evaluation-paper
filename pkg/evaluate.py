"""
Evaluate the data in a simple way.
"""
from lingpy import *
from lingpy.evaluate.acd import bcubes
from lingpy.evaluate.acd import diff, _get_bcubed_score
from util import base_path
from tabulate import tabulate


def renumber(liste):
    x = {}
    count = 1
    out = []
    for idx in liste:
        if idx in x:
            out += [x[idx]]
        else:
            out += [count]
            x[idx] = count
            count += 1
    return out


wl = Wordlist(base_path.joinpath("hmong-mien-alignments.tsv").as_posix())

selected = set()
for concept in wl.rows:
    idxs = wl.get_list(row=concept, flat=True)
    concepts = set()
    for idx in idxs:
        if wl[idx, 'cogid'] != 0:
            concepts.add(wl[idx, 'doculect'])
    if len(concepts) >= 6:
        selected.add(concept)


D = {0: wl.columns}
new_cogid = max([wl[idx, 'cogid'] for idx in wl])+1
for idx in wl:
    if wl[idx, "cogid"] != 0 and wl[idx, 'concept'] in selected:
        D[idx] = wl[idx]
    elif wl[idx, 'concept'] in selected:
        wl[idx, 'cogid'] = new_cogid
        new_cogid += 1
        D[idx] = wl[idx]


wl_filtered = Wordlist(D)
# print("[Title] Normal cogid v.s. Ratliff congate")
autocogid_precision, autocogid_recall, autocogid_fscores = bcubes(
    wl_filtered, "cogid", "autocogid", pprint=False
)

# salient v.s. Ratliff
wl_filtered.add_entries("salientid", "autocogid", lambda x: x)
for idx in wl_filtered:
    ratliff_index = wl_filtered[idx, "ratliff_index"]
    if ratliff_index:
        ratliff_index = int(ratliff_index)
        cogid = wl_filtered[idx, "cogids"][ratliff_index]
        wl_filtered[idx, "salientid"] = cogid

salientid_precision, salientid_recall, salientid_fscores = bcubes(
    wl_filtered, "cogid", "salientid", pprint=False
)

# strict v.s. Ratliff
strictid_precision, strictid_recall, strictid_fscores = bcubes(
    wl_filtered, "cogid", "strictid", pprint=False
)

# loose v.s. Ratliff
looseid_precision, looseid_recall, looseid_fscores = bcubes(
    wl_filtered, "cogid", "looseid", pprint=False
)

# splitter v.s. Ratliff
splitid_precision, splitid_recall, splitid_fscores = bcubes(
    wl_filtered, "cogid", "splitid", pprint=False
)

# lumper v.s. Ratliff
lumpid_precision, lumpid_recall, lumpid_fscores = bcubes(
    wl_filtered, "cogid", "lumpid", pprint=False
)

# print to screen:
header = ["RESULT", "NORMAL", "SALIENT", "STRICT", "LOOSE", "SPLIT", "LUMP"]
table = [
    [
        "PRECISION",
        autocogid_precision,
        salientid_precision,
        strictid_precision,
        looseid_precision,
        splitid_precision,
        lumpid_precision,
    ],
    [
        "RECALL",
        autocogid_recall,
        salientid_recall,
        strictid_recall,
        looseid_recall,
        splitid_recall,
        lumpid_recall,
    ],
    [
        "F-SCORES",
        autocogid_fscores,
        salientid_fscores,
        strictid_fscores,
        looseid_fscores,
        splitid_fscores,
        lumpid_fscores,
    ],
]
print(tabulate(table, header, tablefmt="github"))

# file output
wl_filtered.output(
    "tsv",
    filename=base_path.joinpath("hmong-mien-evaluation-output").as_posix(),
    ignore="all",
    prettify=False,
)


# print to file: evaluation output per concept per language.
text = ""
for concept in wl_filtered.rows:
    idxs = wl_filtered.get_list(row=concept, flat=True)
    cog_ratliff = [wl_filtered[idx, "cogid"] for idx in idxs]
    cog_network = [wl_filtered[idx, "autocogid"] for idx in idxs]
    form_ratliff = [wl_filtered[idx, "ratliff_tokens"] for idx in idxs]
    form_network = [wl_filtered[idx, "tokens"] for idx in idxs]
    langs = [wl_filtered[idx, "doculect"] for idx in idxs]

    cog_RATLIFF = renumber(cog_ratliff)
    cog_NETWORk = renumber(cog_network)

    r = _get_bcubed_score(cog_RATLIFF, cog_NETWORk)
    p = _get_bcubed_score(cog_NETWORk, cog_RATLIFF)
    f = 2 * ((r * p) / (p + r))

    if p < 1 or r < 1:
        text += "## Concept {0}\n".format(concept)
        text += "False Positives: {0:.2f}\n".format(1 - p)
        text += "False Negatives: {0:.2f}\n".format(1 - r)
        text += "Accuracy:        {0:.2f}\n".format(f)

        text += "ID | Language | Word | Word (Ratl.) | Cogn. | Cogn.  (Ratl.)\n"
        text += "--- | --- | --- | --- | --- | --- \n"
        for line in sorted(
            zip(idxs, langs, form_network, form_ratliff, cog_NETWORk, cog_RATLIFF),
            key=lambda x: (x[5], x[4], x[1]),
        ):
            text += " | ".join([str(x) for x in line]) + "\n"
        text += "\n"

with open(base_path.joinpath("evaluation.md").as_posix(), "w") as f:
    f.write(text)
