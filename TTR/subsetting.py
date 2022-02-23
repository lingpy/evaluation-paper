
"""
Demostration purpose. This script can be ignore in the workflow. One can use this script as a template to make tables for the manuscript or presentation. 
"""

from lingpy import *
from pyedictor.util import *
from pyedictor import fetch
from collections import Counter
from tabulate import tabulate


# pull from Edictor
wl = fetch(
    "liusinitic",
    concepts=["float", "earth", "back", "we", "swim", "moon", "wife", "husband", "man", "woman"],
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

wl.output("tsv", filename="liusinitic-subset", prettify=False)