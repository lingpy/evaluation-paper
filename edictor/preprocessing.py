"""
Preprocess data for analysis.
"""
from lingpy.compare.partial import Partial
from lingpy import Wordlist
from lingrex.cognates import common_morpheme_cognates, salient_cognates

def run(wordlist):
    D = {0: [c for c in wordlist.columns]}
    new_columns = [c for c in wordlist.columns] + [
            "strictid", "looseid", "commonid", "salientid"]
    mcogid = max(wordlist.get_etymdict(ref="cogids"))+1
    # turn empty comments into empty strings (otherwise it is None)
    for idx in wordlist:
        if not wordlist[idx, "note"]:
            wordlist[idx, "note"] = ""
    for idx in wordlist:
        if "!i" in wordlist[idx, "note"]:
            pass
        elif "!b" in wordlist[idx, "note"]:
            cogids = wordlist[idx, "cogids"]
            new_cogids = []
            for c in cogids:
                new_cogids += [mcogid]
                mcogid += 1
            wordlist[idx, "cogids"] = new_cogids
            D[idx] = [wordlist[idx, c] for c in D[0]]
        else:
            D[idx] = [wordlist[idx, c] for c in D[0]]
    new_wordlist = Partial(D)
    for conversion in ["strict", "loose"]:
        new_wordlist.add_cognate_ids(
                "cogids", conversion+"id", idtype=conversion)
    common_morpheme_cognates(
            new_wordlist,
            ref="commonid",
            cognates="cogids",
            morphemes="automorphemes"
            )
    salient_cognates(
            new_wordlist,
            ref="salientid",
            cognates="cogids",
            )
    # reduce columns
    D = {0: new_columns}
    for idx in new_wordlist:
        D[idx] = [new_wordlist[idx, c] for c in new_columns]

    return Wordlist(D)

