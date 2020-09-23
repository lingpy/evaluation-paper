from lingpy import *
from util import data_path, base_path

# load manual list
manual_wl = Wordlist(base_path.joinpath("hmeval.tsv").as_posix())
manual_cogid_dict = {}
for idx in manual_wl:
    value_tokens = manual_wl[idx, "tokens"]
    value_cogid = manual_wl[idx, "cogid"]
    value_morpheme = manual_wl[idx, "morphemes"]
    value_note = manual_wl[idx, "note"]
    manual_cogid_dict[idx] = {
        "data_tokens": " ".join(value_tokens),
        "manual_cogid": value_cogid,
        "manual_morphemes": value_morpheme,
        "manual_note": value_note,
    }


# load the merged dataset, and add two columns
wl = Wordlist(base_path.joinpath("hmong-mien-wordlist.tsv").as_posix())
wl.add_entries("note", "tokens", lambda x: x)
wl.add_entries("manual_morphemes", "tokens", lambda x: x)

# further filter.
for idx in wl:
    if idx in manual_cogid_dict.keys():
        wl_tokens = " ".join(wl[idx, "tokens"])
        if wl_tokens == manual_cogid_dict[idx]["data_tokens"]:
            wl[idx, "cogid"] = manual_cogid_dict[idx]["manual_cogid"]
            wl[idx, "manual_morphemes"] = manual_cogid_dict[idx]["manual_morphemes"]
            wl[idx, "note"] = manual_cogid_dict[idx]["manual_note"]
        else:
            print("This is not a match")
            print(wl[idx, "tokens"], manual_wl[idx, "tokens"])

# for filtering
output_dict = {0: wl.columns}
for idx in wl:
    tmp_entry = []
    if wl[idx, "note"] != "!remove!":
        tmp_entry = [wl[idx, head] for head in output_dict[0]]
        output_dict[idx] = tmp_entry

output_wl = Wordlist(output_dict)
output_wl.output(
    "tsv",
    filename=base_path.joinpath("hmong-mien-wordlist-modified").as_posix(),
    ignore=all,
    prettify=False,
)
