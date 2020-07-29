"""
Evaluate the data in a simple way.
"""
from lingpy import *
from lingpy.evaluate.acd import bcubes
from lingpy.evaluate.acd import diff, _get_bcubed_score
from util import base_path


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

D = {0: wl.columns}
didx = 1
for idx in wl:
    if wl[idx, "cogid"] != 0:
        D[didx] = []
        for lab in D[0]:
            D[didx].append(wl[idx, lab])
        didx += 1

wl_filtered = Wordlist(D)
print("[Title] Normal cogid v.s. Ratliff congate")
bcubes(wl_filtered, "network_cogid", "cogid")

# check with ratliff index
print("[Title] Salien part v.s. Ratliff cognate")
wl_filtered.add_entries("network2cogid", "network_cogid", lambda x: x)
for idx in wl_filtered:
    ratliff_index = wl_filtered[idx, "ratliff_index"]
    if ratliff_index:
        ratliff_index = int(ratliff_index)
        cogid = wl_filtered[idx, "cogids"][ratliff_index]
        wl_filtered[idx, "network2cogid"] = cogid

bcubes(wl_filtered, "network2cogid", "cogid")

# strict v.s. Ratliff 
print("[Title] Strict v.s. Ratliff cognate")
bcubes(wl_filtered, "strict_cogid", "cogid")

# loose v.s. Ratliff 
print("[Title] loose v.s. Ratliff cognate")
bcubes(wl_filtered, "loose_cogid", "cogid")

wl_filtered.output(
    "tsv",
    filename=base_path.joinpath("hmong-mien-evaluation-output").as_posix(),
    ignore="all",
    prettify=False,
)

text = ""
for concept in wl_filtered.rows:
    idxs = wl_filtered.get_list(row=concept, flat=True)
    cog_ratliff = [wl_filtered[idx, "cogid"] for idx in idxs]
    cog_network = [wl_filtered[idx, "network_cogid"] for idx in idxs]
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
