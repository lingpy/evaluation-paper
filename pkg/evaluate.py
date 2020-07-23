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
print("[!] Bcubes with normal cogids")
bcubes(wl_filtered, "autocogid", "cogid")

# check with ratliff index
print("[!] Bcubes with Ratliff index")
wl_filtered.add_entries("auto2cogid", "autocogid", lambda x: x)
C = {}
for idx in wl_filtered:
    ratliff_index = wl_filtered[idx, "ratliff_index"]
    if ratliff_index:
        ratliff_index = int(ratliff_index)
        cogid = wl_filtered[idx, "cogids"][ratliff_index]
        wl_filtered[idx, "auto2cogid"] = cogid
        # C[idx] = cogid
# wl_filtered.add_entries('auto2cogid', C, lambda : x)
bcubes(wl_filtered, "auto2cogid", "cogid")

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
    cog_auto = [wl_filtered[idx, "autocogid"] for idx in idxs]
    form_ratliff = [wl_filtered[idx, "ratliff_tokens"] for idx in idxs]
    form_auto = [wl_filtered[idx, "tokens"] for idx in idxs]
    langs = [wl_filtered[idx, "doculect"] for idx in idxs]

    cog_RATLIFF = renumber(cog_ratliff)
    cog_AUTO = renumber(cog_auto)

    r = _get_bcubed_score(cog_RATLIFF, cog_AUTO)
    p = _get_bcubed_score(cog_AUTO, cog_RATLIFF)
    f = 2 * ((r * p) / (p + r))

    if p < 1 or r < 1:
        text += "## Concept {0}\n".format(concept)
        text += "False Positives: {0:.2f}\n".format(1 - p)
        text += "False Negatives: {0:.2f}\n".format(1 - r)
        text += "Accuracy:        {0:.2f}\n".format(f)

        text += "ID | Language | Word | Word (Ratl.) | Cogn. | Cogn.  (Ratl.)\n"
        text += "--- | --- | --- | --- | --- | --- \n"
        for line in sorted(
            zip(idxs, langs, form_auto, form_ratliff, cog_AUTO, cog_RATLIFF),
            key=lambda x: (x[5], x[4], x[1]),
        ):
            text += " | ".join([str(x) for x in line]) + "\n"
        text += "\n"

with open(base_path.joinpath("evaluation.md").as_posix(), "w") as f:
    f.write(text)
